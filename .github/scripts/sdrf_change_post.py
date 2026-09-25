#!/usr/bin/env python3
"""Post the SDRF change report to its pull request: one sticky comment plus risk labels.

Runs in the privileged comment job, triggered when the report workflow finishes, when an
allow-listed AI review bot comments, or when one submits a review. Every trigger does the same
thing: resolve the open PR through the API, find the newest successful report run for the PR's
current head commit, download its artifact, collect the bots' findings, and re-render the
comment. The PR number always comes from the API, never from the (PR-built) report.

Usage: sdrf_change_post.py
Environment: GITHUB_TOKEN, GITHUB_REPOSITORY, and PR_NUMBER and/or HEAD_SHA;
             optional GITHUB_STEP_SUMMARY
"""

from __future__ import annotations

import base64
import functools
import io
import json
import os
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdrf_change_render import MARKER, RANK, render, validate_report  # noqa: E402
from sdrf_external_reviews import collect_notes  # noqa: E402

API = "https://api.github.com"
REPORT_WORKFLOW = "sdrf-change-report.yml"
ARTIFACT_NAME = "sdrf-change-report"
COMMENT_AUTHOR = "github-actions[bot]"
MAX_ARTIFACT_BYTES = 20 * 1024 * 1024
MAX_REPORT_BYTES = 5 * 1024 * 1024
SUMMARY_MAX_CHARS = 400_000
CLEARED_BODY = (f"{MARKER}\n### SDRF change report\n\n"
                "This PR no longer changes dataset SDRF files.\n")
LABEL_COLORS = {
    "sdrf:modified-high": ("d73a4a", "SDRF PR changes existing datasets: high-risk changes"),
    "sdrf:modified-medium": ("fb8c00", "SDRF PR changes existing datasets: medium-risk changes"),
    "sdrf:modified-low": ("fbca04", "SDRF PR changes existing datasets: low-risk changes"),
    "sdrf:new": ("0e8a16", "SDRF PR adds new datasets"),
    "sdrf:deleted": ("6a737d", "SDRF PR deletes datasets"),
}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class GitHub:
    def __init__(self, token: str):
        self.token = token

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"}

    def request(self, method: str, path: str, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(API + path, data=data, method=method,
                                     headers={**self._headers(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and method == "GET":
                return None
            raise
        return json.loads(raw) if raw else {}

    def download(self, url: str) -> bytes:
        # The archive URL redirects to signed blob storage; the token must not follow it there.
        opener = urllib.request.build_opener(_NoRedirect)
        try:
            opener.open(urllib.request.Request(url, headers=self._headers()), timeout=30)
            raise ValueError("artifact download did not redirect")
        except urllib.error.HTTPError as exc:
            if exc.code not in (301, 302, 303, 307, 308):
                raise
            location = exc.headers["Location"]
        with urllib.request.urlopen(location, timeout=120) as resp:
            data = resp.read(MAX_ARTIFACT_BYTES + 1)
        if len(data) > MAX_ARTIFACT_BYTES:
            raise ValueError("report artifact exceeds the size limit")
        return data


def _paged(gh, path: str):
    sep = "&" if "?" in path else "?"
    for page in range(1, 11):
        items = gh.request("GET", f"{path}{sep}per_page=100&page={page}") or []
        yield from items
        if len(items) < 100:
            return


def labels_for(report: dict) -> list[str]:
    datasets = report["datasets"]
    wanted = set()
    if any(d.get("status") == "new" for d in datasets):
        wanted.add("sdrf:new")
    if any(d.get("status") == "deleted" and not d.get("remaining_files") for d in datasets):
        wanted.add("sdrf:deleted")
    risks = [d["risk"] for d in datasets if d.get("risk") in RANK
             and (d.get("status") == "modified"
                  or (d.get("status") == "deleted" and d.get("remaining_files")))]
    if risks:
        wanted.add(f"sdrf:modified-{max(risks, key=RANK.__getitem__)}")
    return sorted(wanted)


def plan_labels(current: list[str], wanted: list[str]) -> tuple[list[str], list[str]]:
    add = [n for n in wanted if n not in current]
    remove = [n for n in current if n in LABEL_COLORS and n not in wanted]
    return add, remove


def find_pr_by_head(gh, repo: str, head_sha: str) -> dict | None:
    for pr in _paged(gh, f"/repos/{repo}/pulls?state=open"):
        if (pr.get("head") or {}).get("sha") == head_sha:
            return pr
    return None


def find_report(gh, repo: str, head_sha: str, pr_number: int) -> tuple[dict | None, bool]:
    """Return (report, a finished report run exists) for this PR's head commit.

    Runs are searched newest first. A run is taken as this PR's when the report inside names
    the PR, or, for a run without an artifact (no SDRF changes), when GitHub lists the PR on
    the run or lists no PR at all (fork PRs).
    """
    listing = gh.request(
        "GET", f"/repos/{repo}/actions/workflows/{REPORT_WORKFLOW}/runs"
               f"?head_sha={head_sha}&event=pull_request&status=completed&per_page=20") or {}
    runs = [r for r in listing.get("workflow_runs", []) if r.get("conclusion") == "success"]
    runs.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    for run in runs:
        listed = [p.get("number") for p in run.get("pull_requests") or []]
        arts = (gh.request("GET", f"/repos/{repo}/actions/runs/{run['id']}/artifacts") or {}).get("artifacts", [])
        art = next((a for a in arts if a.get("name") == ARTIFACT_NAME and not a.get("expired")), None)
        if art is None:
            if not listed or pr_number in listed:
                return None, True
            continue
        if art.get("size_in_bytes", 0) > MAX_ARTIFACT_BYTES:
            raise ValueError("report artifact exceeds the size limit")
        with zipfile.ZipFile(io.BytesIO(gh.download(art["archive_download_url"]))) as zf:
            info = zf.getinfo("report.json")
            if info.file_size > MAX_REPORT_BYTES:
                raise ValueError("report.json exceeds the size limit")
            report = validate_report(json.loads(zf.read(info)))
        if report["pr_number"] == pr_number:
            return report, True
    return None, False


def _existing_comment(gh, repo: str, pr_number: int):
    for c in _paged(gh, f"/repos/{repo}/issues/{pr_number}/comments"):
        # Only our own comment: review bots may quote the marker when they review this report.
        if MARKER in (c.get("body") or "") and (c.get("user") or {}).get("login") == COMMENT_AUTHOR:
            return c
    return None


def _sync_labels(gh, repo: str, pr: dict, wanted: list[str]) -> None:
    number = pr["number"]
    add, remove = plan_labels([label["name"] for label in pr.get("labels", [])], wanted)
    for name in add:
        if gh.request("GET", f"/repos/{repo}/labels/{quote(name, safe='')}") is None:
            color, description = LABEL_COLORS[name]
            gh.request("POST", f"/repos/{repo}/labels",
                       {"name": name, "color": color, "description": description})
    if add:
        gh.request("POST", f"/repos/{repo}/issues/{number}/labels", {"labels": add})
    for name in remove:
        gh.request("DELETE", f"/repos/{repo}/issues/{number}/labels/{quote(name, safe='')}")


def update(gh, repo: str, pr_number: int | None = None, head_sha: str | None = None,
           summary_file: str | None = None) -> str:
    if pr_number:
        pr = gh.request("GET", f"/repos/{repo}/pulls/{pr_number}")
        if not pr or pr.get("state") != "open":
            return "no open PR"
    else:
        pr = find_pr_by_head(gh, repo, head_sha)
        if not pr:
            return "no open PR for this commit"
    current_sha = pr["head"]["sha"]
    if head_sha and head_sha != current_sha:
        return "stale run"

    report, has_run = find_report(gh, repo, current_sha, pr["number"])
    existing = _existing_comment(gh, repo, pr["number"])
    if report is None:
        if not has_run:
            return "report not ready"
        if existing is None:
            return "nothing to report"
        gh.request("PATCH", f"/repos/{repo}/issues/comments/{existing['id']}", {"body": CLEARED_BODY})
        _sync_labels(gh, repo, pr, [])
        return "cleared"

    @functools.cache
    def read_file(path):
        # Read as data through the API; PR code is never checked out or run in this job.
        found = gh.request("GET", f"/repos/{repo}/contents/{quote(path)}?ref={current_sha}")
        if not isinstance(found, dict) or found.get("encoding") != "base64":
            return None
        return base64.b64decode(found["content"]).decode("utf-8", errors="replace")

    notes = collect_notes(gh, repo, pr["number"], report, read_file=read_file)
    body = render(report, external=notes)
    if existing:
        gh.request("PATCH", f"/repos/{repo}/issues/comments/{existing['id']}", {"body": body})
    else:
        gh.request("POST", f"/repos/{repo}/issues/{pr['number']}/comments", {"body": body})
    _sync_labels(gh, repo, pr, labels_for(report))
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as fh:
            fh.write(render(report, max_chars=SUMMARY_MAX_CHARS, external=notes))
    return "posted"


def main() -> int:
    pr_env = os.environ.get("PR_NUMBER", "").strip()
    sha_env = os.environ.get("HEAD_SHA", "").strip()
    if not pr_env.isdigit() and not sha_env:
        raise SystemExit("PR_NUMBER or HEAD_SHA is required")
    status = update(GitHub(os.environ["GITHUB_TOKEN"]), os.environ["GITHUB_REPOSITORY"],
                    pr_number=int(pr_env) if pr_env.isdigit() else None,
                    head_sha=sha_env or None,
                    summary_file=os.environ.get("GITHUB_STEP_SUMMARY"))
    print(f"SDRF change report: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
