"""Tests for rendering the change report as a PR comment."""

from __future__ import annotations

import pytest


def dataset(id_, status="modified", risk="low", changes=None, findings=None, **kw):
    ds = {"id": id_, "path": f"datasets/{id_}/{id_}.sdrf.tsv", "status": status, "risk": risk,
          "restructured": False, "rows": {"old": 10, "new": 10, "added": 0, "removed": 0},
          "columns": {"added": [], "removed": []}, "changes": changes or [],
          "findings": findings or [],
          "quality": {"fixed": 1, "introduced": 0, "defects_head": {},
                      "parse_sdrf": {"base": "fail", "head": "pass"}}}
    ds.update(kw)
    return ds


def report(*datasets):
    order = {"low": 1, "medium": 2, "high": 3}
    risks = [d["risk"] for d in datasets if d["risk"]]
    return {"schema_version": 1, "pr_number": 7, "head_sha": "a" * 40, "base_sha": "b" * 40,
            "summary": {"new": sum(d["status"] == "new" for d in datasets),
                        "modified": sum(d["status"] == "modified" for d in datasets),
                        "deleted": sum(d["status"] == "deleted" for d in datasets),
                        "risk": max(risks, key=order.get) if risks else None},
            "datasets": list(datasets)}


SWAP = {"column": "characteristics[organism]", "old": "Homo sapiens", "new": "Mus musculus",
        "rows": 24, "total_rows": 24, "kind": "replaced", "relation": "unrelated", "risk": "high"}


def test_marker_headline_and_table(render_mod):
    body = render_mod.render(report(dataset("PXD000001", risk="high", changes=[SWAP])))
    assert body.startswith(render_mod.MARKER)
    assert "0 new · 1 modified · 0 deleted · highest risk: high" in body
    assert "| PXD000001 | modified | high | 10 → 10 | 1 fixed / 0 introduced; parse\\_sdrf fail → pass |" in body
    assert "characteristics\\[organism\\]: Homo sapiens → Mus musculus (24/24 rows) \\[unrelated\\]" in body


def test_high_risk_block_open_low_risk_closed(render_mod):
    body = render_mod.render(report(dataset("PXD1", risk="high", changes=[SWAP]),
                                    dataset("PXD2", risk="low")))
    assert "<details open>\n<summary><b>PXD1</b>" in body
    assert "<details>\n<summary><b>PXD2</b>" in body


def test_escape_neutralises_markup_and_mentions(render_mod):
    s = render_mod.escape("<img src=x> | @org/team [link](http://x) *b*")
    assert "<" not in s and ">" not in s
    assert "\\|" in s and "\\[" in s and "\\*" in s
    assert "@​org" in s


def test_escape_truncates(render_mod):
    assert render_mod.escape("x" * 500, limit=10) == "x" * 9 + "…"


def test_change_groups_capped(render_mod):
    changes = [dict(SWAP, old=f"v{i}", risk="medium") for i in range(40)]
    body = render_mod.render(report(dataset("PXD1", risk="medium", changes=changes)))
    assert body.count("→ Mus musculus") == 30
    assert "… and 10 more change groups" in body


def test_new_datasets_collapsed(render_mod):
    new = dataset("PXD9", status="new", risk=None,
                  quality={"fixed": 0, "introduced": 0, "defects_head": {"no_factor_value": 1},
                           "parse_sdrf": {"base": None, "head": "pass"}},
                  rows={"old": None, "new": 12, "added": 0, "removed": 0})
    body = render_mod.render(report(new))
    assert "<details>\n<summary>New datasets (1)</summary>" in body
    assert "| PXD9 | 12 | no\\_factor\\_value: 1 |" in body


def test_summary_rendered_only_when_present(render_mod):
    plain = render_mod.render(report(dataset("PXD1")))
    assert "AI-generated summary" not in plain
    body = render_mod.render(report(dataset("PXD1", summary="Organism corrected.")))
    assert "AI-generated summary. Verify against the diff above." in body
    assert "> Organism corrected." in body


def test_size_cap_drops_low_risk_blocks_first(render_mod):
    big = [dict(SWAP, old="x" * 100 + str(i), risk="low") for i in range(30)]
    r = report(dataset("PXDHIGH", risk="high", changes=[SWAP]),
               *[dataset(f"PXDLOW{i}", risk="low", changes=big) for i in range(10)])
    body = render_mod.render(r, max_chars=12000)
    assert len(body) <= 12000
    assert "<summary><b>PXDHIGH</b>" in body
    assert "dataset details omitted for size" in body
    full = render_mod.render(r, max_chars=10**9)
    assert "dataset details omitted" not in full


@pytest.mark.parametrize("bad", [
    None, [], {"schema_version": 2}, {"schema_version": 1, "pr_number": "7"},
    {"schema_version": 1, "pr_number": 0, "datasets": [], "summary": {}},
    {"schema_version": 1, "pr_number": True, "datasets": [], "summary": {}},
    {"schema_version": 1, "pr_number": 3, "datasets": {}, "summary": {}},
])
def test_validate_report_rejects(render_mod, bad):
    with pytest.raises(ValueError):
        render_mod.validate_report(bad)


def test_validate_report_accepts(render_mod):
    r = report(dataset("PXD1"))
    assert render_mod.validate_report(r) is r


NOTE = {"reviewer": "qodo-code-review[bot]", "url": "https://github.com/o/r/pull/7#discussion_r12",
        "title": "Eight yeast datasets use animal terms",
        "detail": "Samples are <b>yeast</b> but declare @team invertebrates.", "confirmed_by": []}


def test_external_notes_section(render_mod):
    notes = {"PXD1": [NOTE, dict(NOTE, title="Organism swapped", confirmed_by=["characteristics[organism]"],
                                 reviewer="coderabbitai[bot]")]}
    body = render_mod.render(report(dataset("PXD1", risk="high", changes=[SWAP])), external=notes)
    assert "#### External reviewer notes" in body
    assert "- **PXD1** · qodo-code-review\\[bot\\]: Eight yeast datasets use animal terms. " in body
    assert "&lt;b&gt;yeast&lt;/b&gt;" in body and "@​team" in body
    assert "([source](https://github.com/o/r/pull/7#discussion_r12))" in body
    assert "· also flagged by this report: characteristics\\[organism\\]" in body
    assert body.index("External reviewer notes") < body.index("<summary><b>PXD1</b>")


def test_external_note_with_untrusted_url_has_no_link(render_mod):
    notes = {"PXD1": [dict(NOTE, url="https://evil.example/x"), dict(NOTE, title="t2", url="javascript:alert(1)")]}
    body = render_mod.render(report(dataset("PXD1")), external=notes)
    assert "evil" not in body and "javascript" not in body and "[source]" not in body


def test_notes_for_unknown_datasets_are_ignored(render_mod):
    body = render_mod.render(report(dataset("PXD1")), external={"PXD999": [NOTE]})
    assert "External reviewer notes" not in body


def test_notes_survive_size_cap(render_mod):
    big = [dict(SWAP, old="x" * 100 + str(i), risk="low") for i in range(30)]
    r = report(*[dataset(f"PXDLOW{i}", risk="low", changes=big) for i in range(10)])
    body = render_mod.render(r, max_chars=12000, external={"PXDLOW9": [NOTE]})
    assert "Eight yeast datasets use animal terms" in body


def test_non_numeric_fields_are_not_rendered_raw(render_mod):
    evil = dataset("PXD1", rows={"old": "<img src=x>", "new": 3, "added": 0, "removed": 0},
                   quality={"fixed": "<b>", "introduced": None,
                            "parse_sdrf": {"base": "<i>", "head": "pass"}},
                   changes=[dict(SWAP, rows="<x>", total_rows=[1])])
    r = report(evil)
    r["summary"]["new"] = "<script>"
    body = render_mod.render(r)
    assert "<img" not in body and "<script>" not in body and "<x>" not in body and "<i>" not in body
    assert "| - → 3 | - fixed / - introduced; parse\\_sdrf &lt;i&gt; → pass |" in body
    assert "(-/- rows)" in body


def test_validate_report_rejects_bad_datasets(render_mod):
    r = report(dataset("PXD1"))
    r["datasets"].append({"id": 3, "status": "modified"})
    with pytest.raises(ValueError):
        render_mod.validate_report(r)
    r["datasets"][-1] = {"id": "PXD2", "status": "exploded"}
    with pytest.raises(ValueError):
        render_mod.validate_report(r)


def test_same_finding_on_several_datasets_is_one_line(render_mod):
    notes = {f"PXD{i}": [NOTE] for i in range(10)}
    r = report(*[dataset(f"PXD{i}") for i in range(10)])
    body = render_mod.render(r, external=notes)
    assert body.count("Eight yeast datasets use animal terms") == 1
    assert "- **PXD0, PXD1, PXD2, PXD3, PXD4, PXD5, PXD6, PXD7 and 2 more** · " in body


def test_data_check_rendered_for_single_and_grouped_notes(render_mod):
    checked = dict(NOTE, data_check="organism does not fit the declared template")
    body = render_mod.render(report(dataset("PXD1")), external={"PXD1": [checked]})
    assert "· ✓ confirmed by data: organism does not fit the declared template" in body
    notes = {"PXD1": [checked], "PXD2": [NOTE], "PXD3": [checked]}
    body = render_mod.render(report(dataset("PXD1"), dataset("PXD2"), dataset("PXD3")), external=notes)
    assert "· ✓ confirmed by data for PXD1, PXD3: organism does not fit the declared template" in body
