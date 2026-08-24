#!/usr/bin/env python3
"""Aggregate curated SDRF stats and refresh README plots.

Scans datasets/**/*.sdrf.tsv (sandbox excluded), writes:
  docs/stats/summary.json
  docs/stats/plots/*.png
  and replaces the README markers <!-- STATS:START --> ... <!-- STATS:END -->.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

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


def _record_sample(
    state: AggregateState,
    path_key: str,
    source: str,
    row: dict,
    org_col: str | None,
    dis_col: str | None,
    sample_org: dict[str, str],
    sample_dis: dict[str, str],
) -> None:
    key = (path_key, source)
    state.sample_seen.add(key)

    if source not in sample_org and org_col:
        org = normalize_term(row.get(org_col))
        if org:
            sample_org[source] = canonicalize_organism(org)

    if source not in sample_dis and dis_col:
        dis = normalize_term(row.get(dis_col))
        if dis and dis.lower() not in HEALTHY_DISEASE_TOKENS:
            sample_dis[source] = dis


def _process_row(
    state: AggregateState,
    path_key: str,
    row: dict,
    cols: dict[str, str | None],
    sample_org: dict[str, str],
    sample_dis: dict[str, str],
) -> None:
    state.total_rows += 1
    src_col = cols["source"]
    file_col = cols["data_file"]
    source = (row.get(src_col) or "").strip() if src_col else ""
    data_file = (row.get(file_col) or "").strip() if file_col else ""

    if source:
        _record_sample(
            state,
            path_key,
            source,
            row,
            cols["organism"],
            cols["disease"],
            sample_org,
            sample_dis,
        )

    if data_file:
        state.run_seen.add((path_key, data_file))

    lab = classify_label(row.get(cols["label"]) if cols["label"] else None)
    if lab:
        state.labels[lab] += 1

    acq = classify_acquisition(
        row.get(cols["acquisition"]) if cols["acquisition"] else None
    )
    if acq:
        state.acquisitions[acq] += 1


def process_sdrf_file(path: Path, state: AggregateState) -> None:
    accession = path.parent.name
    path_key = path.as_posix()
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        headers = list(reader.fieldnames or [])
        if not headers:
            return

        cols = {
            "organism": find_column(headers, "organism"),
            "disease": find_column(headers, "disease"),
            "label": find_column(headers, "label"),
            "acquisition": find_column(headers, "acquisition"),
            "source": find_column(headers, "source"),
            "data_file": find_column(headers, "data_file"),
        }
        sample_org: dict[str, str] = {}
        sample_dis: dict[str, str] = {}

        for row in reader:
            _process_row(state, path_key, row, cols, sample_org, sample_dis)

        for org in sample_org.values():
            state.samples_by_organism[org] += 1
            state.accession_organisms[accession].add(org)
        for dis in sample_dis.values():
            state.diseases[dis] += 1


def aggregate() -> dict:
    files = iter_sdrf_files()
    state = AggregateState()
    for path in files:
        process_sdrf_file(path, state)

    organisms: Counter = Counter()
    for orgs in state.accession_organisms.values():
        organisms.update(orgs)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "generated_at": generated_at,
        "totals": {
            "accessions": len({p.parent.name for p in files}),
            "sdrf_files": len(files),
            "samples": len(state.sample_seen),
            "runs": len(state.run_seen),
            "assay_rows": state.total_rows,
        },
        "organisms": organisms.most_common(),
        "samples_by_organism": state.samples_by_organism.most_common(),
        "diseases": state.diseases.most_common(),
        "labels": state.labels.most_common(),
        "acquisitions": state.acquisitions.most_common(),
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


def _shorten_label(text: str, max_len: int = 36) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def _empty_plot(path: Path, title: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.text(0.5, 0.5, "No data", ha="center", va="center", fontsize=12)
    ax.set_title(title, fontsize=13, pad=10, fontweight="bold")
    ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def _order_hbar_items(
    items: list[tuple[str, int]],
) -> list[tuple[str, int]]:
    named = [(k, v) for k, v in items if k != "Other"]
    other = [(k, v) for k, v in items if k == "Other"]
    return sorted(named, key=lambda kv: kv[1], reverse=True) + other


def _annotate_hbar_values(
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
        label = f"{value:,} ({pct:.1f}%)" if show_percent else f"{value:,}"
        ax.text(
            bar.get_width() + xmax * 0.02,
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="left",
            fontsize=9,
            color="#24292f",
        )


def hbar_plot(
    path: Path,
    title: str,
    items: list[tuple[str, int]],
    color: str,
    *,
    show_percent: bool = False,
    colors: list[str] | None = None,
) -> None:
    """Horizontal bars — readable long labels, no pie-slice collisions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if not items:
        _empty_plot(path, title)
        return

    ordered = _order_hbar_items(items)
    labels = [_shorten_label(k) for k, _ in ordered]
    values = [v for _, v in ordered]
    total = sum(values) or 1
    n = len(values)

    height = max(3.8, 0.48 * n + 1.6)
    fig, ax = plt.subplots(figsize=(10.0, height))
    y = list(range(n))
    bar_colors = (
        [colors[i % len(colors)] for i in range(n)]
        if colors
        else [color] * n
    )
    bars = ax.barh(
        y,
        values,
        color=bar_colors,
        edgecolor="white",
        linewidth=0.6,
        height=0.72,
    )
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Count", fontsize=10)
    ax.set_title(title, fontsize=13, pad=12, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle=":", alpha=0.45)
    ax.set_axisbelow(True)

    xmax = max(values)
    ax.set_xlim(0, xmax * 1.28)
    _annotate_hbar_values(
        ax,
        bars,
        values,
        total=total,
        xmax=xmax,
        show_percent=show_percent,
    )

    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def render_plots(stats: dict) -> dict[str, str]:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "organisms": "plots/organisms.png",
        "samples_by_organism": "plots/samples_by_organism.png",
        "diseases": "plots/diseases.png",
        "quant_methods": "plots/quant_methods.png",
        "acquisition": "plots/acquisition.png",
    }

    hbar_plot(
        STATS_DIR / paths["organisms"],
        "Organisms by accession count",
        top_with_other(stats["organisms"], 10),
        "#1f6feb",
    )
    hbar_plot(
        STATS_DIR / paths["samples_by_organism"],
        "Samples by organism",
        top_with_other(stats["samples_by_organism"], 10),
        "#098658",
    )
    hbar_plot(
        STATS_DIR / paths["diseases"],
        "Top annotated diseases (healthy/normal excluded)",
        top_with_other(stats["diseases"], 10),
        "#bf3989",
    )
    hbar_plot(
        STATS_DIR / paths["quant_methods"],
        "Assay rows by quantification label",
        stats["labels"],
        "#1f6feb",
        show_percent=True,
        colors=["#1f6feb", "#f78166", "#bf8700", "#8250df", "#6e7781"],
    )
    hbar_plot(
        STATS_DIR / paths["acquisition"],
        "Assay rows by acquisition method",
        stats["acquisitions"],
        "#0969da",
        show_percent=True,
        colors=["#0969da", "#1a7f37", "#9a6700", "#6e7781"],
    )
    return paths


def fmt_int(n: int) -> str:
    return f"{n:,}"


def build_readme_section(stats: dict, plot_paths: dict[str, str]) -> str:
    totals = stats["totals"]
    top_org = stats["organisms"][0][0] if stats["organisms"] else "n/a"
    dia = dict(stats["acquisitions"]).get("DIA", 0)
    tmt = dict(stats["labels"]).get("TMT", 0)
    lfq = dict(stats["labels"]).get("LFQ", 0)

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
        f"| Samples (unique `source name` per file) | "
        f"{fmt_int(totals['samples'])} |",
        f"| Runs (unique `comment[data file]` per file) | "
        f"{fmt_int(totals['runs'])} |",
        f"| Assay rows | {fmt_int(totals['assay_rows'])} |",
        "",
        f"**Highlights:** most common organism is **{top_org}**; "
        f"**{fmt_int(dia)}** DIA assay rows; "
        f"**{fmt_int(tmt)}** TMT and **{fmt_int(lfq)}** LFQ assay rows.",
        "",
        f"![Organisms](docs/stats/{plot_paths['organisms']})",
        "",
        f"![Samples by organism]"
        f"(docs/stats/{plot_paths['samples_by_organism']})",
        "",
        f"![Diseases](docs/stats/{plot_paths['diseases']})",
        "",
        f"![Quantification methods]"
        f"(docs/stats/{plot_paths['quant_methods']})",
        "",
        f"![Acquisition methods]"
        f"(docs/stats/{plot_paths['acquisition']})",
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
    }
    (STATS_DIR / "summary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    stats = aggregate()
    plot_paths = render_plots(stats)
    write_summary(stats)
    update_readme(build_readme_section(stats, plot_paths))

    totals = stats["totals"]
    print("README resource stats refreshed:")
    print(f"  accessions: {totals['accessions']}")
    print(f"  sdrf_files: {totals['sdrf_files']}")
    print(f"  samples:    {totals['samples']}")
    print(f"  runs:       {totals['runs']}")
    print(f"  assay_rows: {totals['assay_rows']}")
    print(f"  wrote: {STATS_DIR.relative_to(REPO_ROOT)} and README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
