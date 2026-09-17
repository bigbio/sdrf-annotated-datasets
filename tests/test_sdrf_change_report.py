"""Tests for the SDRF change report: semantic diff, ontology relations, risk and report building."""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

import pytest

HEADER = [
    "source name",
    "characteristics[organism]",
    "characteristics[organism part]",
    "characteristics[disease]",
    "characteristics[biological replicate]",
    "assay name",
    "comment[label]",
    "comment[data file]",
    "comment[fraction identifier]",
    "comment[technical replicate]",
    "comment[instrument]",
    "comment[modification parameters]",
    "comment[modification parameters]",
    "factor value[disease]",
]

OX = "NT=Oxidation;AC=UNIMOD:35;MT=Variable;TA=M"
CAM = "NT=Carbamidomethyl;AC=UNIMOD:4;MT=Fixed;TA=C"


def make_row(i, **over):
    values = {
        "source name": f"sample {i}",
        "characteristics[organism]": "Homo sapiens",
        "characteristics[organism part]": "liver",
        "characteristics[disease]": "normal" if i % 2 else "hepatocellular carcinoma",
        "characteristics[biological replicate]": str(i),
        "assay name": f"run {i}",
        "comment[label]": "label free sample",
        "comment[data file]": f"file_{i}.raw",
        "comment[fraction identifier]": "1",
        "comment[technical replicate]": "1",
        "comment[instrument]": "NT=Q Exactive;AC=MS:1001911",
        "mods": (OX, CAM),
        "factor value[disease]": "normal" if i % 2 else "hepatocellular carcinoma",
    }
    values.update(over)
    return values


def to_tsv(rows, header=None, drop=()):
    header = [h for h in (header or HEADER) if h not in drop]
    lines = ["\t".join(header)]
    for r in rows:
        cells, mod_i = [], 0
        for h in header:
            if h == "comment[modification parameters]":
                cells.append(r["mods"][mod_i] if mod_i < len(r["mods"]) else "")
                mod_i += 1
            else:
                cells.append(r[h])
        lines.append("\t".join(cells))
    return "\n".join(lines) + "\n"


def base_rows(n=24, **over):
    return [make_row(i, **over) for i in range(1, n + 1)]


# ---------------------------------------------------------------- diff engine


def test_identical_files_have_no_changes(report_mod):
    t = to_tsv(base_rows())
    d = report_mod.diff_tables(t, t)
    assert d["changes"] == []
    assert d["columns"] == {"added": [], "removed": []}
    assert d["rows"] == {"old": 24, "new": 24, "added": 0, "removed": 0}
    assert d["restructured"] is False


def test_organism_swap_is_grouped_across_rows(report_mod):
    old = to_tsv(base_rows())
    new = to_tsv(base_rows(**{"characteristics[organism]": "Mus musculus"}))
    d = report_mod.diff_tables(old, new)
    assert d["changes"] == [{
        "column": "characteristics[organism]", "old": "Homo sapiens", "new": "Mus musculus",
        "rows": 24, "total_rows": 24, "kind": "replaced",
    }]


def test_partial_value_change_counts_only_affected_rows(report_mod):
    old_rows = base_rows()
    new_rows = base_rows()
    for r in new_rows[:3]:
        r["characteristics[organism part]"] = "hepatocyte"
    d = report_mod.diff_tables(to_tsv(old_rows), to_tsv(new_rows))
    assert [(c["old"], c["new"], c["rows"]) for c in d["changes"]] == [("liver", "hepatocyte", 3)]


def test_key_value_formatting_is_format_only(report_mod):
    old = to_tsv(base_rows())
    new = to_tsv(base_rows(**{"comment[instrument]": "NT=q exactive; AC=MS:1001911"}))
    (c,) = report_mod.diff_tables(old, new)["changes"]
    assert c["kind"] == "format"


def test_filled_and_emptied(report_mod):
    old = to_tsv(base_rows(**{"characteristics[organism part]": "not available"}))
    new = to_tsv(base_rows())
    assert report_mod.diff_tables(old, new)["changes"][0]["kind"] == "filled"
    assert report_mod.diff_tables(new, old)["changes"][0]["kind"] == "emptied"


def test_reordered_repeated_columns_are_not_a_change(report_mod):
    old = to_tsv(base_rows())
    new = to_tsv(base_rows(mods=(CAM, OX)))
    assert report_mod.diff_tables(old, new)["changes"] == []


def test_added_modification_is_reported_as_set_change(report_mod):
    header = HEADER + ["comment[modification parameters]"]
    old = to_tsv(base_rows())
    new = to_tsv(base_rows(mods=(OX, CAM, "NT=Phospho;AC=UNIMOD:21")), header=header)
    (c,) = report_mod.diff_tables(old, new)["changes"]
    assert c["column"] == "comment[modification parameters]"
    assert c["kind"] == "replaced"
    assert "Phospho" in c["new"] and "Phospho" not in c["old"]
    assert report_mod.diff_tables(old, new)["columns"] == {"added": [], "removed": []}


def test_column_removed_and_added(report_mod):
    old = to_tsv(base_rows())
    new = to_tsv(base_rows(), drop=("characteristics[disease]",))
    d = report_mod.diff_tables(old, new)
    assert d["columns"] == {"added": [], "removed": ["characteristics[disease]"]}
    assert d["changes"] == []
    assert report_mod.diff_tables(new, old)["columns"] == {
        "added": ["characteristics[disease]"], "removed": []}


def test_rows_removed_and_data_files(report_mod):
    old = to_tsv(base_rows())
    new = to_tsv(base_rows()[:20])
    d = report_mod.diff_tables(old, new)
    assert d["rows"] == {"old": 24, "new": 20, "added": 0, "removed": 4}
    assert d["removed_data_files"] == ["file_21.raw", "file_22.raw", "file_23.raw", "file_24.raw"]
    assert d["restructured"] is False


def test_restructured_when_most_rows_unmatched(report_mod):
    old = to_tsv(base_rows())
    new_rows = base_rows()
    for i, r in enumerate(new_rows):
        if i < 20:
            r["comment[data file]"] = f"renamed_{i}.raw"
    d = report_mod.diff_tables(old, to_tsv(new_rows))
    assert d["restructured"] is True
    assert d["changes"] == []


def test_multiplexed_rows_matched_by_label(report_mod):
    rows = []
    for ch in ("TMT126", "TMT127", "TMT128"):
        rows.append(make_row(1, **{"comment[label]": ch, "comment[data file]": "plex1.raw",
                                   "source name": f"s-{ch}"}))
    new_rows = [dict(r) for r in rows]
    new_rows[2]["characteristics[organism part]"] = "kidney"
    d = report_mod.diff_tables(to_tsv(rows), to_tsv(new_rows))
    assert [(c["old"], c["new"], c["rows"]) for c in d["changes"]] == [("liver", "kidney", 1)]
    assert d["labels"] == {"old": ["TMT126", "TMT127", "TMT128"],
                           "new": ["TMT126", "TMT127", "TMT128"]}


def test_label_reformatting_does_not_break_matching(report_mod):
    old = to_tsv(base_rows(**{"comment[label]": "AC=MS:1002038;NT=label free sample"}))
    new = to_tsv(base_rows(**{"comment[label]": "NT=label free sample;AC=MS:1002038"}))
    d = report_mod.diff_tables(old, new)
    assert d["restructured"] is False and d["rows"]["removed"] == 0
    assert d["labels"]["old"] == d["labels"]["new"] == ["label free sample"]
    assert [c["kind"] for c in d["changes"]] == ["format"]


def test_label_correction_is_a_value_change(report_mod):
    old = to_tsv(base_rows(**{"comment[label]": "NT=label free"}))
    new = to_tsv(base_rows(**{"comment[label]": "NT=label free sample;AC=MS:1002038"}))
    d = report_mod.diff_tables(old, new)
    assert d["restructured"] is False and d["rows"]["removed"] == 0
    assert [(c["column"], c["rows"]) for c in d["changes"]] == [("comment[label]", 24)]


def test_peak_list_replaced_by_raw_is_matched_by_file_stem(report_mod):
    old_rows = base_rows()
    for r in old_rows:
        r["comment[data file]"] = r["comment[data file]"].replace(".raw", ".mzML")
    d = report_mod.diff_tables(to_tsv(old_rows), to_tsv(base_rows()))
    assert d["restructured"] is False
    assert d["removed_data_files"] == []
    assert d["rows"]["removed"] == 0
    assert all(c["column"] == "comment[data file]" for c in d["changes"])
    assert sum(c["rows"] for c in d["changes"]) == 24


def test_duplicate_keys_matched_in_order(report_mod):
    rows = [make_row(1), make_row(1)]
    new_rows = [make_row(1), make_row(1, **{"characteristics[disease]": "cirrhosis"})]
    d = report_mod.diff_tables(to_tsv(rows), to_tsv(new_rows))
    assert d["rows"]["removed"] == 0
    assert [(c["new"], c["rows"]) for c in d["changes"]] == [("cirrhosis", 1)]


def test_empty_file_raises(report_mod):
    with pytest.raises(ValueError):
        report_mod.diff_tables("", to_tsv(base_rows()))


# ---------------------------------------------------------------- ontology relations


class FakeOls:
    """Minimal OLS4 stand-in: terms by label, ancestors and parents by obo_id."""

    def __init__(self, terms, parents, fail=False):
        self.terms = terms  # label -> (obo_id, ontology)
        self.parents = parents  # obo_id -> [obo_id]
        self.fail = fail
        self.calls = 0

    def ancestors(self, obo):
        out, stack = set(), list(self.parents.get(obo, []))
        while stack:
            p = stack.pop()
            if p not in out:
                out.add(p)
                stack.extend(self.parents.get(p, []))
        return out

    def __call__(self, url):
        self.calls += 1
        if self.fail:
            raise OSError("OLS down")
        parsed = urlparse(url)
        if parsed.path.endswith("/search"):
            q = parse_qs(parsed.query)["q"][0]
            docs = []
            for label, (obo, onto) in self.terms.items():
                if q.lower() in (label.lower(), obo.lower()):
                    docs.append({"label": label, "obo_id": obo, "ontology_name": onto,
                                 "iri": f"http://purl.obolibrary.org/obo/{obo.replace(':', '_')}",
                                 "is_defining_ontology": True})
            return {"response": {"docs": docs}}
        obo = next(o for _, (o, _) in self.terms.items()
                   if o.replace(":", "_") in url.replace("%252F", "/").replace("%2F", "/"))
        if "hierarchicalParents" in url:
            ids = self.parents.get(obo, [])
        else:
            ids = self.ancestors(obo)
        return {"_embedded": {"terms": [{"obo_id": i} for i in ids]}}


ANATOMY = FakeOls(
    terms={
        "liver": ("UBERON:0002107", "uberon"),
        "hepatic lobule": ("UBERON:0004647", "uberon"),
        "kidney": ("UBERON:0002113", "uberon"),
        "abdominal organ": ("UBERON:0000916", "uberon"),
        "brain": ("UBERON:0000955", "uberon"),
        "Homo sapiens": ("NCBITaxon:9606", "ncbitaxon"),
        "Mus musculus": ("NCBITaxon:10090", "ncbitaxon"),
    },
    parents={
        "UBERON:0004647": ["UBERON:0002107"],
        "UBERON:0002107": ["UBERON:0000916"],
        "UBERON:0002113": ["UBERON:0000916"],
        "UBERON:0000916": ["UBERON:0000062"],
        "UBERON:0000955": ["UBERON:0000062"],
    },
)


@pytest.mark.parametrize("old,new,expected", [
    ("liver", "hepatic lobule", "refinement"),
    ("hepatic lobule", "liver", "generalisation"),
    ("liver", "kidney", "sibling"),
    ("liver", "brain", "unrelated"),
    ("liver", "no such tissue", "unknown"),
    ("liver", "NT=liver;AC=UBERON:0002107", "same"),
])
def test_relations(report_mod, old, new, expected):
    r = report_mod.OlsResolver(fetch=ANATOMY)
    assert r.relation("characteristics[organism part]", old, new) == expected


def test_relation_unknown_when_ols_fails(report_mod):
    r = report_mod.OlsResolver(fetch=FakeOls({}, {}, fail=True))
    assert r.relation("characteristics[organism part]", "liver", "kidney") == "unknown"


def test_relation_none_for_non_ontology_column(report_mod):
    r = report_mod.OlsResolver(fetch=ANATOMY)
    assert r.relation("comment[technical replicate]", "1", "2") is None


def test_budget_limits_lookups(report_mod):
    fake = FakeOls(ANATOMY.terms, ANATOMY.parents)
    r = report_mod.OlsResolver(fetch=fake, budget=1)
    assert r.relation("characteristics[organism part]", "liver", "kidney") == "sibling"
    calls = fake.calls
    assert r.relation("characteristics[organism part]", "liver", "brain") == "unknown"
    assert fake.calls == calls


def test_annotate_relations_marks_same_as_format(report_mod):
    changes = [
        {"column": "characteristics[organism part]", "old": "liver",
         "new": "NT=liver;AC=UBERON:0002107", "rows": 2, "total_rows": 2, "kind": "replaced"},
        {"column": "characteristics[organism]", "old": "Homo sapiens", "new": "Mus musculus",
         "rows": 2, "total_rows": 2, "kind": "replaced"},
        {"column": "comment[data file]", "old": "a", "new": "b", "rows": 1, "total_rows": 2,
         "kind": "replaced"},
    ]
    report_mod.annotate_relations(changes, report_mod.OlsResolver(fetch=ANATOMY))
    assert changes[0]["kind"] == "format" and changes[0]["relation"] == "same"
    assert changes[1]["relation"] == "unrelated"
    assert "relation" not in changes[2]


# ---------------------------------------------------------------- risk


def modified(**kw):
    ds = {"id": "PXD1", "status": "modified", "restructured": False,
          "rows": {"old": 10, "new": 10, "added": 0, "removed": 0},
          "columns": {"added": [], "removed": []}, "changes": [],
          "removed_data_files": [], "labels": {"old": [], "new": []}}
    ds.update(kw)
    return ds


def change(column, kind="replaced", relation=None):
    c = {"column": column, "old": "a", "new": "b", "rows": 1, "total_rows": 10, "kind": kind}
    if relation:
        c["relation"] = relation
    return c


@pytest.mark.parametrize("c,expected", [
    (change("characteristics[organism]", relation="unrelated"), "high"),
    (change("characteristics[organism]", relation="refinement"), "low"),
    (change("comment[label]"), "high"),
    (change("characteristics[organism part]", relation="sibling"), "medium"),
    (change("characteristics[disease]", relation="unknown"), "medium"),
    (change("characteristics[organism part]", relation="generalisation"), "medium"),
    (change("characteristics[cell type]", relation="refinement"), "low"),
    (change("comment[instrument]"), "medium"),
    (change("comment[technical replicate]"), "medium"),
    (change("characteristics[organism]", kind="emptied"), "medium"),
    (change("characteristics[disease]", kind="filled"), "low"),
    (change("comment[instrument]", kind="format"), "low"),
])
def test_change_risk(report_mod, c, expected):
    ds = modified(changes=[c])
    report_mod.classify(ds)
    assert c["risk"] == expected
    assert ds["risk"] == expected


@pytest.mark.parametrize("kw,expected", [
    ({"rows": {"old": 10, "new": 8, "added": 0, "removed": 2}}, "high"),
    ({"removed_data_files": ["x.raw"]}, "high"),
    ({"restructured": True}, "high"),
    ({"labels": {"old": ["TMT126"], "new": ["TMT127"]}}, "high"),
    ({"columns": {"added": [], "removed": ["factor value[disease]"]}}, "high"),
    ({"columns": {"added": [], "removed": ["characteristics[disease]"]}}, "medium"),
    ({"columns": {"added": ["characteristics[sex]"], "removed": []}}, "low"),
    ({"rows": {"old": 10, "new": 12, "added": 2, "removed": 0}}, "low"),
    ({}, "low"),
])
def test_dataset_findings_risk(report_mod, kw, expected):
    ds = modified(**kw)
    report_mod.classify(ds)
    assert ds["risk"] == expected


def test_deleted_is_high_and_new_has_no_risk(report_mod):
    d = {"id": "PXD1", "status": "deleted", "changes": []}
    n = {"id": "PXD2", "status": "new", "changes": []}
    report_mod.classify(d)
    report_mod.classify(n)
    assert d["risk"] == "high"
    assert n["risk"] is None


def test_changes_sorted_by_risk_then_rows(report_mod):
    low = change("characteristics[disease]", kind="filled")
    low["rows"] = 9
    high = change("comment[label]")
    ds = modified(changes=[low, high])
    report_mod.classify(ds)
    assert [c["risk"] for c in ds["changes"]] == ["high", "low"]


# ---------------------------------------------------------------- quality + report


def test_quality_delta_counts_fixed_and_introduced(report_mod, tmp_path):
    base = tmp_path / "base.sdrf.tsv"
    head = tmp_path / "head.sdrf.tsv"
    base.write_text(to_tsv(base_rows(**{"characteristics[disease]": "Not Available"})))
    head.write_text(to_tsv(base_rows()))
    q = report_mod.quality_delta(head, base, parse_fn=lambda p: (p == head, ""))
    assert q["fixed"] == 24 and q["introduced"] == 0
    assert q["parse_sdrf"] == {"base": "fail", "head": "pass"}


def test_quality_parse_error_is_reported(report_mod, tmp_path):
    head = tmp_path / "head.sdrf.tsv"
    head.write_text(to_tsv(base_rows()))

    def boom(_):
        raise FileNotFoundError("parse_sdrf")
    q = report_mod.quality_delta(head, None, parse_fn=boom)
    assert q["parse_sdrf"] == {"base": None, "head": "error"}


def test_main_writes_report(report_mod, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    mod_path = "datasets/PXD000001/PXD000001.sdrf.tsv"
    new_path = "datasets/PXD000002/PXD000002.sdrf.tsv"
    del_path = "datasets/PXD000003/PXD000003.sdrf.tsv"
    for p, text in [
        (mod_path, to_tsv(base_rows(**{"characteristics[organism]": "Mus musculus"}))),
        (new_path, to_tsv(base_rows(4))),
        (".base/" + mod_path, to_tsv(base_rows())),
        (".base/" + del_path, to_tsv(base_rows(6))),
    ]:
        (tmp_path / p).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / p).write_text(text)
    (tmp_path / "ns.txt").write_text(
        f"M\t{mod_path}\nA\t{new_path}\nD\t{del_path}\nM\tREADME.md\nA\tsandbox/X/X.sdrf.tsv\n")
    monkeypatch.setattr(report_mod, "default_parse", lambda p: (True, ""))
    rc = report_mod.main(["--name-status", "ns.txt", "--base-dir", ".base", "--out", "out/r.json",
                          "--pr", "42", "--head-sha", "h" * 40, "--base-sha", "b" * 40, "--no-ols"])
    assert rc == 0
    r = json.loads((tmp_path / "out/r.json").read_text())
    assert r["schema_version"] == 1 and r["pr_number"] == 42
    assert r["summary"] == {"new": 1, "modified": 1, "deleted": 1, "risk": "high"}
    by = {d["id"]: d for d in r["datasets"]}
    assert by["PXD000001"]["changes"][0]["relation"] == "unknown"
    assert by["PXD000001"]["risk"] == "high"
    assert by["PXD000002"]["rows"]["new"] == 4 and by["PXD000002"]["risk"] is None
    assert by["PXD000003"]["rows"]["old"] == 6 and by["PXD000003"]["quality"] is None


def test_new_datasets_skip_parse_sdrf(report_mod, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = "datasets/PXD000002/PXD000002.sdrf.tsv"
    (tmp_path / path).parent.mkdir(parents=True)
    (tmp_path / path).write_text(to_tsv(base_rows(3)))
    calls = []
    monkeypatch.setattr(report_mod, "default_parse", lambda p: calls.append(p) or (True, ""))
    ds = report_mod.build_dataset("new", path, tmp_path / ".base", None)
    assert calls == []
    assert ds["quality"]["parse_sdrf"] == {"base": None, "head": None}


def test_main_without_sdrf_changes_writes_nothing(report_mod, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "ns.txt").write_text("M\tREADME.md\n")
    rc = report_mod.main(["--name-status", "ns.txt", "--base-dir", ".base", "--out", "r.json",
                          "--pr", "1", "--head-sha", "h", "--base-sha", "b", "--no-ols"])
    assert rc == 0
    assert not (tmp_path / "r.json").exists()
