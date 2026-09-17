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
    assert "| PXD000001 | modified | high | 10 → 10 | 1 fixed / 0 introduced; parse_sdrf fail → pass |" in body
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
