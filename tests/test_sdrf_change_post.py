"""Tests for posting the change report: label selection and GitHub calls."""

from __future__ import annotations

import json

import pytest


def report(*datasets):
    return {"schema_version": 1, "pr_number": 5, "head_sha": "a" * 40, "base_sha": "b" * 40,
            "summary": {"new": 0, "modified": 0, "deleted": 0, "risk": None},
            "datasets": list(datasets)}


def ds(status, risk):
    return {"id": "PXD1", "status": status, "risk": risk, "changes": [], "findings": []}


@pytest.mark.parametrize("datasets,expected", [
    ([ds("new", None)], ["sdrf:new"]),
    ([ds("deleted", "high")], ["sdrf:deleted"]),
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
    def __init__(self, head_sha, comments, labels=()):
        self.head_sha = head_sha
        self.comments = comments
        self.labels = list(labels)
        self.calls = []

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == "GET" and path.endswith("/pulls/5"):
            return {"head": {"sha": self.head_sha}, "labels": [{"name": n} for n in self.labels]}
        if method == "GET" and "/comments" in path:
            return self.comments if "page=1" in path else []
        if method == "GET" and "/labels/" in path:
            return {"name": path.rsplit("/", 1)[-1]}
        return {}


def test_publish_updates_existing_bot_comment(post_mod):
    gh = FakeGitHub("a" * 40, [
        {"id": 1, "body": "unrelated", "user": {"login": "someone", "type": "User"}},
        {"id": 2, "body": post_mod.MARKER + " old", "user": {"login": "someone", "type": "User"}},
        {"id": 3, "body": post_mod.MARKER + " old", "user": {"login": "github-actions[bot]",
                                                             "type": "Bot"}},
    ], labels=["sdrf:modified-low"])
    post_mod.publish(gh, "o/r", report(ds("modified", "high")), "a" * 40, "BODY")
    methods = [(m, p) for m, p, _ in gh.calls]
    assert ("PATCH", "/repos/o/r/issues/comments/3") in methods
    assert not any(m == "POST" and p.endswith("/issues/5/comments") for m, p in methods)
    assert ("POST", "/repos/o/r/issues/5/labels") in methods
    assert ("DELETE", "/repos/o/r/issues/5/labels/sdrf%3Amodified-low") in methods


def test_publish_creates_comment_when_missing(post_mod):
    gh = FakeGitHub("a" * 40, [])
    post_mod.publish(gh, "o/r", report(ds("new", None)), "a" * 40, "BODY")
    assert ("POST", "/repos/o/r/issues/5/comments", {"body": "BODY"}) in gh.calls


def test_publish_refuses_head_mismatch(post_mod):
    gh = FakeGitHub("c" * 40, [])
    with pytest.raises(SystemExit):
        post_mod.publish(gh, "o/r", report(ds("new", None)), "a" * 40, "BODY")
    assert all(m == "GET" for m, _, _ in gh.calls)


def test_main_rejects_oversized_report(post_mod, tmp_path, monkeypatch):
    p = tmp_path / "r.json"
    p.write_text(json.dumps(report()) + " " * (post_mod.MAX_REPORT_BYTES + 1))
    monkeypatch.setenv("GITHUB_TOKEN", "t")
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("WORKFLOW_HEAD_SHA", "a" * 40)
    with pytest.raises(SystemExit):
        post_mod.main([str(p)])
