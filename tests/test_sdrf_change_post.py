"""Tests for posting the change report: PR resolution, artifact lookup, comment and labels."""

from __future__ import annotations

import io
import json
import re
import zipfile

import pytest

SHA = "a" * 40


def report(*datasets, pr=5):
    return {"schema_version": 1, "pr_number": pr, "head_sha": SHA, "base_sha": "b" * 40,
            "summary": {"new": 0, "modified": 0, "deleted": 0, "risk": None},
            "datasets": list(datasets)}


def ds(status, risk, id_="PXD1", **kw):
    d = {"id": id_, "path": f"datasets/{id_}/{id_}.sdrf.tsv", "status": status, "risk": risk,
         "changes": [], "findings": []}
    d.update(kw)
    return d


def zipped(obj) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("report.json", json.dumps(obj))
    return buf.getvalue()


@pytest.mark.parametrize("datasets,expected", [
    ([ds("new", None)], ["sdrf:new"]),
    ([ds("deleted", "high")], ["sdrf:deleted"]),
    ([ds("deleted", "medium", remaining_files=["x.sdrf.tsv"])], ["sdrf:modified-medium"]),
    ([ds("modified", "low"), ds("modified", "medium")], ["sdrf:modified-medium"]),
    ([ds("new", None), ds("modified", "high"), ds("deleted", "high")],
     ["sdrf:deleted", "sdrf:modified-high", "sdrf:new"]),
])
def test_labels_for(post_mod, datasets, expected):
    assert post_mod.labels_for(report(*datasets)) == expected


def test_plan_labels_keeps_unmanaged(post_mod):
    add, remove = post_mod.plan_labels(["bug", "sdrf:modified-low", "sdrf:new"],
                                       ["sdrf:new", "sdrf:modified-high"])
    assert add == ["sdrf:modified-high"]
    assert remove == ["sdrf:modified-low"]


class FakeGitHub:
    """Routes the handful of endpoints the poster uses."""

    def __init__(self, pr=None, open_prs=(), runs=(), artifacts=None, blobs=None, comments=(),
                 review_items=None):
        self.pr = pr
        self.open_prs = list(open_prs)
        self.runs = list(runs)
        self.artifacts = artifacts or {}
        self.blobs = blobs or {}
        self.comments = list(comments)
        self.review_items = review_items or {}
        self.calls = []

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        base = path.split("?")[0]
        if method != "GET":
            return {}
        page = re.search(r"[?&]page=(\d+)", path)
        if page and page.group(1) != "1":
            return []
        if base.endswith("/pulls/5"):
            return self.pr
        if base.endswith("/pulls"):
            return self.open_prs
        if "/actions/workflows/" in base:
            return {"workflow_runs": self.runs}
        if base.endswith("/artifacts"):
            return {"artifacts": self.artifacts.get(base.split("/")[-2], [])}
        if base.endswith("/issues/5/comments"):
            return self.comments
        if base.endswith("/reviews") or base.endswith("/pulls/5/comments"):
            return self.review_items.get(base.rsplit("/", 1)[-1], [])
        if "/labels/" in base:
            return {"name": base.rsplit("/", 1)[-1]}
        return None

    def download(self, url):
        self.calls.append(("DOWNLOAD", url, None))
        return self.blobs[url]


def pr(sha=SHA, labels=()):
    return {"number": 5, "state": "open", "head": {"sha": sha}, "labels": [{"name": n} for n in labels]}


def run(id_, pr_numbers=(5,)):
    return {"id": id_, "status": "completed", "conclusion": "success",
            "created_at": f"2026-09-17T10:0{id_}:00Z",
            "pull_requests": [{"number": n} for n in pr_numbers]}


def artifact(id_, size=100):
    return {"name": "sdrf-change-report", "size_in_bytes": size, "expired": False,
            "archive_download_url": f"https://api.github.com/artifacts/{id_}/zip"}


def bot_comment(body, id_=3):
    return {"id": id_, "body": body, "user": {"login": "github-actions[bot]", "type": "Bot"}}


def posted(gh, method, suffix):
    return [b for m, p, b in gh.calls if m == method and p.split("?")[0].endswith(suffix)]


def test_find_pr_by_head(post_mod):
    gh = FakeGitHub(open_prs=[{"number": 4, "head": {"sha": "c" * 40}}, pr()])
    assert post_mod.find_pr_by_head(gh, "o/r", SHA)["number"] == 5
    assert post_mod.find_pr_by_head(gh, "o/r", "d" * 40) is None


def test_find_report_uses_newest_run_for_this_pr(post_mod):
    r = report(ds("modified", "high"))
    other = report(ds("modified", "low"), pr=9)
    gh = FakeGitHub(runs=[run(1), run(2, pr_numbers=())],
                    artifacts={"1": [artifact(1)], "2": [artifact(2)]},
                    blobs={"https://api.github.com/artifacts/1/zip": zipped(r),
                           "https://api.github.com/artifacts/2/zip": zipped(other)})
    found, has_run = post_mod.find_report(gh, "o/r", SHA, 5)
    assert has_run is True
    assert found["datasets"][0]["risk"] == "high"


def test_find_report_without_artifact_means_no_sdrf_changes(post_mod):
    gh = FakeGitHub(runs=[run(1)], artifacts={"1": []})
    assert post_mod.find_report(gh, "o/r", SHA, 5) == (None, True)


def test_find_report_before_any_run(post_mod):
    assert post_mod.find_report(FakeGitHub(runs=[]), "o/r", SHA, 5) == (None, False)


def test_find_report_rejects_oversized_artifact(post_mod):
    gh = FakeGitHub(runs=[run(1)], artifacts={"1": [artifact(1, size=post_mod.MAX_ARTIFACT_BYTES + 1)]})
    with pytest.raises(ValueError):
        post_mod.find_report(gh, "o/r", SHA, 5)


def test_update_posts_comment_with_external_notes_and_labels(post_mod):
    r = report(ds("modified", "high", id_="PXD000513"))
    qodo = ("1\\. Yeast declared as invertebrate <code>🐞 Bug</code>\n\n<pre>\n"
            "PXD000513 uses an animal template for a fungus.\n</pre>")
    gh = FakeGitHub(pr=pr(labels=["sdrf:modified-low"]), runs=[run(1)],
                    artifacts={"1": [artifact(1)]},
                    blobs={"https://api.github.com/artifacts/1/zip": zipped(r)},
                    comments=[{"id": 8, "body": qodo, "user": {"login": "qodo-code-review[bot]", "type": "Bot"},
                               "html_url": "https://github.com/o/r/pull/5#issuecomment-8"}])
    status = post_mod.update(gh, "o/r", pr_number=5)
    assert status == "posted"
    (body,) = posted(gh, "POST", "/issues/5/comments")
    assert "Yeast declared as invertebrate" in body["body"]
    assert "([source](https://github.com/o/r/pull/5#issuecomment-8))" in body["body"]
    assert posted(gh, "POST", "/issues/5/labels") == [{"labels": ["sdrf:modified-high"]}]
    assert ("DELETE", "/repos/o/r/issues/5/labels/sdrf%3Amodified-low", None) in gh.calls


def test_update_edits_existing_bot_comment(post_mod):
    r = report(ds("new", None))
    marker = post_mod.MARKER
    gh = FakeGitHub(pr=pr(), runs=[run(1)], artifacts={"1": [artifact(1)]},
                    blobs={"https://api.github.com/artifacts/1/zip": zipped(r)},
                    comments=[{"id": 2, "body": marker, "user": {"login": "x", "type": "User"}},
                              {"id": 4, "body": marker, "user": {"login": "coderabbitai[bot]", "type": "Bot"}},
                              bot_comment(marker + " old", id_=3)])
    post_mod.update(gh, "o/r", pr_number=5)
    assert posted(gh, "PATCH", "/issues/comments/3")
    assert not posted(gh, "PATCH", "/issues/comments/2")
    assert not posted(gh, "PATCH", "/issues/comments/4")
    assert not posted(gh, "POST", "/issues/5/comments")


def test_update_uses_pr_from_api_not_report(post_mod):
    r = report(ds("modified", "high"), pr=77)
    gh = FakeGitHub(pr=pr(), runs=[run(1, pr_numbers=())], artifacts={"1": [artifact(1)]},
                    blobs={"https://api.github.com/artifacts/1/zip": zipped(r)})
    assert post_mod.update(gh, "o/r", pr_number=5) == "report not ready"
    assert not any("/issues/77" in p for _, p, _ in gh.calls)


def test_update_skips_stale_run(post_mod):
    gh = FakeGitHub(open_prs=[pr(sha="c" * 40)])
    assert post_mod.update(gh, "o/r", head_sha=SHA) == "no open PR for this commit"
    gh = FakeGitHub(pr=pr(sha="c" * 40))
    assert post_mod.update(gh, "o/r", pr_number=5, head_sha=SHA) == "stale run"


def test_update_clears_comment_and_labels_when_sdrf_changes_are_reverted(post_mod):
    gh = FakeGitHub(pr=pr(labels=["sdrf:new", "bug"]), runs=[run(1)], artifacts={"1": []},
                    comments=[bot_comment(post_mod.MARKER + " old")])
    assert post_mod.update(gh, "o/r", pr_number=5) == "cleared"
    (patch,) = posted(gh, "PATCH", "/issues/comments/3")
    assert "no longer changes dataset SDRF files" in patch["body"]
    assert ("DELETE", "/repos/o/r/issues/5/labels/sdrf%3Anew", None) in gh.calls
    assert not any(p.endswith("/labels/bug") for _, p, _ in gh.calls)


def test_update_without_sdrf_changes_and_no_comment_does_nothing(post_mod):
    gh = FakeGitHub(pr=pr(), runs=[run(1)], artifacts={"1": []})
    assert post_mod.update(gh, "o/r", pr_number=5) == "nothing to report"
    assert all(m == "GET" for m, _, _ in gh.calls)


def test_update_writes_bounded_job_summary(post_mod, tmp_path):
    r = report(ds("new", None))
    gh = FakeGitHub(pr=pr(), runs=[run(1)], artifacts={"1": [artifact(1)]},
                    blobs={"https://api.github.com/artifacts/1/zip": zipped(r)})
    summary = tmp_path / "summary.md"
    post_mod.update(gh, "o/r", pr_number=5, summary_file=str(summary))
    text = summary.read_text()
    assert post_mod.MARKER in text and len(text) <= post_mod.SUMMARY_MAX_CHARS
