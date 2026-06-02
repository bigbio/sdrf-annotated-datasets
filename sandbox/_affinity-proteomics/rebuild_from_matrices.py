#!/usr/bin/env python3
"""Rebuild affinity-proteomics SDRF drafts from deposited NPX/ADAT matrices."""

from __future__ import annotations

import csv
import io
import itertools
import json
import re
import sys
import urllib.request
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, "/private/tmp/affinity_pyarrow")

try:
    import pyarrow.parquet as pq
except Exception as exc:  # pragma: no cover - this is an environment guard.
    raise SystemExit(
        "pyarrow is required for Olink parquet matrices; install it or set PYTHONPATH."
    ) from exc


REPO = Path(__file__).resolve().parents[2]
CAMPAIGN = REPO / "sandbox" / "_affinity-proteomics"
CACHE = Path("/private/tmp/affinity-data-cache")
CACHE.mkdir(parents=True, exist_ok=True)

NA = "not available"
VALID_OLINK_PLATFORMS = {
    "Olink Target 96",
    "Olink Explore 384",
    "Olink Explore HT",
    "Olink Reveal",
}
VALID_SOMASCAN_MENUS = {
    "SomaScan 1.1K",
    "SomaScan 1.3K",
    "SomaScan 5K",
    "SomaScan 7K",
    "SomaScan 11K",
}

COMMON_COLUMNS = [
    "source name",
    "characteristics[organism]",
    "characteristics[organism part]",
    "characteristics[disease]",
    "characteristics[age]",
    "characteristics[sex]",
    "characteristics[developmental stage]",
    "characteristics[individual]",
    "characteristics[ancestry category]",
    "characteristics[cell type]",
    "characteristics[biological replicate]",
    "characteristics[pooled sample]",
    "characteristics[sample type]",
    "characteristics[sample matrix]",
    "assay name",
    "technology type",
    "comment[technical replicate]",
    "comment[data file]",
    "comment[file uri]",
    "comment[platform]",
    "comment[instrument]",
    "comment[panel version]",
    "comment[quantification unit]",
    "comment[plate]",
    "comment[normalization method]",
]

OLINK_COLUMNS = COMMON_COLUMNS + [
    "comment[olink panel]",
    "comment[olink platform]",
    "comment[npx normalization]",
    "comment[olink lot number]",
    "comment[sdrf version]",
    "comment[sdrf annotation tool]",
]

SOMASCAN_COLUMNS = COMMON_COLUMNS + [
    "comment[somascan menu]",
    "comment[somascan platform]",
    "comment[dilution]",
    "comment[somascan lot number]",
    "comment[sdrf version]",
    "comment[sdrf annotation tool]",
]

REQUIRED_COLUMNS = {
    "source name",
    "characteristics[organism]",
    "characteristics[organism part]",
    "characteristics[disease]",
    "characteristics[age]",
    "characteristics[sex]",
    "characteristics[biological replicate]",
    "assay name",
    "technology type",
    "comment[technical replicate]",
    "comment[data file]",
    "comment[platform]",
    "comment[olink panel]",
    "comment[olink platform]",
    "comment[somascan menu]",
    "comment[somascan platform]",
}

ALWAYS_KEEP_COLUMNS = REQUIRED_COLUMNS | {
    "characteristics[sample type]",
}


def clean(value: object) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r", "").replace("\n", " ").strip()
    if text in {"", "None", "nan", "NaN", "NA", "N/A"}:
        return ""
    return re.sub(r"\s+", " ", text)


def display_or_na(value: object) -> str:
    return clean(value) or NA


def normalize_lower(value: object) -> str:
    return clean(value).lower()


def slug(value: object, fallback: str) -> str:
    text = clean(value) or fallback
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._-")
    return (text[:80] or fallback)


def identifier(value: object) -> str:
    text = clean(value)
    if not text:
        return NA
    text = re.sub(r"\s*-\s*", "-", text)
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._-")
    return text or NA


def source_identifier(accession: str, sample_id: object) -> str:
    return f"{accession}-{slug(sample_id, 'sample')}"


def assay_identifier(accession: str, assay_index: int, sample_id: object) -> str:
    return f"{accession}-r{assay_index:05d}-{slug(sample_id, 'sample')}"


def first_present(row: dict[str, object], names: list[str]) -> str:
    for name in names:
        if name in row:
            value = clean(row.get(name))
            if value:
                return value
    lower = {str(k).lower(): k for k in row}
    for name in names:
        key = lower.get(name.lower())
        if key:
            value = clean(row.get(key))
            if value:
                return value
    return ""


def detect_delimiter(header_line: str) -> str:
    candidates = [",", ";", "\t"]
    return max(
        candidates,
        key=lambda delimiter: len(next(csv.reader([header_line], delimiter=delimiter))),
    )


def load_manifest() -> list[dict[str, str]]:
    with (CAMPAIGN / "manifest.tsv").open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_current_sdrf_files(row: dict[str, str]) -> list[dict[str, str]]:
    path = REPO / row["sdrf_path"]
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        seen: OrderedDict[str, dict[str, str]] = OrderedDict()
        for record in reader:
            name = record["comment[data file]"]
            if name not in seen:
                seen[name] = dict(record)
        return list(seen.values())


def split_semicolon(value: str) -> list[str]:
    return [item for item in (clean(value).split(";") if clean(value) else []) if item]


def is_primary_matrix(platform_family: str, filename: str, all_files: list[str]) -> bool:
    lower = filename.lower()
    if platform_family == "olink":
        preferred_exists = any(
            ("npx" in item.lower() or item.lower().endswith(".parquet"))
            for item in all_files
        )
        if preferred_exists:
            return "npx" in lower or lower.endswith(".parquet")
        return lower.endswith((".csv", ".tsv", ".parquet"))

    if platform_family == "somascan":
        adat_exists = any(item.lower().endswith(".adat") for item in all_files)
        if adat_exists:
            return lower.endswith(".adat")
        return lower.endswith((".adat", ".csv", ".tsv"))

    return True


def download_to_cache(uri: str, filename: str) -> Path:
    target = CACHE / filename
    if target.exists() and target.stat().st_size > 0:
        return target
    with urllib.request.urlopen(uri, timeout=600) as response, target.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
    return target


def merge_sample(
    samples: OrderedDict[str, dict[str, object]],
    key: str,
    values: dict[str, object],
) -> None:
    if key not in samples:
        values = dict(values)
        values["panels"] = set([clean(values.get("panel"))]) if clean(values.get("panel")) else set()
        samples[key] = values
        return

    existing = samples[key]
    panel = clean(values.get("panel"))
    if panel:
        existing.setdefault("panels", set()).add(panel)
    for name, value in values.items():
        if name == "panel":
            continue
        if not clean(existing.get(name)) and clean(value):
            existing[name] = clean(value)


def parse_npx_csv(uri: str, filename: str) -> tuple[list[dict[str, object]], dict[str, object]]:
    samples: OrderedDict[str, dict[str, object]] = OrderedDict()
    row_count = 0
    with urllib.request.urlopen(uri, timeout=600) as raw:
        text = io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="")
        first_line = text.readline()
        delimiter = detect_delimiter(first_line)
        reader = csv.DictReader(itertools.chain([first_line], text), delimiter=delimiter)
        headers = reader.fieldnames or []
        sample_col = next(
            (
                col
                for col in headers
                if col.lower().replace("_", "").replace(" ", "")
                in {"sampleid", "sampleidentifier"}
            ),
            "",
        )
        if not sample_col:
            return [], {"headers": headers, "delimiter": delimiter, "rows_read": 0}

        for record in reader:
            row_count += 1
            sample_id = clean(record.get(sample_col))
            if not sample_id:
                continue
            merge_sample(
                samples,
                sample_id,
                {
                    "sample_id": sample_id,
                    "plate": first_present(record, ["PlateID", "PlateId", "Plate", "RunID"]),
                    "panel": first_present(record, ["Panel", "PanelName", "AssayPanel"]),
                    "sample_type_raw": first_present(
                        record, ["SampleType", "Sample_Type", "Sample Type", "Group"]
                    ),
                    "sample_matrix": first_present(
                        record, ["SampleMatrix", "Sample_Matrix", "Matrix"]
                    ),
                    "normalization": first_present(
                        record, ["Normalization", "NormalizationMethod", "NPXNormalization"]
                    ),
                    "well": first_present(record, ["WellID", "WellId", "Well", "PlatePosition"]),
                    "lot": first_present(record, ["Panel_Lot_Nr", "PanelLotNr", "Lot"]),
                    "source_kind": "npx",
                },
            )

    return finalize_panel_sets(samples), {
        "headers": headers,
        "delimiter": delimiter,
        "rows_read": row_count,
    }


def parse_npx_parquet(uri: str, filename: str) -> tuple[list[dict[str, object]], dict[str, object]]:
    path = download_to_cache(uri, filename)
    parquet = pq.ParquetFile(path)
    headers = parquet.schema_arrow.names
    sample_col = next(
        (
            col
            for col in headers
            if col.lower().replace("_", "").replace(" ", "")
            in {"sampleid", "sampleidentifier"}
        ),
        "",
    )
    if not sample_col:
        return [], {"headers": headers, "rows_read": 0, "cached_path": str(path)}

    wanted = [
        sample_col,
        "PlateID",
        "PlateId",
        "Panel",
        "SampleType",
        "Sample_Type",
        "SampleMatrix",
        "Normalization",
        "WellID",
        "WellId",
        "Panel_Lot_Nr",
    ]
    columns = [col for col in OrderedDict.fromkeys(wanted) if col in headers]
    samples: OrderedDict[str, dict[str, object]] = OrderedDict()
    row_count = 0
    for batch in parquet.iter_batches(columns=columns, batch_size=100_000):
        data = batch.to_pydict()
        batch_len = len(data[sample_col])
        row_count += batch_len
        for i in range(batch_len):
            record = {col: data[col][i] for col in columns}
            sample_id = clean(record.get(sample_col))
            if not sample_id:
                continue
            merge_sample(
                samples,
                sample_id,
                {
                    "sample_id": sample_id,
                    "plate": first_present(record, ["PlateID", "PlateId", "Plate"]),
                    "panel": first_present(record, ["Panel", "PanelName"]),
                    "sample_type_raw": first_present(
                        record, ["SampleType", "Sample_Type", "Sample Type"]
                    ),
                    "sample_matrix": first_present(record, ["SampleMatrix", "Matrix"]),
                    "normalization": first_present(record, ["Normalization"]),
                    "well": first_present(record, ["WellID", "WellId", "Well"]),
                    "lot": first_present(record, ["Panel_Lot_Nr"]),
                    "source_kind": "parquet",
                },
            )

    return finalize_panel_sets(samples), {
        "headers": headers,
        "rows_read": row_count,
        "cached_path": str(path),
    }


def finalize_panel_sets(samples: OrderedDict[str, dict[str, object]]) -> list[dict[str, object]]:
    finalized = []
    for sample in samples.values():
        panels = sorted(clean(panel) for panel in sample.get("panels", set()) if clean(panel))
        if len(panels) == 1:
            sample["panel"] = panels[0]
        elif len(panels) > 1:
            sample["panel"] = "; ".join(panels[:8])
        else:
            sample["panel"] = clean(sample.get("panel"))
        sample.pop("panels", None)
        finalized.append(sample)
    return finalized


def parse_adat(uri: str) -> tuple[list[dict[str, object]], dict[str, object]]:
    samples: list[dict[str, object]] = []
    assay_version = ""
    process_steps = ""
    header: list[str] | None = None
    in_table = False

    with urllib.request.urlopen(uri, timeout=900) as raw:
        for raw_line in raw:
            line = raw_line.decode("utf-8", "replace").rstrip("\n\r")
            if line.startswith("!AssayVersion"):
                parts = line.split("\t")
                assay_version = clean(parts[1] if len(parts) > 1 else "")
            elif line.startswith("!ProcessSteps"):
                parts = line.split("\t")
                process_steps = clean(parts[1] if len(parts) > 1 else "")

            if line.startswith("^TABLE_BEGIN"):
                in_table = True
                continue
            if not in_table:
                continue

            parts = line.split("\t")
            if header is None:
                if parts and parts[0] == "PlateId" and "SampleId" in parts:
                    header = parts
                continue

            if not parts or parts[0].startswith("^"):
                continue
            if len(parts) < len(header):
                continue

            record = {name: parts[idx] for idx, name in enumerate(header) if idx < len(parts)}
            sample_id = clean(record.get("SampleId"))
            if not sample_id:
                continue
            samples.append(
                {
                    "sample_id": sample_id,
                    "plate": clean(record.get("PlateId")),
                    "well": clean(record.get("PlatePosition")),
                    "subarray": clean(record.get("Subarray")),
                    "sample_type_raw": clean(record.get("SampleType")),
                    "sample_matrix": clean(record.get("SampleMatrix")),
                    "subject_id": clean(record.get("SubjectID")),
                    "cli": clean(record.get("CLI")),
                    "percent_dilution": clean(record.get("PercentDilution")),
                    "normalization": process_steps,
                    "source_kind": "adat",
                }
            )

    return samples, {
        "headers": header or [],
        "rows_read": len(samples),
        "assay_version": assay_version,
        "process_steps": process_steps,
    }


def normalize_sample_type(raw: object) -> str:
    text = normalize_lower(raw)
    if not text:
        return "not applicable"
    if "negative" in text and "control" in text:
        return "negative control"
    if "positive" in text and "control" in text:
        return "positive control"
    if "plate" in text and "control" in text:
        return "plate control"
    if "buffer" in text and "control" in text:
        return "buffer control"
    if "qc" in text or "quality" in text:
        return "quality control sample"
    if "calibrator" in text or "calibration" in text:
        return "calibrator"
    if "control" in text:
        return "quality control sample"
    if text in {"sample", "samp", "s", "sample_control", "sample control", "sample type"}:
        return "not applicable"
    return "not applicable"


def normalize_matrix(value: object, fallback: str) -> str:
    text = normalize_lower(value)
    if "serum" in text:
        return "blood serum"
    if "plasma" in text or "plasmapheresis" in text:
        return "blood plasma"
    if "cerebrospinal" in text or text == "csf":
        return "cerebrospinal fluid"
    if "blood" in text:
        return "blood"
    fallback = normalize_lower(fallback)
    return fallback or NA


def normalize_npx_method(value: object) -> str:
    text = normalize_lower(value)
    if not text:
        return NA
    if "bridge" in text:
        return "bridge normalized"
    if "plate" in text or "ipc" in text:
        return "plate control normalized"
    if "intensity" in text:
        return "intensity normalized"
    if "not" in text and "norm" in text:
        return "not normalized"
    return NA


def normalize_dilution(value: object) -> str:
    text = normalize_lower(value).replace("percent", "").replace(" ", "")
    text = text[:-1] if text.endswith("%") else text
    if text in {"0.005", ".005"}:
        return "0.005%"
    if text in {"0.5", ".5"}:
        return "0.5%"
    if text in {"20", "20.0"}:
        return "20%"
    if text in {"40", "40.0"}:
        return "40%"
    return NA


def infer_olink_platform(
    filename: str,
    title: str,
    current_platform: str,
    current_olink_platform: str,
    panels: list[str],
) -> str:
    current = clean(current_olink_platform) or clean(current_platform)
    text = " ".join([filename, title, *panels]).lower()
    if re.search(r"\bolink reveal\b|\breveal\b", text):
        return "Olink Reveal"
    if any(
        token in text
        for token in [
            "target 96",
            "organ damage",
            "inflammation",
            "cardiometabolic",
            "neurology",
            "immuno-oncology",
            "oncology",
        ]
    ):
        return "Olink Target 96"
    if "explore" in text or "explore_ht" in text or "3072" in text or "1536" in text:
        return "Olink Explore HT"
    if current in VALID_OLINK_PLATFORMS:
        return current
    return "Olink Explore HT"


def normalize_olink_panel(value: object, platform: str, fallback: str) -> str:
    text = clean(value)
    fallback = clean(fallback)
    if not text:
        return fallback if fallback and "not reported" not in fallback.lower() else platform
    lower = text.lower()
    if lower in {"explore_ht", "explore ht", "explore"}:
        return "Olink Explore HT"
    if lower == "reveal":
        return "Olink Reveal"
    if lower == "inflammation":
        return "Olink Target 96 Inflammation"
    if lower in {"cardiometabolic_ii", "cardiometabolic ii"}:
        return "Olink Target 96 Cardiometabolic II"
    if lower in {"neurology_ii", "neurology ii"}:
        return "Olink Target 96 Neurology II"
    if lower == "oncology" and platform == "Olink Target 96":
        return "Olink Target 96 Oncology"
    return text


def infer_somascan_menu(filename: str, current_menu: str, header_len: int, assay_version: str) -> str:
    current = clean(current_menu)
    text = " ".join([filename, current, assay_version]).lower()
    if "11k" in text or "v5" in text or header_len > 10_000:
        return "SomaScan 11K"
    if "7k" in text or header_len > 7_000:
        return "SomaScan 7K"
    if "5k" in text or header_len > 4_000:
        return "SomaScan 5K"
    if "1.3k" in text or header_len > 1_200:
        return "SomaScan 1.3K"
    if current in VALID_SOMASCAN_MENUS:
        return current
    return "SomaScan 7K"


def infer_somascan_platform(assay_version: str, current_platform: str) -> str:
    text = normalize_lower(assay_version)
    current = clean(current_platform)
    if "v4.1" in text:
        return "SomaScan Assay v4.1"
    if re.search(r"\bv4\b", text):
        return "SomaScan Assay v4"
    if current in {"SomaScan Assay", "SomaScan Assay v4", "SomaScan Assay v4.1"}:
        return current
    return "SomaScan Assay"


def write_sdrf(path: Path, header: list[str], rows: list[list[str]]) -> None:
    header, rows, _removed = prune_all_unavailable_optional_columns(header, rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def prune_all_unavailable_optional_columns(
    header: list[str], rows: list[list[str]]
) -> tuple[list[str], list[list[str]], list[str]]:
    keep_indexes: list[int] = []
    removed: list[str] = []
    for idx, column in enumerate(header):
        if column in ALWAYS_KEEP_COLUMNS:
            keep_indexes.append(idx)
            continue
        values = [clean(row[idx]).lower() for row in rows]
        if values and all(value in {NA, "not applicable"} for value in values):
            removed.append(column)
        else:
            keep_indexes.append(idx)
    pruned_header = [header[idx] for idx in keep_indexes]
    pruned_rows = [[row[idx] for idx in keep_indexes] for row in rows]
    return pruned_header, pruned_rows, removed


def row_templates(platform_family: str) -> list[str]:
    return []


def build_common_values(
    accession: str,
    manifest_row: dict[str, str],
    file_row: dict[str, str],
    assay_index: int,
    sample: dict[str, object],
    biological_replicate: int,
    technical_replicate: int,
    platform: str,
    panel_name: str,
    panel_version: str,
    quantification_unit: str,
    technology_type: str,
) -> list[str]:
    sample_id = clean(sample.get("sample_id")) or f"sample-{biological_replicate}"
    source_name = source_identifier(accession, sample_id)
    assay_name = assay_identifier(accession, assay_index, sample_id)
    individual = identifier(clean(sample.get("subject_id")) or clean(sample.get("cli")))
    return [
        source_name,
        "Homo sapiens",
        display_or_na(manifest_row.get("organism_part")),
        display_or_na(manifest_row.get("disease")),
        NA,
        NA,
        NA,
        individual,
        NA,
        NA,
        str(biological_replicate),
        NA,
        normalize_sample_type(sample.get("sample_type_raw")),
        normalize_matrix(sample.get("sample_matrix"), manifest_row.get("sample_matrix", "")),
        assay_name,
        technology_type,
        str(technical_replicate),
        file_row["comment[data file]"],
        file_row["comment[file uri]"],
        platform,
        NA,
        panel_version or NA,
        quantification_unit,
        display_or_na(sample.get("plate")),
        display_or_na(sample.get("normalization")),
    ]


def rebuild() -> None:
    manifest_rows = load_manifest()
    inspection: list[dict[str, object]] = []
    updated_manifest: list[dict[str, str]] = []
    autoresearch_rows: list[dict[str, str]] = []

    for manifest_row in manifest_rows:
        accession = manifest_row["accession"]
        platform_family = manifest_row["platform_family"]
        current_file_rows = load_current_sdrf_files(manifest_row)
        filenames = (
            split_semicolon(manifest_row.get("data_files", ""))
            or split_semicolon(manifest_row.get("primary_matrices", ""))
            + split_semicolon(manifest_row.get("skipped_secondary_files", ""))
            or [row["comment[data file]"] for row in current_file_rows]
        )
        primary_file_rows = [
            row
            for row in current_file_rows
            if is_primary_matrix(platform_family, row["comment[data file]"], filenames)
        ]
        skipped = [name for name in filenames if name not in {row["comment[data file]"] for row in primary_file_rows}]

        sdrf_rows: list[list[str]] = []
        all_panels_or_menus: list[str] = []
        source_replicates: OrderedDict[str, int] = OrderedDict()
        assay_index = 0

        for file_index, file_row in enumerate(primary_file_rows, start=1):
            filename = file_row["comment[data file]"]
            uri = file_row["comment[file uri]"]
            lower = filename.lower()
            if platform_family == "olink":
                if lower.endswith(".parquet"):
                    samples, meta = parse_npx_parquet(uri, filename)
                else:
                    samples, meta = parse_npx_csv(uri, filename)
                panels = [clean(sample.get("panel")) for sample in samples if clean(sample.get("panel"))]
                platform = infer_olink_platform(
                    filename,
                    manifest_row.get("title", ""),
                    file_row.get("comment[platform]", ""),
                    file_row.get("comment[olink platform]", ""),
                    panels,
                )
                tech_reps: Counter[str] = Counter()
                for sample in samples:
                    sample_id = clean(sample.get("sample_id"))
                    source_name = source_identifier(accession, sample_id)
                    if source_name not in source_replicates:
                        source_replicates[source_name] = len(source_replicates) + 1
                    assay_index += 1
                    tech_reps[sample_id] += 1
                    panel_name = normalize_olink_panel(
                        sample.get("panel"),
                        platform,
                        file_row.get("comment[panel name]", ""),
                    )
                    all_panels_or_menus.append(panel_name)
                    row = build_common_values(
                        accession,
                        manifest_row,
                        file_row,
                        assay_index,
                        sample,
                        source_replicates[source_name],
                        tech_reps[sample_id],
                        platform,
                        panel_name,
                        NA,
                        "NPX",
                        "protein expression profiling by antibody array",
                    )
                    row += [
                        panel_name,
                        platform,
                        normalize_npx_method(sample.get("normalization")),
                        display_or_na(sample.get("lot")),
                        "v1.1.0",
                        "NT=sdrf-skills-autoresearch;VV=v0.0.0",
                    ]
                    sdrf_rows.append(row)

            elif platform_family == "somascan":
                samples, meta = parse_adat(uri)
                menu = infer_somascan_menu(
                    filename,
                    file_row.get("comment[somascan menu]", ""),
                    len(meta.get("headers", [])),
                    clean(meta.get("assay_version")),
                )
                platform = "SomaScan Assay"
                somascan_platform = infer_somascan_platform(
                    clean(meta.get("assay_version")),
                    file_row.get("comment[somascan platform]", ""),
                )
                all_panels_or_menus.append(menu)
                tech_reps: Counter[str] = Counter()
                for sample in samples:
                    sample_id = clean(sample.get("sample_id"))
                    source_name = source_identifier(accession, sample_id)
                    if source_name not in source_replicates:
                        source_replicates[source_name] = len(source_replicates) + 1
                    assay_index += 1
                    tech_reps[sample_id] += 1
                    row = build_common_values(
                        accession,
                        manifest_row,
                        file_row,
                        assay_index,
                        sample,
                        source_replicates[source_name],
                        tech_reps[sample_id],
                        platform,
                        menu,
                        clean(meta.get("assay_version")) or NA,
                        "RFU",
                        "protein expression profiling by aptamer array",
                    )
                    row += [
                        menu,
                        somascan_platform,
                        normalize_dilution(sample.get("percent_dilution")),
                        NA,
                        "v1.1.0",
                        "NT=sdrf-skills-autoresearch;VV=v0.0.0",
                    ]
                    sdrf_rows.append(row)
            else:
                samples, meta = [], {}

            inspection.append(
                {
                    "accession": accession,
                    "file": filename,
                    "file_uri": uri,
                    "platform_family": platform_family,
                    "primary_matrix": True,
                    "sample_count": len(samples),
                    "rows_read": meta.get("rows_read", len(samples)),
                    "columns": meta.get("headers", [])[:80],
                    "assay_version": meta.get("assay_version", ""),
                    "delimiter": meta.get("delimiter", ""),
                    "first_samples": samples[:5],
                }
            )

        for name in skipped:
            inspection.append(
                {
                    "accession": accession,
                    "file": name,
                    "platform_family": platform_family,
                    "primary_matrix": False,
                    "sample_count": 0,
                    "skip_reason": "secondary wide matrix skipped because a primary NPX/ADAT matrix was available",
                }
            )

        header = OLINK_COLUMNS if platform_family == "olink" else SOMASCAN_COLUMNS
        sdrf_path = REPO / manifest_row["sdrf_path"]
        write_sdrf(sdrf_path, header, sdrf_rows)

        panels_or_menus = sorted(set(panel for panel in all_panels_or_menus if panel))
        updated = OrderedDict()
        for key in [
            "accession",
            "sdrf_path",
            "title",
            "submission_type",
            "publication_date",
            "platform_family",
            "templates",
            "organism",
            "organism_part",
            "disease",
            "sample_matrix",
        ]:
            updated[key] = manifest_row.get(key, "")
        updated["primary_matrix_count"] = str(len(primary_file_rows))
        updated["sample_row_count"] = str(len(sdrf_rows))
        updated["primary_matrices"] = ";".join(row["comment[data file]"] for row in primary_file_rows)
        updated["skipped_secondary_files"] = ";".join(skipped)
        updated["pride_url"] = manifest_row.get("pride_url", "")
        updated["europepmc_evidence"] = manifest_row.get("europepmc_evidence", "")
        updated["notes"] = (
            "Regenerated by sdrf-autoresearch from primary deposited NPX/ADAT/parquet "
            "matrices; rows represent extracted sample-level matrix entries."
        )
        updated_manifest.append(updated)

        first_platform = ""
        if sdrf_rows:
            first_platform = sdrf_rows[0][header.index("comment[platform]")]
        autoresearch_rows.append(
            {
                "accession": accession,
                "sdrf_path": manifest_row["sdrf_path"],
                "rows": str(len(sdrf_rows)),
                "primary_matrices": str(len(primary_file_rows)),
                "platform_family": platform_family,
                "technology_type": (
                    "protein expression profiling by antibody array"
                    if platform_family == "olink"
                    else "protein expression profiling by aptamer array"
                ),
                "platform": first_platform,
                "panel_or_menu": "; ".join(panels_or_menus[:12]) or NA,
                "quantification_unit": "NPX" if platform_family == "olink" else "RFU",
                "organism_template": "human",
                "evidence_pride": manifest_row.get("pride_url", ""),
                "evidence_europepmc": manifest_row.get("europepmc_evidence", ""),
                "validation_status": "pending_validation",
                "validation_note": "Regenerated from primary NPX/ADAT/parquet matrices; validation pending.",
            }
        )

        print(
            f"{accession}: wrote {len(sdrf_rows)} sample-level rows "
            f"from {len(primary_file_rows)} primary matrices"
        )

    with (CAMPAIGN / "data-matrix-inspection.json").open("w") as handle:
        json.dump(inspection, handle, indent=2)
        handle.write("\n")

    with (CAMPAIGN / "manifest.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(updated_manifest[0]))
        writer.writeheader()
        writer.writerows(updated_manifest)

    with (CAMPAIGN / "autoresearch-round1.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(autoresearch_rows[0]))
        writer.writeheader()
        writer.writerows(autoresearch_rows)

    print(f"Inspection written to {CAMPAIGN / 'data-matrix-inspection.json'}")


if __name__ == "__main__":
    rebuild()
