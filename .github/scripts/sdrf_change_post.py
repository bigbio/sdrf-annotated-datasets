#!/usr/bin/env python3
"""Post the SDRF change report to its pull request: one sticky comment plus risk labels.

Runs in the privileged workflow_run job. The report artifact was produced from untrusted PR
code, so it is size-checked and validated, and the PR it names must have the head commit the
triggering run was built from before anything is written.

Usage: sdrf_change_post.py report.json
Environment: GITHUB_TOKEN, GITHUB_REPOSITORY, WORKFLOW_HEAD_SHA, optional GITHUB_STEP_SUMMARY
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sdrf_change_render import MARKER, RANK, render, validate_report  # noqa: E402

API = "https://api.github.com"
MAX_REPORT_BYTES = 5 * 1024 * 1024
LABEL_COLORS = {
    "sdrf:modified-high": ("d73a4a", "SDRF PR changes existing datasets: high-risk changes"),
    "sdrf:modified-medium": ("fb8c00", "SDRF PR changes existing datasets: medium-risk changes"),
    "sdrf:modified-low": ("fbca04", "SDRF PR changes existing datasets: low-risk changes"),
    "sdrf:new": ("0e8a16", "SDRF PR adds new datasets"),
    "sdrf:deleted": ("6a737d", "SDRF PR deletes datasets"),
}


class GitHub:
    def __init__(self, token: str):
        self.token = token

    def request(self, method: str, path: str, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(API + path, data=data, method=method, headers={
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and method == "GET":
                return None
            raise
        return json.loads(raw) if raw else {}


def labels_for(report: dict) -> list[str]:
    datasets = report["datasets"]
    wanted = set()
    if any(d.get("status") == "new" for d in datasets):
        wanted.add("sdrf:new")
    if any(d.get("status") == "deleted" for d in datasets):
        wanted.add("sdrf:deleted")
    risks = [d["risk"] for d in datasets if d.get("status") == "modified" and d.get("risk") in RANK]
    if risks:
        wanted.add(f"sdrf:modified-{max(risks, key=RANK.__getitem__)}")
    return sorted(wanted)


def plan_labels(current: list[str], wanted: list[str]) -> tuple[list[str], list[str]]:
    add = [n for n in wanted if n not in current]
    remove = [n for n in current if n in LABEL_COLORS and n not in wanted]
    return add, remove


def _find_comment(gh, repo: str, pr: int):
    for page in range(1, 11):
        comments = gh.request("GET", f"/repos/{repo}/issues/{pr}/comments?per_page=100&page={page}") or []
        for c in comments:
            user = c.get("user") or {}
            if MARKER in (c.get("body") or "") and user.get("type") == "Bot":
                return c
        if len(comments) < 100:
            return None
    return None


def publish(gh, repo: str, report: dict, head_sha: str, body: str) -> None:
    pr_number = report["pr_number"]
    pr = gh.request("GET", f"/repos/{repo}/pulls/{pr_number}")
    if not pr or (pr.get("head") or {}).get("sha") != head_sha:
        raise SystemExit(f"PR #{pr_number} head does not match the workflow run; not posting")

    existing = _find_comment(gh, repo, pr_number)
    if existing:
        gh.request("PATCH", f"/repos/{repo}/issues/comments/{existing['id']}", {"body": body})
    else:
        gh.request("POST", f"/repos/{repo}/issues/{pr_number}/comments", {"body": body})

    current = [label["name"] for label in pr.get("labels", [])]
    add, remove = plan_labels(current, labels_for(report))
    for name in add:
        if gh.request("GET", f"/repos/{repo}/labels/{quote(name, safe='')}") is None:
            color, description = LABEL_COLORS[name]
            gh.request("POST", f"/repos/{repo}/labels",
                       {"name": name, "color": color, "description": description})
    if add:
        gh.request("POST", f"/repos/{repo}/issues/{pr_number}/labels", {"labels": add})
    for name in remove:
        gh.request("DELETE", f"/repos/{repo}/issues/{pr_number}/labels/{quote(name, safe='')}")


def main(argv: list[str]) -> int:
    path = Path(argv[0])
    if path.stat().st_size > MAX_REPORT_BYTES:
        raise SystemExit("report.json exceeds the size limit")
    report = validate_report(json.loads(path.read_text(encoding="utf-8")))

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as fh:
            fh.write(render(report, max_chars=10**9))

    gh = GitHub(os.environ["GITHUB_TOKEN"])
    publish(gh, os.environ["GITHUB_REPOSITORY"], report, os.environ["WORKFLOW_HEAD_SHA"],
            render(report))
    print(f"Posted change report to PR #{report['pr_number']}; labels: {labels_for(report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
