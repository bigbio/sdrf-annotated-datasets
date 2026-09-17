"""Tests for collecting external AI reviewer findings and mapping them to datasets."""

from __future__ import annotations

import pytest

from conftest import load_script


@pytest.fixture(scope="module")
def ext():
    return load_script("sdrf_external_reviews")


QODO_SUMMARY = """<h3>Code Review by Qodo</h3>

<details>
<summary>  1.  Eight yeast datasets use animal terms <code>📘 Rule violation</code> <code>≡ Correctness</code></summary>

<pre>
Eight added SDRFs identify samples as <b><i>saccharomyces cerevisiae</i></b> while declaring the
animal-specific <b><i>NT=invertebrates;VV=v1.1.0</i></b> template layer. The mismatch occurs in
PXD000513 and PXD002392.
</pre>

<details>
<summary><strong>Agent Prompt</strong></summary>

```
## Fix Focus Areas
- datasets/PXD000513/PXD000513.sdrf.tsv[2-46]
- datasets/PXD002392/PXD002392.sdrf.tsv[2-21]
## Recommended Fix
1. Remove the invertebrates layer <code>x</code>
```
</details>
</details>

<details>
<summary>  2.  <s>Validation blocks the dataset</s> <code>✓ Resolved</code> <code>🐞 Bug</code></summary>

<pre>
PXD000513 failed validation.
</pre>
</details>
"""

QODO_INLINE = """<img src="https://img.shields.io/badge/High-634FD1?style=flat-square" alt="Action required">

1\\. Human samples are labeled yeast <code>🐞 Bug</code> <code>≡ Correctness</code>

<pre>
Rows 2-3 annotate the explicitly named human RBP assays as <b><i>saccharomyces cerevisiae</i></b>.
</pre>
"""

CODERABBIT_INLINE = """_🎯 Functional Correctness_ | _🟠 Major_ | _⚡ Quick win_

<details>
<summary>🔎 Supported by static analysis</summary>
lots of tool output mentioning PXD999999
</details>

**Organism column was replaced for every row.**

The organism changed from Homo sapiens to Mus musculus on all rows, but the publication describes
human donors. Check the source before accepting.

<!-- This is an auto-generated comment by CodeRabbit -->
"""


def report(*datasets):
    return {"datasets": list(datasets)}


def ds(id_, **kw):
    d = {"id": id_, "path": f"datasets/{id_}/{id_}.sdrf.tsv", "status": "new", "risk": None,
         "changes": [], "findings": []}
    d.update(kw)
    return d


class FakeGitHub:
    def __init__(self, issue_comments=(), reviews=(), review_comments=()):
        self.data = {"issues": list(issue_comments), "reviews": list(reviews),
                     "pulls": list(review_comments)}

    def request(self, method, path):
        if "page=1" not in path:
            return []
        if "/issues/" in path:
            return self.data["issues"]
        if path.split("?")[0].endswith("/reviews"):
            return self.data["reviews"]
        return self.data["pulls"]


def comment(login, body, url="https://github.com/o/r/pull/5#issuecomment-1", **kw):
    c = {"user": {"login": login}, "body": body, "html_url": url}
    c.update(kw)
    return c


def test_split_findings_uses_numbered_badged_items(ext):
    units = ext.split_findings(QODO_SUMMARY)
    assert len(units) == 2
    assert "Eight yeast datasets" in units[0] and "Remove the invertebrates" in units[0]


def test_title_and_detail_from_qodo(ext):
    unit = ext.split_findings(QODO_SUMMARY)[0]
    title = ext.title_of(unit)
    assert title == "Eight yeast datasets use animal terms"
    detail = ext.detail_of(unit, title)
    assert detail.startswith("Eight added SDRFs identify samples as saccharomyces cerevisiae")
    assert "<" not in detail and ">" not in detail


def test_title_and_detail_from_coderabbit(ext):
    title = ext.title_of(CODERABBIT_INLINE)
    assert title == "Organism column was replaced for every row."
    assert ext.detail_of(CODERABBIT_INLINE, title).startswith("The organism changed from Homo sapiens")


def test_resolved_findings_are_skipped(ext):
    units = ext.split_findings(QODO_SUMMARY)
    assert not ext.is_resolved(units[0])
    assert ext.is_resolved(units[1])


def test_summary_finding_maps_to_every_mentioned_dataset(ext):
    gh = FakeGitHub(issue_comments=[comment("qodo-code-review[bot]", QODO_SUMMARY)])
    notes = ext.collect_notes(gh, "o/r", 5, report(ds("PXD000513"), ds("PXD002392"), ds("PXD000001")))
    assert set(notes) == {"PXD000513", "PXD002392"}
    (note,) = notes["PXD000513"]
    assert note["reviewer"] == "qodo-code-review[bot]"
    assert note["title"] == "Eight yeast datasets use animal terms"
    assert note["url"] == "https://github.com/o/r/pull/5#issuecomment-1"


def test_inline_comment_maps_by_path_and_ignores_details(ext):
    gh = FakeGitHub(review_comments=[
        comment("coderabbitai[bot]", CODERABBIT_INLINE, path="datasets/PXD000001/PXD000001.sdrf.tsv"),
        comment("qodo-code-review[bot]", QODO_INLINE, path=".github/scripts/x.py"),
    ])
    notes = ext.collect_notes(gh, "o/r", 5, report(ds("PXD000001"), ds("PXD999999")))
    assert list(notes) == ["PXD000001"]


def test_unlisted_authors_are_ignored(ext):
    gh = FakeGitHub(issue_comments=[comment("someone", QODO_SUMMARY),
                                    comment("github-actions[bot]", QODO_SUMMARY)])
    assert ext.collect_notes(gh, "o/r", 5, report(ds("PXD000513"))) == {}


def test_duplicate_findings_are_merged_and_capped(ext):
    gh = FakeGitHub(
        issue_comments=[comment("qodo-code-review[bot]", QODO_SUMMARY)],
        review_comments=[comment("qodo-code-review[bot]", QODO_SUMMARY.replace("1.  Eight", "1.  Eight"),
                                 path="datasets/PXD000513/PXD000513.sdrf.tsv")]
        + [comment("coderabbitai[bot]", f"**Problem number {i}.**\n\nDetails about the problem here, long enough.",
                   path="datasets/PXD000513/PXD000513.sdrf.tsv") for i in range(10)])
    notes = ext.collect_notes(gh, "o/r", 5, report(ds("PXD000513")))
    titles = [n["title"] for n in notes["PXD000513"]]
    assert titles.count("Eight yeast datasets use animal terms") == 1
    assert len(titles) == ext.MAX_NOTES_PER_DATASET


def test_dataset_id_match_is_exact(ext):
    body = "1\\. Problem in PXD0005130 <code>🐞 Bug</code>\n\n<pre>\nDetails long enough to show.\n</pre>"
    gh = FakeGitHub(issue_comments=[comment("qodo-code-review[bot]", body)])
    assert ext.collect_notes(gh, "o/r", 5, report(ds("PXD000513"))) == {}


def test_confirmed_when_report_flags_same_column(ext):
    flagged = ds("PXD000001", status="modified", risk="high", changes=[
        {"column": "characteristics[organism]", "old": "Homo sapiens", "new": "Mus musculus",
         "rows": 3, "total_rows": 3, "kind": "replaced", "risk": "high"}])
    gh = FakeGitHub(review_comments=[
        comment("coderabbitai[bot]", CODERABBIT_INLINE, path="datasets/PXD000001/PXD000001.sdrf.tsv")])
    (note,) = ext.collect_notes(gh, "o/r", 5, report(flagged))["PXD000001"]
    assert note["confirmed_by"] == ["characteristics[organism]"]


def test_not_confirmed_without_matching_flag(ext):
    gh = FakeGitHub(issue_comments=[comment("qodo-code-review[bot]", QODO_SUMMARY)])
    (note,) = ext.collect_notes(gh, "o/r", 5, report(ds("PXD000513")))["PXD000513"]
    assert note["confirmed_by"] == []


def test_shorten_prefers_sentence_end_without_double_punctuation(ext):
    assert ext._shorten("First sentence is here. Second one is much longer than the limit allows.", 40) \
        == "First sentence is here."
    assert ext._shorten("word " * 30, 20).endswith("word…")


def test_clean_keeps_identifiers_and_unescapes_entities(ext):
    text = "Reports <b>instrument_cannot_write_data_file</b> in the repository&#x27;s gate, _emphasis_ and **bold**."
    assert ext.clean(text) == "Reports instrument_cannot_write_data_file in the repository's gate, emphasis and bold."


def test_finding_resolved_in_summary_hides_inline_copy(ext):
    summary = ("<summary>  2.  <s>Validation blocks the dataset</s> <code>✓ Resolved</code></summary>\n"
               "<pre>\nPXD000513 failed validation.\n</pre>")
    inline = "1\\. Validation blocks the dataset <code>🐞 Bug</code>\n\n<pre>\nPXD000513 gate fails on rows 2-31.\n</pre>"
    gh = FakeGitHub(issue_comments=[comment("qodo-code-review[bot]", summary)],
                    review_comments=[comment("qodo-code-review[bot]", inline,
                                             path="datasets/PXD000513/PXD000513.sdrf.tsv")])
    assert ext.collect_notes(gh, "o/r", 5, report(ds("PXD000513"))) == {}
