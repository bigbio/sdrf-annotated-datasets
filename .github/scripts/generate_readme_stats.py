#!/usr/bin/env python3
"""Aggregate curated SDRF stats and refresh README plots.

Scans datasets/**/*.sdrf.tsv (sandbox excluded), writes:
  docs/stats/summary.json
  docs/stats/plots/{organisms,diseases,methods,completeness,templates}.png
  and replaces the README markers <!-- STATS:START --> ... <!-- STATS:END -->.

Pass --plots-only to redraw figures from an existing summary.json.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASETS_DIR = REPO_ROOT / "datasets"
STATS_DIR = REPO_ROOT / "docs" / "stats"
PLOTS_DIR = STATS_DIR / "plots"
README_PATH = REPO_ROOT / "README.md"

STATS_START = "<!-- STATS:START -->"
STATS_END = "<!-- STATS:END -->"

# MS ontology accession used widely for label-free sample
LABEL_FREE_AC = "MS:1002038"

NA_TOKENS = {
    "",
    "na",
    "n/a",
    "none",
    "null",
    "not available",
    "not applicable",
    "not applicable.",
    "unknown",
    ".",
}

NOT_APPLICABLE_TOKENS = {
    "not applicable",
    "not applicable.",
}

COMPLETENESS_FIELDS = [
    "organism",
    "organism part",
    "disease",
    "cell type",
    "age",
    "sex",
    "developmental stage",
    "ancestry category",
    "cell line",
]

BY_ORGANISM_FIELDS = [
    "organism part",
    "disease",
    "age",
    "sex",
    "cell type",
]

TEMPLATE_LAYER = {
    "ms-proteomics": "Technology",
    "affinity-proteomics": "Technology",
    "ms-metabolomics": "Technology",
    "human": "Sample",
    "vertebrates": "Sample",
    "invertebrates": "Sample",
    "plants": "Sample",
    "metaproteomics": "Sample",
    "human-gut": "Sample",
    "soil": "Sample",
    "water": "Sample",
    "clinical-metadata": "Sample",
    "oncology-metadata": "Sample",
    "dia-acquisition": "Experiment",
    "single-cell": "Experiment",
    "crosslinking": "Experiment",
    "immunopeptidomics": "Experiment",
    "cell-lines": "Experiment",
    "lc-ms-metabolomics": "Experiment",
    "gc-ms-metabolomics": "Experiment",
}

METAPROTEOMICS_TEMPLATES = {
    "metaproteomics",
    "human-gut",
    "soil",
    "water",
}

TECHNOLOGY_TEMPLATES = {
    "ms-proteomics",
    "affinity-proteomics",
    "ms-metabolomics",
}

HEALTHY_DISEASE_TOKENS = {
    "normal",
    "healthy",
    "healthy control",
    "healthy controls",
    "control",
    "controls",
    "no disease",
    "none",
    "not applicable",
}

_AC_RE = re.compile(r"(?:^|;)\s*AC=[^;]+;?", flags=re.IGNORECASE)
_NT_RE = re.compile(r"(?:^|;)\s*NT=([^;]+)", flags=re.IGNORECASE)
_LABEL_FREE_RE = re.compile(r"label[\s-]?free|labelfree", flags=re.IGNORECASE)


def normalize_term(raw: str | None) -> str | None:
    """Strip SDRF NT=/AC= payloads and return a displayable name."""
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None

    nt = _NT_RE.search(text)
    if nt:
        text = nt.group(1).strip()
    else:
        text = _AC_RE.sub("", text).strip(" ;")
        if not text:
            return None

    if text.lower() in NA_TOKENS:
        return None
    return text


def canonicalize_organism(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name).strip()
    parts = cleaned.split(" ")
    if len(parts) >= 2 and parts[0].isalpha() and parts[1].isalpha():
        genus = parts[0].capitalize()
        species = " ".join(p.lower() for p in parts[1:])
        return f"{genus} {species}"
    return cleaned


def classify_label(raw: str | None) -> str | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text or text.lower() in NA_TOKENS:
        return None
    upper = text.upper()
    if LABEL_FREE_AC in upper or _LABEL_FREE_RE.search(text):
        return "LFQ"
    if "TMT" in upper:
        return "TMT"
    if "ITRAQ" in upper:
        return "iTRAQ"
    if "SILAC" in upper:
        return "SILAC"
    return "Other"


def classify_acquisition(raw: str | None) -> str | None:
    if raw is None:
        return None
    text = normalize_term(raw) or str(raw).strip()
    if not text or text.lower() in NA_TOKENS:
        return None
    lower = text.lower()
    if "independent" in lower or lower == "dia":
        return "DIA"
    if "dependent" in lower or lower == "dda":
        return "DDA"
    if "reaction monitoring" in lower or lower in {"srm", "mrm", "prm"}:
        return "SRM/MRM"
    return "Other"


def parse_template_name(raw: str | None) -> str | None:
    """Return the leaf template name from comment[sdrf template]."""
    if raw is None:
        return None
    text = str(raw).strip()
    if not text or text.lower() in NA_TOKENS:
        return None
    if "NT=" in text.upper():
        for part in text.split(";"):
            if part.strip().upper().startswith("NT="):
                name = part.split("=", 1)[1].strip()
                return name or None
        return None
    split = re.split(r"\s+v", text, maxsplit=1, flags=re.IGNORECASE)
    return split[0].strip() or None


def completeness_status(raw: str | None) -> str:
    """Classify a cell as filled, incomplete, or not_applicable."""
    if raw is None:
        return "incomplete"
    text = str(raw).strip()
    if not text:
        return "incomplete"
    lower = text.lower()
    if lower in NOT_APPLICABLE_TOKENS:
        return "not_applicable"
    if lower in NA_TOKENS:
        return "incomplete"
    if normalize_term(text) is None:
        return "incomplete"
    return "filled"


def _header_index(headers: list[str], name: str | None) -> int | None:
    if not name:
        return None
    try:
        return headers.index(name)
    except ValueError:
        return None


def _cell(row: list[str], idx: int | None) -> str:
    if idx is None or idx < 0 or idx >= len(row):
        return ""
    return row[idx]


def find_header(headers: list[str], *predicates) -> str | None:
    for header in headers:
        hl = header.lower()
        if all(pred(hl) for pred in predicates):
            return header
    return None


def find_column(headers: list[str], kind: str) -> str | None:
    lookup = {
        "organism": lambda hs: find_header(
            hs,
            lambda h: "organism]" in h or h.endswith("[organism]"),
            lambda h: "organism part" not in h,
        ),
        "disease": lambda hs: (
            find_header(
                hs,
                lambda h: h.startswith("characteristics[") and "disease" in h,
            )
            or find_header(hs, lambda h: "disease" in h)
        ),
        "label": lambda hs: find_header(hs, lambda h: h == "comment[label]"),
        "acquisition": lambda hs: find_header(
            hs, lambda h: "proteomics data acquisition method" in h
        ),
        "source": lambda hs: find_header(hs, lambda h: h == "source name"),
        "data_file": lambda hs: find_header(
            hs, lambda h: h == "comment[data file]"
        ),
        "organism_part": lambda hs: find_header(
            hs, lambda h: "organism part" in h
        ),
        "age": lambda hs: find_header(
            hs,
            lambda h: h.endswith("[age]") or h == "characteristics[age]",
        ),
        "sex": lambda hs: find_header(
            hs,
            lambda h: h.endswith("[sex]") or h == "characteristics[sex]",
        ),
        "cell_type": lambda hs: find_header(hs, lambda h: "cell type" in h),
        "cell_line": lambda hs: find_header(hs, lambda h: "cell line" in h),
        "developmental_stage": lambda hs: find_header(
            hs, lambda h: "developmental stage" in h
        ),
        "ancestry": lambda hs: find_header(hs, lambda h: "ancestry" in h),
    }
    if kind not in lookup:
        raise ValueError(f"unknown column kind: {kind}")
    return lookup[kind](headers)


def iter_sdrf_files() -> list[Path]:
    if not DATASETS_DIR.exists():
        return []
    return sorted(DATASETS_DIR.rglob("*.sdrf.tsv"))


@dataclass
class AggregateState:
    diseases: Counter = field(default_factory=Counter)
    labels: Counter = field(default_factory=Counter)
    acquisitions: Counter = field(default_factory=Counter)
    samples_by_organism: Counter = field(default_factory=Counter)
    sample_seen: set[tuple[str, str]] = field(default_factory=set)
    run_seen: set[tuple[str, str]] = field(default_factory=set)
    accession_organisms: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    total_rows: int = 0
    completeness: dict[str, Counter] = field(
        default_factory=lambda: defaultdict(Counter)
    )
    completeness_by_org: dict[str, dict[str, Counter]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(Counter))
    )
    templates_files: Counter = field(default_factory=Counter)
    templates_accessions: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    files_with_template: int = 0
    accessions_with_template: set[str] = field(default_factory=set)
    specialty_files: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    specialty_accessions: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )


FIELD_KIND = {
    "organism": "organism",
    "organism part": "organism_part",
    "disease": "disease",
    "age": "age",
    "sex": "sex",
    "cell type": "cell_type",
    "cell line": "cell_line",
    "developmental stage": "developmental_stage",
    "ancestry category": "ancestry",
}

SPECIALTY_FROM_TEMPLATE = {
    "single-cell": "Single-cell",
    "cell-lines": "Cell lines",
    "crosslinking": "Crosslinking",
    "immunopeptidomics": "Immunopeptidomics",
    "dia-acquisition": "DIA",
    "affinity-proteomics": "Affinity proteomics",
    "clinical-metadata": "Clinical",
    "oncology-metadata": "Oncology",
}


def _mark_specialty(
    state: AggregateState, name: str, accession: str, path_key: str
) -> None:
    state.specialty_accessions[name].add(accession)
    state.specialty_files[name].add(path_key)


def process_sdrf_file(path: Path, state: AggregateState) -> None:
    accession = path.parent.name
    path_key = path.as_posix()
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            headers = next(reader)
        except StopIteration:
            return
        headers = [h.strip() for h in headers]
        if not headers:
            return

        idx = {
            kind: _header_index(headers, find_column(headers, kind))
            for kind in (
                "organism",
                "organism_part",
                "disease",
                "age",
                "sex",
                "cell_type",
                "cell_line",
                "developmental_stage",
                "ancestry",
                "label",
                "acquisition",
                "source",
                "data_file",
            )
        }
        tmpl_idxs = [
            i
            for i, header in enumerate(headers)
            if header.lower() == "comment[sdrf template]"
        ]

        sample_org: dict[str, str] = {}
        sample_dis: dict[str, str] = {}
        sample_seen_local: set[str] = set()
        file_templates: set[str] = set()
        has_filled_cell_line = False
        has_metagenome = False

        for row in reader:
            if not row or not any(cell.strip() for cell in row):
                continue
            state.total_rows += 1
            source = _cell(row, idx["source"]).strip()
            data_file = _cell(row, idx["data_file"]).strip()

            for tmpl_i in tmpl_idxs:
                name = parse_template_name(_cell(row, tmpl_i))
                if name:
                    file_templates.add(name)

            lab = classify_label(_cell(row, idx["label"]) or None)
            if lab:
                state.labels[lab] += 1
            acq = classify_acquisition(_cell(row, idx["acquisition"]) or None)
            if acq:
                state.acquisitions[acq] += 1
            if data_file:
                state.run_seen.add((path_key, data_file))

            if not source or source in sample_seen_local:
                continue
            sample_seen_local.add(source)
            state.sample_seen.add((path_key, source))

            org_raw = _cell(row, idx["organism"])
            org = normalize_term(org_raw)
            if org:
                org = canonicalize_organism(org)
                sample_org[source] = org
                if "metagenome" in org.lower() or "microbiome" in org.lower():
                    has_metagenome = True

            dis = normalize_term(_cell(row, idx["disease"]))
            if dis and dis.lower() not in HEALTHY_DISEASE_TOKENS:
                sample_dis[source] = dis

            statuses: dict[str, str] = {}
            for field, kind in FIELD_KIND.items():
                if idx[kind] is None:
                    statuses[field] = "incomplete"
                else:
                    statuses[field] = completeness_status(_cell(row, idx[kind]))
                state.completeness[field][statuses[field]] += 1
            if statuses.get("cell line") == "filled":
                has_filled_cell_line = True
            if org:
                for field in BY_ORGANISM_FIELDS:
                    state.completeness_by_org[org][field][statuses[field]] += 1

        for org in sample_org.values():
            state.samples_by_organism[org] += 1
            state.accession_organisms[accession].add(org)
        for dis in sample_dis.values():
            state.diseases[dis] += 1

        if file_templates:
            state.files_with_template += 1
            state.accessions_with_template.add(accession)
            for name in file_templates:
                state.templates_files[name] += 1
                state.templates_accessions[name].add(accession)
                if name in METAPROTEOMICS_TEMPLATES:
                    _mark_specialty(state, "Metaproteomics", accession, path_key)
                specialty = SPECIALTY_FROM_TEMPLATE.get(name)
                if specialty:
                    _mark_specialty(state, specialty, accession, path_key)

        if has_filled_cell_line:
            _mark_specialty(state, "Cell lines", accession, path_key)
        if has_metagenome:
            _mark_specialty(state, "Metaproteomics", accession, path_key)


def _completeness_entry(name: str, counts: Counter) -> dict:
    filled = int(counts.get("filled", 0))
    incomplete = int(counts.get("incomplete", 0))
    not_applicable = int(counts.get("not_applicable", 0))
    applicable = filled + incomplete
    pct = round(100.0 * filled / applicable, 1) if applicable else 0.0
    return {
        "name": name,
        "filled": filled,
        "applicable": applicable,
        "not_applicable": not_applicable,
        "pct": pct,
    }


def aggregate() -> dict:
    files = iter_sdrf_files()
    state = AggregateState()
    for path in files:
        process_sdrf_file(path, state)

    organisms: Counter = Counter()
    for orgs in state.accession_organisms.values():
        organisms.update(orgs)

    completeness = [
        _completeness_entry(field, state.completeness[field])
        for field in COMPLETENESS_FIELDS
    ]

    top_orgs = [name for name, _ in state.samples_by_organism.most_common(8)]
    completeness_by_organism = []
    for org in top_orgs:
        field_rows = [
            _completeness_entry(field, state.completeness_by_org[org][field])
            for field in BY_ORGANISM_FIELDS
        ]
        completeness_by_organism.append({"name": org, "fields": field_rows})

    templates = []
    for name, accessions in sorted(
        state.templates_accessions.items(),
        key=lambda kv: (-len(kv[1]), kv[0]),
    ):
        templates.append(
            {
                "name": name,
                "accessions": len(accessions),
                "files": int(state.templates_files[name]),
                "layer": TEMPLATE_LAYER.get(name, "Other"),
            }
        )

    specialty_order = [
        "Single-cell",
        "Cell lines",
        "Metaproteomics",
        "Crosslinking",
        "Immunopeptidomics",
        "DIA",
        "Affinity proteomics",
        "Clinical",
        "Oncology",
    ]
    specialties = []
    for name in specialty_order:
        acc = state.specialty_accessions.get(name, set())
        files_for = state.specialty_files.get(name, set())
        if not acc and not files_for:
            specialties.append(
                {"name": name, "accessions": 0, "files": 0}
            )
            continue
        specialties.append(
            {
                "name": name,
                "accessions": len(acc),
                "files": len(files_for),
            }
        )

    n_accessions = len({p.parent.name for p in files})
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "generated_at": generated_at,
        "totals": {
            "accessions": n_accessions,
            "sdrf_files": len(files),
            "samples": len(state.sample_seen),
            "runs": len(state.run_seen),
            "assay_rows": state.total_rows,
            "files_with_template": state.files_with_template,
            "accessions_with_template": len(state.accessions_with_template),
        },
        "organisms": organisms.most_common(),
        "samples_by_organism": state.samples_by_organism.most_common(),
        "diseases": state.diseases.most_common(),
        "labels": state.labels.most_common(),
        "acquisitions": state.acquisitions.most_common(),
        "completeness": completeness,
        "completeness_by_organism": completeness_by_organism,
        "templates": templates,
        "specialties": specialties,
    }


def top_with_other(
    items: list[tuple[str, int]], n: int = 10
) -> list[tuple[str, int]]:
    if len(items) <= n:
        return items
    head = items[:n]
    other = sum(v for _, v in items[n:])
    if other:
        head = head + [("Other", other)]
    return head


INK = "#1B2838"
MUTED = "#5B6775"
GRID = "#E4E8F0"
AXIS = "#C5CAD3"
FACE = "#FFFFFF"
OTHER_COLOR = "#B7BDC6"

# Shared categorical colours so the same organism matches across panels.
ORGANISM_COLORS = [
    "#1F4E79",
    "#2E86AB",
    "#1A7F7A",
    "#3D8B5C",
    "#7A9B3C",
    "#C4922A",
    "#D36B2F",
    "#C44536",
    "#8E4A73",
    "#5C6B8A",
    "#6D7C8B",
]

DISEASE_COLORS = [
    "#4A0E32",
    "#6B1D4A",
    "#8B2E5F",
    "#A63D70",
    "#C04A7E",
    "#D16B94",
    "#DC8AA9",
    "#E5A8BE",
    "#EDC4D2",
    "#C9A0B8",
]

LABEL_COLORS = {
    "LFQ": "#1F4E79",
    "TMT": "#D36B2F",
    "SILAC": "#1A7F7A",
    "iTRAQ": "#8E4A73",
    "Other": OTHER_COLOR,
}

ACQ_COLORS = {
    "DDA": "#1F4E79",
    "DIA": "#2E9A8F",
    "SRM/MRM": "#C4922A",
    "Other": OTHER_COLOR,
}

_BINOMIAL_BLOCKLIST = {
    "human",
    "severe",
    "other",
    "bacteria",
    "unknown",
}

SAVE_DPI = 200


def _apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "DejaVu Sans",
                "Liberation Sans",
                "Arial",
                "Helvetica",
            ],
            "font.size": 10,
            "text.color": INK,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.titlecolor": INK,
            "axes.labelsize": 10,
            "axes.labelcolor": MUTED,
            "axes.edgecolor": AXIS,
            "axes.linewidth": 0.7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.color": MUTED,
            "ytick.color": INK,
            "xtick.labelsize": 9,
            "ytick.labelsize": 10,
            "figure.facecolor": FACE,
            "axes.facecolor": FACE,
            "savefig.facecolor": FACE,
            "savefig.dpi": SAVE_DPI,
            "axes.grid": False,
        }
    )


def _shorten_label(text: str, max_len: int = 34) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def _is_binomial(name: str) -> bool:
    parts = name.split()
    if len(parts) not in {2, 3}:
        return False
    if not parts[0][:1].isupper():
        return False
    if not all(p.isalpha() for p in parts):
        return False
    if parts[0].lower() in _BINOMIAL_BLOCKLIST:
        return False
    return all(p[:1].islower() for p in parts[1:])


def _split_other(
    items: list[tuple[str, int]],
) -> tuple[list[tuple[str, int]], int]:
    named = [(k, v) for k, v in items if k != "Other"]
    other = sum(v for k, v in items if k == "Other")
    named.sort(key=lambda kv: kv[1], reverse=True)
    return named, other


def _order_hbar_items(
    items: list[tuple[str, int]],
) -> list[tuple[str, int]]:
    named, other = _split_other(items)
    if other:
        named = named + [("Other", other)]
    return named


def _count_tick(value: float, _pos=None) -> str:
    if value <= 0:
        return "0"
    if value >= 1_000_000:
        as_m = value / 1_000_000
        return f"{as_m:.1f}M".replace(".0M", "M")
    if value >= 1000:
        as_k = value / 1000
        if abs(as_k - round(as_k)) < 1e-6:
            return f"{int(round(as_k))}k"
        return f"{as_k:.1f}k"
    return f"{int(value)}"


def _organism_colors(names: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {"Other": OTHER_COLOR}
    palette = [c for c in ORGANISM_COLORS]
    idx = 0
    for name in names:
        if name in mapping:
            continue
        mapping[name] = palette[idx % len(palette)]
        idx += 1
    return mapping


def _style_axes(ax, *, xlabel: str | None = None) -> None:
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=GRID, linewidth=0.7, linestyle="-")
    ax.tick_params(axis="y", length=0, pad=5)
    ax.tick_params(axis="x", length=3, width=0.6, color=AXIS)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color=MUTED, labelpad=6)
    ax.xaxis.set_major_formatter(FuncFormatter(_count_tick))


def _italicize_binomial_ticks(ax, names: list[str]) -> None:
    for tick, name in zip(ax.get_yticklabels(), names, strict=True):
        if _is_binomial(name):
            tick.set_fontstyle("italic")


def _contrasting_text(face_rgba) -> str:
    r, g, b = face_rgba[:3]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return FACE if luminance < 0.62 else INK


def _annotate_bars(
    ax,
    bars,
    values: list[int],
    *,
    total: int,
    xmax: float,
    show_percent: bool,
) -> None:
    for bar, value in zip(bars, values, strict=True):
        pct = 100.0 * value / total
        label = f"{value:,} ({pct:.0f}%)" if show_percent else f"{value:,}"
        inside = bar.get_width() >= xmax * 0.28
        text_color = (
            _contrasting_text(bar.get_facecolor()) if inside else INK
        )
        ax.text(
            bar.get_width() * 0.985 if inside else bar.get_width() + xmax * 0.018,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="right" if inside else "left",
            fontsize=8.5,
            color=text_color,
            fontweight="bold" if inside else "normal",
            clip_on=False,
        )


def _draw_hbar(
    ax,
    items: list[tuple[str, int]],
    *,
    colors: list[str],
    show_percent: bool = False,
    italic_binomials: bool = False,
    xlabel: str = "Count",
    preserve_order: bool = False,
) -> None:
    if not items:
        ax.set_axis_off()
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=MUTED)
        return

    ordered = items if preserve_order else _order_hbar_items(items)
    names = [k for k, _ in ordered]
    labels = [_shorten_label(k) for k in names]
    values = [v for _, v in ordered]
    total = sum(values) or 1
    n = len(values)
    y = list(range(n))
    bar_colors = [colors[i] if i < len(colors) else OTHER_COLOR for i in range(n)]

    bars = ax.barh(
        y,
        values,
        color=bar_colors,
        edgecolor=FACE,
        linewidth=0.6,
        height=0.72,
        zorder=3,
    )
    for bar, name in zip(bars, names, strict=True):
        if name == "Other":
            bar.set_color(OTHER_COLOR)
            bar.set_alpha(0.95)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    if italic_binomials:
        _italicize_binomial_ticks(ax, names)

    xmax = max(values) if values else 1
    ax.set_xlim(0, xmax * 1.24)
    _style_axes(ax, xlabel=xlabel)
    _annotate_bars(
        ax,
        bars,
        values,
        total=total,
        xmax=xmax,
        show_percent=show_percent,
    )


def _draw_donut(
    ax,
    items: list[tuple[str, int]],
    *,
    color_map: dict[str, str],
    center_caption: str,
    legend: str = "none",
) -> None:
    ordered = _order_hbar_items(items)
    if not ordered:
        ax.set_axis_off()
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=MUTED)
        return

    names = [k for k, _ in ordered]
    values = [v for _, v in ordered]
    total = sum(values) or 1
    colors = [color_map.get(name, OTHER_COLOR) for name in names]

    wedges, _ = ax.pie(
        values,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.48, edgecolor=FACE, linewidth=2.2),
        radius=1.0,
    )
    ax.set_aspect("equal")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.25, 1.25)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    ax.text(
        0,
        0.10,
        f"{total:,}",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=INK,
    )
    ax.text(
        0,
        -0.18,
        center_caption,
        ha="center",
        va="center",
        fontsize=8,
        color=MUTED,
    )

    if legend == "none":
        return

    legend_labels = [
        f"{name}   {value:,}  ({100.0 * value / total:.1f}%)"
        for name, value in ordered
    ]
    loc, bbox = (
        ("upper center", (0.5, -0.04))
        if legend == "below"
        else ("center left", (1.08, 0.5))
    )
    legend_artist = ax.legend(
        wedges,
        legend_labels,
        loc=loc,
        bbox_to_anchor=bbox,
        ncol=1,
        frameon=False,
        fontsize=8.5,
        handlelength=1.05,
        handleheight=1.05,
        borderaxespad=0.0,
        labelspacing=0.6,
    )
    for text in legend_artist.get_texts():
        text.set_color(INK)


def _draw_color_key(
    ax,
    items: list[tuple[str, int]],
    color_map: dict[str, str],
) -> None:
    ordered = _order_hbar_items(items)
    ax.set_axis_off()
    if not ordered:
        return
    total = sum(v for _, v in ordered) or 1
    n = len(ordered)
    ax.set_xlim(0, 1)
    ax.set_ylim(-(n + 1) / 2.0, (n + 1) / 2.0)
    for i, (name, value) in enumerate(ordered):
        y = (n - 1) / 2.0 - i
        ax.scatter(
            [0.04],
            [y],
            s=90,
            c=[color_map.get(name, OTHER_COLOR)],
            marker="s",
            linewidths=0,
            zorder=3,
            clip_on=False,
        )
        pct = 100.0 * value / total
        ax.text(
            0.12,
            y,
            f"{name}    {value:,}   ({pct:.1f}%)",
            fontsize=9,
            va="center",
            ha="left",
            color=INK,
            clip_on=False,
        )


def _panel_title(ax, letter: str, title: str) -> None:
    ax.set_title(
        f"{letter}   {title}",
        loc="left",
        fontsize=11,
        fontweight="bold",
        pad=8,
        color=INK,
    )


def _make_figure(
    *,
    nrows: int,
    ncols: int,
    figsize: tuple[float, float],
    title: str,
    subtitle: str,
    width_ratios: list[float] | None = None,
    wspace: float = 0.28,
    hspace: float = 0.34,
    left: float = 0.08,
    right: float = 0.97,
    top: float = 0.97,
    bottom: float = 0.08,
    header_ratio: float = 0.16,
):
    fig = plt.figure(figsize=figsize)
    outer = fig.add_gridspec(
        2,
        1,
        height_ratios=[header_ratio, 1.0],
        hspace=0.08,
        left=left,
        right=right,
        top=top,
        bottom=bottom,
    )
    header = fig.add_subplot(outer[0, 0])
    header.set_axis_off()
    header.set_xlim(0, 1)
    header.set_ylim(0, 1)
    header.text(
        0.0,
        0.70,
        title,
        fontsize=13.5,
        fontweight="bold",
        va="center",
        ha="left",
        color=INK,
    )
    header.text(
        0.0,
        0.12,
        subtitle,
        fontsize=8.5,
        color=MUTED,
        va="center",
        ha="left",
    )
    header.plot(
        [0, 1],
        [-0.18, -0.18],
        color=GRID,
        linewidth=0.9,
        clip_on=False,
        transform=header.transAxes,
    )

    inner = outer[1, 0].subgridspec(
        nrows,
        ncols,
        wspace=wspace,
        hspace=hspace,
        width_ratios=width_ratios,
    )
    axes = [
        [fig.add_subplot(inner[r, c]) for c in range(ncols)] for r in range(nrows)
    ]
    if nrows == 1 and ncols == 1:
        return fig, axes[0][0]
    if nrows == 1:
        return fig, axes[0]
    if ncols == 1:
        return fig, [row[0] for row in axes]
    return fig, axes


def _save(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        path,
        dpi=SAVE_DPI,
        bbox_inches="tight",
        pad_inches=0.16,
        facecolor=FACE,
    )
    plt.close(fig)


def _empty_figure(path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8.4, 3.2))
    ax.set_axis_off()
    ax.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=12, color=MUTED)
    ax.set_title(title, fontsize=13, pad=10, fontweight="bold")
    _save(fig, path)


def render_organism_figure(
    path: Path,
    accessions: list[tuple[str, int]],
    samples: list[tuple[str, int]],
) -> None:
    acc_items = top_with_other(accessions, 10)
    sample_items = top_with_other(samples, 10)
    if not acc_items and not sample_items:
        _empty_figure(path, "Organisms")
        return

    names_for_color: list[str] = []
    for items in (acc_items, sample_items):
        for name, _ in _order_hbar_items(items):
            if name not in names_for_color:
                names_for_color.append(name)
    cmap = _organism_colors(names_for_color)

    fig, axes = _make_figure(
        nrows=2,
        ncols=1,
        figsize=(8.6, 9.8),
        title="Organisms in curated annotations",
        subtitle="Top 10 taxa plus remaining organisms aggregated as Other.",
        hspace=0.28,
        left=0.28,
        right=0.97,
        bottom=0.06,
        header_ratio=0.11,
    )

    for ax, items, letter, title, xlabel in (
        (axes[0], acc_items, "A", "Accessions", "Accessions"),
        (axes[1], sample_items, "B", "Samples", "Samples"),
    ):
        ordered = _order_hbar_items(items)
        colors = [cmap.get(name, OTHER_COLOR) for name, _ in ordered]
        _panel_title(ax, letter, title)
        _draw_hbar(
            ax,
            items,
            colors=colors,
            italic_binomials=True,
            xlabel=xlabel,
        )

    _save(fig, path)


def render_disease_figure(path: Path, diseases: list[tuple[str, int]]) -> None:
    items = top_with_other(diseases, 10)
    named, other = _split_other(items)
    if not named and not other:
        _empty_figure(path, "Diseases")
        return

    n_other_terms = max(0, len(diseases) - 10)
    share_items = [
        ("Top 10 terms", sum(v for _, v in named)),
        ("Other terms", other),
    ]
    share_colors = {"Top 10 terms": "#8B2E5F", "Other terms": OTHER_COLOR}

    fig, axes = _make_figure(
        nrows=1,
        ncols=3,
        figsize=(10.0, 5.6),
        title="Disease annotations",
        subtitle=(
            "Healthy / normal / control samples excluded. "
            f"{n_other_terms:,} additional disease terms aggregated as Other."
        ),
        width_ratios=[1.65, 0.95, 0.90],
        wspace=0.12,
        left=0.20,
        right=0.98,
        bottom=0.10,
        header_ratio=0.24,
    )

    _panel_title(axes[0], "A", "Most frequent terms")
    _draw_hbar(
        axes[0],
        named,
        colors=DISEASE_COLORS[: len(named)],
        xlabel="Samples",
    )

    _panel_title(axes[1], "B", "Share of annotated samples")
    _draw_donut(
        axes[1],
        share_items,
        color_map=share_colors,
        center_caption="samples",
        legend="none",
    )
    axes[2].set_title(" ", pad=8)
    _draw_color_key(axes[2], share_items, share_colors)

    _save(fig, path)


def render_methods_figure(
    path: Path,
    labels: list[tuple[str, int]],
    acquisitions: list[tuple[str, int]],
) -> None:
    if not labels and not acquisitions:
        _empty_figure(path, "Assay methods")
        return

    fig, axes = _make_figure(
        nrows=1,
        ncols=4,
        figsize=(10.4, 4.6),
        title="Quantification and acquisition",
        subtitle=(
            "Assay rows with a recognized quantification label or acquisition method."
        ),
        width_ratios=[1.20, 0.92, 1.20, 1.05],
        wspace=0.05,
        left=0.02,
        right=0.99,
        bottom=0.06,
        header_ratio=0.22,
    )

    _panel_title(axes[0], "A", "Quantification label")
    _draw_donut(
        axes[0],
        labels,
        color_map=LABEL_COLORS,
        center_caption="assay rows",
        legend="none",
    )
    axes[1].set_title(" ", pad=8)
    _draw_color_key(axes[1], labels, LABEL_COLORS)

    _panel_title(axes[2], "B", "Acquisition method")
    _draw_donut(
        axes[2],
        acquisitions,
        color_map=ACQ_COLORS,
        center_caption="assay rows",
        legend="none",
    )
    axes[3].set_title(" ", pad=8)
    _draw_color_key(axes[3], acquisitions, ACQ_COLORS)

    _save(fig, path)


LAYER_COLORS = {
    "Technology": "#1F4E79",
    "Sample": "#1A7F7A",
    "Experiment": "#D36B2F",
    "Other": OTHER_COLOR,
}

SPECIALTY_COLORS = {
    "Single-cell": "#8E4A73",
    "Cell lines": "#2E86AB",
    "Metaproteomics": "#3D8B5C",
    "Crosslinking": "#C4922A",
    "Immunopeptidomics": "#C44536",
    "DIA": "#1A7F7A",
    "Affinity proteomics": "#5C6B8A",
    "Clinical": "#6B1D4A",
    "Oncology": "#A63D70",
}

COMPLETE_CMAP = LinearSegmentedColormap.from_list(
    "sdrf_complete", ["#F2F4F7", "#7FB8B2", "#1A7F7A", "#1F4E79"]
)
COMPLETE_CMAP.set_bad("#EEF1F4")


def _draw_pct_hbar(ax, rows: list[dict], *, color: str = "#1A7F7A") -> None:
    if not rows:
        ax.set_axis_off()
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=MUTED)
        return
    labels = [row["name"] for row in rows]
    values = [float(row["pct"]) for row in rows]
    n = len(values)
    y = list(range(n))
    bars = ax.barh(
        y,
        values,
        color=color,
        edgecolor=FACE,
        linewidth=0.6,
        height=0.72,
        zorder=3,
    )
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 112)
    _style_axes(ax, xlabel="% of applicable samples")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{int(v)}%"))
    for bar, row in zip(bars, rows, strict=True):
        filled = int(row.get("filled", 0))
        applicable = int(row.get("applicable", 0))
        label = f"{row['pct']:.0f}%   ({filled:,} / {applicable:,})"
        inside = bar.get_width() >= 38
        ax.text(
            bar.get_width() - 1.2 if inside else bar.get_width() + 1.4,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="right" if inside else "left",
            fontsize=8,
            color=_contrasting_text(bar.get_facecolor()) if inside else INK,
            fontweight="bold" if inside else "normal",
            clip_on=False,
        )


def render_completeness_figure(
    path: Path,
    completeness: list[dict],
    by_organism: list[dict],
) -> None:
    if not completeness:
        _empty_figure(path, "Annotation completeness")
        return

    fig, axes = _make_figure(
        nrows=2,
        ncols=1,
        figsize=(8.8, 9.4),
        title="Annotation completeness",
        subtitle=(
            "Share of samples with a real value. Missing columns and "
            "'not available' count as incomplete; 'not applicable' is excluded."
        ),
        hspace=0.38,
        left=0.22,
        right=0.97,
        bottom=0.08,
        header_ratio=0.12,
    )

    _panel_title(axes[0], "A", "By metadata field")
    labeled = [
        {**row, "name": row["name"][:1].upper() + row["name"][1:]}
        for row in completeness
    ]
    _draw_pct_hbar(axes[0], labeled, color="#1A7F7A")

    _panel_title(axes[1], "B", "By organism (top taxa by sample count)")
    ax = axes[1]
    if not by_organism:
        ax.set_axis_off()
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=MUTED)
        _save(fig, path)
        return

    fields = BY_ORGANISM_FIELDS
    field_labels = [name[:1].upper() + name[1:] for name in fields]
    organisms = [row["name"] for row in by_organism]
    matrix: list[list[float]] = []
    for org_row in by_organism:
        lookup = {item["name"]: item for item in org_row.get("fields", [])}
        line: list[float] = []
        for field in fields:
            item = lookup.get(field, {"pct": 0.0, "applicable": 0})
            if item.get("applicable"):
                line.append(float(item["pct"]))
            else:
                line.append(float("nan"))
        matrix.append(line)

    im = ax.imshow(
        matrix,
        cmap=COMPLETE_CMAP,
        vmin=0,
        vmax=100,
        aspect="auto",
        interpolation="nearest",
    )
    ax.set_xticks(range(len(field_labels)))
    ax.set_xticklabels(field_labels, fontsize=9)
    ax.set_yticks(range(len(organisms)))
    ax.set_yticklabels([_shorten_label(name, 28) for name in organisms], fontsize=9)
    _italicize_binomial_ticks(ax, organisms)
    ax.tick_params(axis="both", length=0)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    for i, line in enumerate(matrix):
        for j, value in enumerate(line):
            if value != value:  # NaN
                text, color = "—", MUTED
            else:
                text = f"{value:.0f}"
                color = FACE if value >= 55 else INK
            ax.text(j, i, text, ha="center", va="center", fontsize=8, color=color)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.ax.tick_params(labelsize=8, length=2)
    cbar.set_label("% complete", fontsize=8, color=MUTED)

    _save(fig, path)


def render_templates_figure(
    path: Path,
    templates: list[dict],
    specialties: list[dict],
    totals: dict,
) -> None:
    tech_counts: dict[str, int] = {
        "MS proteomics": 0,
        "Affinity proteomics": 0,
        "Metabolomics": 0,
        "Undeclared": 0,
    }
    tech_map = {
        "ms-proteomics": "MS proteomics",
        "affinity-proteomics": "Affinity proteomics",
        "ms-metabolomics": "Metabolomics",
    }
    for row in templates:
        label = tech_map.get(row["name"])
        if label:
            tech_counts[label] = int(row["accessions"])
    n_acc = int(totals.get("accessions", 0))
    n_with = int(totals.get("accessions_with_template", 0))
    undeclared = max(0, n_acc - n_with)
    tech_counts["Undeclared"] = undeclared
    tech_bits = [
        f"{count:,} {label.lower()}"
        for label, count in tech_counts.items()
        if label != "Undeclared" and count
    ]
    tech_note = "; ".join(tech_bits) if tech_bits else "none declared"

    extra_templates = [
        (row["name"], int(row["accessions"]))
        for row in templates
        if row["name"] not in TECHNOLOGY_TEMPLATES
    ]
    extra_colors = [
        LAYER_COLORS.get(row["layer"], OTHER_COLOR)
        for row in templates
        if row["name"] not in TECHNOLOGY_TEMPLATES
    ]

    fig, axes = _make_figure(
        nrows=1,
        ncols=2,
        figsize=(10.2, 7.2),
        title="Templates and specialized collections",
        subtitle=(
            f"{n_with:,} of {n_acc:,} accessions declare a template "
            f"({tech_note}). Cell lines and metaproteomics also count "
            "filled cell-line or metagenome evidence."
        ),
        width_ratios=[1.15, 1.0],
        wspace=0.28,
        left=0.22,
        right=0.97,
        bottom=0.10,
        header_ratio=0.20,
    )

    _panel_title(axes[0], "A", "Sample and experiment templates")
    if extra_templates:
        _draw_hbar(
            axes[0],
            extra_templates,
            colors=extra_colors,
            xlabel="Accessions",
        )
    else:
        axes[0].set_axis_off()
        axes[0].text(0.5, 0.5, "No data", ha="center", va="center", color=MUTED)

    _panel_title(axes[1], "B", "Single-cell, cell lines, metaproteomics")
    specialty_items = [
        (row["name"], int(row["accessions"]))
        for row in specialties
        if int(row["accessions"]) > 0
        or row["name"] in {"Single-cell", "Cell lines", "Metaproteomics"}
    ]
    if not specialty_items:
        specialty_items = [
            (row["name"], int(row["accessions"])) for row in specialties
        ]
    specialty_colors = [
        SPECIALTY_COLORS.get(name, OTHER_COLOR) for name, _ in specialty_items
    ]
    _draw_hbar(
        axes[1],
        specialty_items,
        colors=specialty_colors,
        xlabel="Accessions",
        preserve_order=True,
    )

    _save(fig, path)


def _cleanup_stale_plots(keep: set[str]) -> None:
    if not PLOTS_DIR.exists():
        return
    for png in PLOTS_DIR.glob("*.png"):
        if png.name not in keep:
            png.unlink()


def render_plots(stats: dict) -> dict[str, str]:
    _apply_style()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "organisms": "plots/organisms.png",
        "diseases": "plots/diseases.png",
        "methods": "plots/methods.png",
        "completeness": "plots/completeness.png",
        "templates": "plots/templates.png",
    }

    render_organism_figure(
        STATS_DIR / paths["organisms"],
        stats["organisms"],
        stats["samples_by_organism"],
    )
    render_disease_figure(STATS_DIR / paths["diseases"], stats["diseases"])
    render_methods_figure(
        STATS_DIR / paths["methods"],
        stats["labels"],
        stats["acquisitions"],
    )
    render_completeness_figure(
        STATS_DIR / paths["completeness"],
        stats.get("completeness", []),
        stats.get("completeness_by_organism", []),
    )
    render_templates_figure(
        STATS_DIR / paths["templates"],
        stats.get("templates", []),
        stats.get("specialties", []),
        stats.get("totals", {}),
    )
    _cleanup_stale_plots({Path(p).name for p in paths.values()})
    return paths


def fmt_int(n: int) -> str:
    return f"{n:,}"


def _lookup_pct(rows: list[dict], name: str) -> float | None:
    for row in rows:
        if row.get("name") == name:
            return float(row.get("pct", 0))
    return None


def _lookup_specialty(rows: list[dict], name: str) -> int:
    for row in rows:
        if row.get("name") == name:
            return int(row.get("accessions", 0))
    return 0


def build_readme_section(stats: dict, plot_paths: dict[str, str]) -> str:
    totals = stats["totals"]
    top_org = stats["organisms"][0][0] if stats["organisms"] else "n/a"
    dia = dict(stats["acquisitions"]).get("DIA", 0)
    tmt = dict(stats["labels"]).get("TMT", 0)
    lfq = dict(stats["labels"]).get("LFQ", 0)
    age_pct = _lookup_pct(stats.get("completeness", []), "age")
    disease_pct = _lookup_pct(stats.get("completeness", []), "disease")
    n_single = _lookup_specialty(stats.get("specialties", []), "Single-cell")
    n_cell = _lookup_specialty(stats.get("specialties", []), "Cell lines")
    n_meta = _lookup_specialty(stats.get("specialties", []), "Metaproteomics")
    n_tmpl = int(totals.get("accessions_with_template", 0))

    completeness_bits = []
    if disease_pct is not None:
        completeness_bits.append(f"disease {disease_pct:.0f}%")
    if age_pct is not None:
        completeness_bits.append(f"age {age_pct:.0f}%")
    completeness_note = (
        "; sample-field completeness (applicable samples): "
        + ", ".join(completeness_bits)
        + "."
        if completeness_bits
        else "."
    )

    lines = [
        STATS_START,
        "## Resource at a glance",
        "",
        f"_Auto-generated from curated `datasets/` on {stats['generated_at']}. "
        "Sandbox drafts are excluded._",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| Accessions | {fmt_int(totals['accessions'])} |",
        f"| SDRF files | {fmt_int(totals['sdrf_files'])} |",
        f"| Accessions with a declared template | {fmt_int(n_tmpl)} |",
        f"| Samples (unique `source name` per file) | "
        f"{fmt_int(totals['samples'])} |",
        f"| Runs (unique `comment[data file]` per file) | "
        f"{fmt_int(totals['runs'])} |",
        f"| Assay rows | {fmt_int(totals['assay_rows'])} |",
        "",
        f"**Highlights:** most common organism is **{top_org}**; "
        f"**{fmt_int(dia)}** DIA assay rows; "
        f"**{fmt_int(tmt)}** TMT and **{fmt_int(lfq)}** LFQ assay rows; "
        f"**{fmt_int(n_single)}** single-cell, **{fmt_int(n_cell)}** cell-line, "
        f"and **{fmt_int(n_meta)}** metaproteomics accessions"
        f"{completeness_note}",
        "",
        f"![Organisms in curated annotations]"
        f"(docs/stats/{plot_paths['organisms']})",
        "",
        f"![Disease annotations]"
        f"(docs/stats/{plot_paths['diseases']})",
        "",
        f"![Quantification and acquisition methods]"
        f"(docs/stats/{plot_paths['methods']})",
        "",
        f"![Annotation completeness]"
        f"(docs/stats/{plot_paths['completeness']})",
        "",
        f"![Templates and specialized collections]"
        f"(docs/stats/{plot_paths['templates']})",
        "",
        STATS_END,
    ]
    return "\n".join(lines) + "\n"


def update_readme(section: str) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    if STATS_START in text and STATS_END in text:
        pattern = re.compile(
            re.escape(STATS_START) + r".*?" + re.escape(STATS_END),
            flags=re.DOTALL,
        )
        text = pattern.sub(section.strip(), text)
    else:
        anchor = "## Key links"
        if anchor in text:
            text = text.replace(anchor, section + "\n" + anchor, 1)
        else:
            text = text.rstrip() + "\n\n" + section

    README_PATH.write_text(
        text if text.endswith("\n") else text + "\n", encoding="utf-8"
    )


def load_summary() -> dict:
    payload = json.loads((STATS_DIR / "summary.json").read_text(encoding="utf-8"))

    def pairs(key: str) -> list[tuple[str, int]]:
        return [(row["name"], int(row["count"])) for row in payload[key]]

    return {
        "generated_at": payload["generated_at"],
        "totals": payload["totals"],
        "organisms": pairs("organisms"),
        "samples_by_organism": pairs("samples_by_organism"),
        "diseases": pairs("diseases"),
        "labels": pairs("labels"),
        "acquisitions": pairs("acquisitions"),
        "completeness": payload.get("completeness", []),
        "completeness_by_organism": payload.get(
            "completeness_by_organism", []
        ),
        "templates": payload.get("templates", []),
        "specialties": payload.get("specialties", []),
    }


def write_summary(stats: dict) -> None:
    STATS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": stats["generated_at"],
        "totals": stats["totals"],
        "organisms": [
            {"name": k, "count": v} for k, v in stats["organisms"]
        ],
        "samples_by_organism": [
            {"name": k, "count": v}
            for k, v in stats["samples_by_organism"]
        ],
        "diseases": [
            {"name": k, "count": v} for k, v in stats["diseases"]
        ],
        "labels": [{"name": k, "count": v} for k, v in stats["labels"]],
        "acquisitions": [
            {"name": k, "count": v} for k, v in stats["acquisitions"]
        ],
        "completeness": stats.get("completeness", []),
        "completeness_by_organism": stats.get(
            "completeness_by_organism", []
        ),
        "templates": stats.get("templates", []),
        "specialties": stats.get("specialties", []),
    }
    (STATS_DIR / "summary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    plots_only = "--plots-only" in argv

    if plots_only:
        stats = load_summary()
    else:
        stats = aggregate()
        write_summary(stats)

    plot_paths = render_plots(stats)
    update_readme(build_readme_section(stats, plot_paths))

    totals = stats["totals"]
    print("README resource stats refreshed:")
    print(f"  accessions: {totals['accessions']}")
    print(f"  sdrf_files: {totals['sdrf_files']}")
    print(f"  samples:    {totals['samples']}")
    print(f"  runs:       {totals['runs']}")
    print(f"  assay_rows: {totals['assay_rows']}")
    print(
        f"  templates:  {totals.get('accessions_with_template', 0)} "
        "accessions declare a template"
    )
    print(f"  wrote: {STATS_DIR.relative_to(REPO_ROOT)} and README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
