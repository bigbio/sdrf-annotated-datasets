"""Tests for the SDRF review gate in .github/scripts/sdrf_review.py.

Every dataset PR in this repository is judged by this script, and until now a change to it
ran nothing: both dataset workflows are path-filtered to `datasets/**`, so a PR touching only
`.github/scripts/` triggered no checks at all.

The cases below pin the behaviour the gate is relied on for, including the two things that
are easy to break silently: the advisory/blocking split, and the `--baseline` subtraction that
decides whether a pre-existing defect blocks an unrelated change.
"""

from __future__ import annotations

import pytest

BASE_HEADER = [
    "source name",
    "characteristics[organism]",
    "characteristics[organism part]",
    "characteristics[disease]",
    "characteristics[biological replicate]",
    "assay name",
    "technology type",
    "comment[label]",
    "comment[instrument]",
    "comment[cleavage agent details]",
    "comment[technical replicate]",
    "comment[fraction identifier]",
    "comment[data file]",
    "comment[sdrf template]",
    "factor value[disease]",
]


def row(src="PXD000001-Sample-1", organism="Homo sapiens", part="heart", disease="normal",
        bio="1", assay="r1", label="NT=label free sample;AC=MS:1002038",
        instrument="NT=Q Exactive;AC=MS:1001911", tech="1", frac="1", data="r1.raw",
        template="NT=ms-proteomics;VV=v1.1.0", factor="normal"):
    return [src, organism, part, disease, bio, assay,
            "proteomic profiling by mass spectrometry", label, instrument,
            "NT=Trypsin;AC=MS:1001251", tech, frac, data, template, factor]


class TestStructuralCheck:
    def test_clean_file_has_no_defects(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(assay="r1", data="r1.raw"),
                                     row(src="PXD000001-Sample-2", assay="r2", data="r2.raw")])
        assert gate.structural_check(str(p)) == (0, 0)

    def test_ragged_row_is_counted(self, gate, write_sdrf):
        good = row()
        p = write_sdrf(BASE_HEADER, [good, good[:-2]])
        ragged, _ = gate.structural_check(str(p))
        assert ragged == 1

    def test_coordinate_collision_is_counted(self, gate, write_sdrf):
        # identical (source, bio rep, tech rep, fraction, label); only the file name differs,
        # and comment[data file] is explicitly not an explainer
        p = write_sdrf(BASE_HEADER, [row(assay="r1", data="r1.raw"),
                                     row(assay="r2", data="r2.raw")])
        _, collisions = gate.structural_check(str(p))
        assert collisions == 1

    def test_label_channels_are_not_a_collision(self, gate, write_sdrf):
        """Multiplexed data legitimately repeats a coordinate once per label channel."""
        p = write_sdrf(BASE_HEADER, [
            row(label="NT=TMT126;AC=MS:1002623", data="mix.raw"),
            row(label="NT=TMT127N;AC=MS:1002624", data="mix.raw"),
        ])
        assert gate.structural_check(str(p))[1] == 0

    def test_a_descriptive_column_explains_a_repeated_coordinate(self, gate, write_sdrf):
        """A second design axis carried in another column is annotation, not collision."""
        p = write_sdrf(BASE_HEADER, [
            row(part="heart", assay="r1", data="r1.raw"),
            row(part="liver", assay="r2", data="r2.raw"),
        ])
        assert gate.structural_check(str(p))[1] == 0

    def test_empty_file_is_safe(self, gate, tmp_path):
        p = tmp_path / "empty.sdrf.tsv"
        p.write_text("", encoding="utf-8")
        assert gate.structural_check(str(p)) == (0, 0)


class TestContentCheck:
    def test_clean_file_reports_nothing(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(assay="r1", data="r1.raw"),
                                     row(src="PXD000001-Sample-2", assay="r2", data="r2.raw")])
        assert gate.content_check(str(p)) == {}

    def test_reserved_word_must_be_lowercase(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(disease="Not Available", factor="Not Available")])
        assert gate.content_check(str(p))["reserved_word_case"] >= 1

    def test_characteristics_take_a_bare_label(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(part="NT=heart;AC=UBERON:0000948")])
        assert gate.content_check(str(p))["characteristics_not_bare_label"] == 1

    def test_pandas_artifact_header_is_detected(self, gate, write_sdrf):
        header = list(BASE_HEADER)
        header[13] = "comment[sdrf template].1"
        p = write_sdrf(header, [row()])
        assert gate.content_check(str(p))["artifact_headers"] == 1

    def test_peak_list_data_file_is_advisory(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(data="r1.mzML")])
        found = gate.content_check(str(p))
        assert found["peak_list_data_file"] == 1
        assert "peak_list_data_file" in gate.ADVISORY

    def test_missing_factor_value_is_advisory(self, gate, write_sdrf):
        header = BASE_HEADER[:-1]
        p = write_sdrf(header, [row()[:-1]])
        found = gate.content_check(str(p))
        assert found["no_factor_value"] == 1
        assert "no_factor_value" in gate.ADVISORY

    def test_all_sentinel_factor_is_hollow_and_blocks(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(factor="not available"),
                                     row(src="PXD000001-Sample-2", assay="r2",
                                         data="r2.raw", factor="not available")])
        found = gate.content_check(str(p))
        assert found["hollow_factor_value"] == 1
        assert "hollow_factor_value" not in gate.ADVISORY

    def test_a_constant_real_factor_is_not_hollow(self, gate, write_sdrf):
        """A single-condition study has no contrast; the corpus norm is a constant value."""
        p = write_sdrf(BASE_HEADER, [row(factor="dilated cardiomyopathy"),
                                     row(src="PXD000001-Sample-2", assay="r2",
                                         data="r2.raw", factor="dilated cardiomyopathy")])
        assert "hollow_factor_value" not in gate.content_check(str(p))


class TestInstrumentVendorCheck:
    """A vendor's acquisition software writes its own container format."""

    @pytest.mark.parametrize("instrument,files,expected", [
        ("Q Exactive", ["a.d.zip", "b.d.zip"], 2),        # Thermo model, Bruker files
        ("timsTOF Pro", ["a.raw"], 1),                     # Bruker model, Thermo file
        ("Q Exactive", ["a.raw", "b.raw"], 0),
        ("timsTOF Pro", ["a.d.zip"], 0),
        ("Q Exactive", ["a.mzML"], 0),                     # converted, vendor-neutral
        ("Some Unlisted Analyzer", ["a.d"], 0),            # unrecognised model: silent
    ])
    def test_vendor_and_format(self, gate, instrument, files, expected):
        assert gate.instrument_vendor_check({instrument}, files) == expected

    def test_several_instruments_any_may_match(self, gate):
        assert gate.instrument_vendor_check({"Q Exactive", "timsTOF Pro"},
                                            ["a.raw", "b.d.zip"]) == 0

    def test_no_files_is_silent(self, gate):
        assert gate.instrument_vendor_check({"Q Exactive"}, []) == 0

    def test_reported_through_content_check(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(instrument="NT=Q Exactive;AC=MS:1001911",
                                         data="a.d.zip")])
        assert gate.content_check(str(p))["instrument_cannot_write_data_file"] == 1


class TestDeclaredTemplates:
    def test_parameter_spelling(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(template="NT=ms-proteomics;VV=v1.1.0")])
        assert gate.declared_templates(str(p)) == ["ms-proteomics"]

    def test_plain_spelling(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(template="ms-proteomics v1.1.0")])
        assert gate.declared_templates(str(p)) == ["ms-proteomics"]

    def test_repeated_column_collects_every_template(self, gate, write_sdrf):
        """A DIA file declares two templates in two columns of the same name.

        A plain csv.DictReader would keep only the last, so the gate reads raw indices.
        """
        header = list(BASE_HEADER) + ["comment[sdrf template]"]
        p = write_sdrf(header, [row() + ["NT=dia-acquisition;VV=v1.1.0"]])
        assert gate.declared_templates(str(p)) == ["ms-proteomics", "dia-acquisition"]

    def test_sentinel_is_not_a_template(self, gate, write_sdrf):
        p = write_sdrf(BASE_HEADER, [row(template="not available")])
        assert gate.declared_templates(str(p)) == []

    def test_no_column_returns_empty(self, gate, write_sdrf):
        header = [c for c in BASE_HEADER if c != "comment[sdrf template]"]
        r = [v for c, v in zip(BASE_HEADER, row()) if c != "comment[sdrf template]"]
        p = write_sdrf(header, [r])
        assert gate.declared_templates(str(p)) == []


class TestBaselinePath:
    def test_relative_path_resolves_inside_the_baseline(self, gate):
        got = gate._baseline_path("/base", "datasets/PXD1/PXD1.sdrf.tsv")
        assert str(got) == "/base/datasets/PXD1/PXD1.sdrf.tsv"

    def test_absolute_path_does_not_escape_the_baseline(self, gate):
        """Path('/base') / '/abs' returns '/abs', which would make the baseline the file
        itself and silently disable every check."""
        got = gate._baseline_path("/base", "/abs/datasets/PXD1/PXD1.sdrf.tsv")
        assert str(got).startswith("/base/")


class TestBaselineSubtraction:
    """The mechanism that decides whether a pre-existing defect blocks an unrelated change.

    Nothing else exercises it, and every new gate rule depends on it behaving this way.
    """

    def _counts(self, gate, before, after):
        base = gate.content_check(str(before))
        head = gate.content_check(str(after))
        return {k: v - base.get(k, 0) for k, v in head.items() if v - base.get(k, 0) > 0}

    def test_unchanged_pre_existing_defect_is_not_new(self, gate, write_sdrf, tmp_path):
        bad = [row(part="NT=heart;AC=UBERON:0000948")]
        before = write_sdrf(BASE_HEADER, bad, root=tmp_path / "base")
        after = write_sdrf(BASE_HEADER, bad, root=tmp_path / "head")
        assert self._counts(gate, before, after) == {}

    def test_an_increase_is_reported(self, gate, write_sdrf, tmp_path):
        before = write_sdrf(BASE_HEADER, [row(part="NT=heart;AC=UBERON:0000948")],
                            root=tmp_path / "base")
        after = write_sdrf(BASE_HEADER, [row(part="NT=heart;AC=UBERON:0000948"),
                                         row(src="PXD000001-Sample-2", assay="r2", data="r2.raw",
                                             part="NT=liver;AC=UBERON:0002107")],
                           root=tmp_path / "head")
        assert self._counts(gate, before, after)["characteristics_not_bare_label"] == 1

    def test_a_fix_is_not_reported_as_a_defect(self, gate, write_sdrf, tmp_path):
        before = write_sdrf(BASE_HEADER, [row(part="NT=heart;AC=UBERON:0000948")],
                            root=tmp_path / "base")
        after = write_sdrf(BASE_HEADER, [row(part="heart")], root=tmp_path / "head")
        assert self._counts(gate, before, after) == {}
