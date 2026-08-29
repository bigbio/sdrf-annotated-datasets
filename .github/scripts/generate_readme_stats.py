#!/usr/bin/env python3
"""Aggregate curated SDRF stats and refresh README plots.

Scans datasets/**/*.sdrf.tsv (sandbox excluded), writes:
  docs/stats/summary.json
  docs/stats/plots/{coverage,organisms,diseases,methods,analytical,completeness,templates,contributions}.png
  and replaces the README markers <!-- STATS:START --> ... <!-- STATS:END -->.

Pass --plots-only to redraw figures from an existing summary.json.
"""

from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
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

PROXI_DATASETS_URL = (
    "https://proteomecentral.proteomexchange.org/api/proxi/v0.1/datasets"
)
PRIDE_COUNT_URL = "https://www.ebi.ac.uk/pride/ws/archive/v3/projects/count"
HTTP_UA = (
    "sdrf-annotated-datasets-stats/1.0 "
    "(+https://github.com/bigbio/sdrf-annotated-datasets)"
)
PX_ACCESSION_PREFIXES = ("PXD", "MSV", "JPST", "IPX", "PASS")

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

AGENT_EMAILS = {
    "cursoragent@cursor.com": "Cursor",
    "noreply@anthropic.com": "Claude",
    "198982749+copilot@users.noreply.github.com": "Copilot",
    "175728472+copilot@users.noreply.github.com": "Copilot",
    "annotator@sdrf-skills.local": "SDRF Annotator",
}

AGENT_NAME_PATTERNS = (
    (re.compile(r"cursor", re.I), "Cursor"),
    (re.compile(r"claude", re.I), "Claude"),
    (re.compile(r"copilot", re.I), "Copilot"),
    (re.compile(r"sdrf annotator", re.I), "SDRF Annotator"),
    (re.compile(r"chatgpt|openai", re.I), "ChatGPT"),
    (re.compile(r"\bcodex\b", re.I), "Codex"),
    (re.compile(r"gemini", re.I), "Gemini"),
)

HUMAN_NAME_ALIASES = {
    "ypriverol": "Yasset Perez-Riverol",
    "jeroen van goey": "Jeroen Van Goey",
}

_COAUTHOR_RE = re.compile(
    r"^Co-authored-by:\s*(.+?)\s*<([^>]+)>", flags=re.IGNORECASE
)

# Explicit agent declarations in commit messages, PR bodies, and comments.
# Keep these tight so review-bot copy (CodeRabbit, Copilot reviewer) does not
# count as the annotating agent.
_AGENT_TEXT_PATTERNS = (
    (
        re.compile(
            r"made with \[cursor\]|made with cursor|cursor\.com/agents|"
            r"generated with cursor|co-authored-by:\s*cursor\b",
            re.I,
        ),
        "Cursor",
    ),
    (
        re.compile(
            r"generated with \[claude|generated with claude|"
            r"claude\.com/claude-code|co-authored-by:\s*claude\b",
            re.I,
        ),
        "Claude",
    ),
    (
        re.compile(
            r"copilot-swe-agent|co-authored-by:\s*copilot\b|"
            r"generated with github copilot",
            re.I,
        ),
        "Copilot",
    ),
    (
        re.compile(
            r"sdrf annotator|annotator@sdrf-skills",
            re.I,
        ),
        "SDRF Annotator",
    ),
    (
        re.compile(r"made with chatgpt|generated with chatgpt", re.I),
        "ChatGPT",
    ),
    (
        re.compile(r"generated with (?:openai )?codex|made with (?:openai )?codex", re.I),
        "Codex",
    ),
)

# Same automated annotation pipeline as batches that declared Cursor, but
# later squash-merges dropped Co-authored-by / "Made with Cursor".
_CAMPAIGN_TITLE_RE = re.compile(
    r"easy targets|automated e\.?\s*coli sdrf|escalated pride easy-target",
    re.I,
)
_CAMPAIGN_BODY_RE = re.compile(
    r"synthesi[sz]ed label-free stubs from pride|"
    r"label-free stubs synthesi[sz]ed from pride|"
    r"annotation pipeline recovery",
    re.I,
)
_MIGRATION_TITLE_RE = re.compile(
    r"migrate annotated sdrf|from specification repo|"
    r"from proteomics-sample-metadata",
    re.I,
)
_ANNOTATION_PR_RE = re.compile(
    r"sdrf annotation|easy targets|automated e\.?\s*coli sdrf|"
    r"community sdrf|escalated pride easy-target|"
    r"bulk lfq|tissue-expression sdrf",
    re.I,
)
_MECHANICAL_PR_RE = re.compile(
    r"normalize |corpus cleanup|restore \d|review gate|^chore:|"
    r"mechanical (?:remap|fixes)|reserved-word casing|"
    r"migrate annotated",
    re.I,
)
_PR_NUMBER_SUBJECT_RE = re.compile(r"\(#(\d+)\)\s*$")
_PR_MERGE_SUBJECT_RE = re.compile(r"Merge pull request #(\d+)\b", re.I)
_CODERABBIT_BLOCK_RE = re.compile(
    r"<!-- This is an auto-generated comment:.*?"
    r"<!-- end of auto-generated comment.*?-->",
    flags=re.I | re.S,
)

# GitHub logins that authored the annotation, not review-only bots.
_AGENT_LOGINS = {
    "cursoragent": "Cursor",
    "cursor": "Cursor",
    "copilot-swe-agent": "Copilot",
}
_REVIEW_BOT_LOGINS = {
    "copilot-pull-request-reviewer",
    "coderabbitai",
    "qodo-code-review",
    "github-actions",
    "web-flow",
    "dependabot",
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
_MT_RE = re.compile(r"(?:^|;)\s*MT=([^;]+)", flags=re.IGNORECASE)

RUN_BINS = [
    (1, 1, "1"),
    (2, 2, "2"),
    (3, 4, "3–4"),
    (5, 9, "5–9"),
    (10, 19, "10–19"),
    (20, 49, "20–49"),
    (50, 99, "50–99"),
    (100, 199, "100–199"),
    (200, None, "≥200"),
]

INSTRUMENT_CANON = {
    name.lower(): name
    for name in (
        "Q Exactive",
        "Q Exactive HF",
        "Q Exactive HF-X",
        "Q Exactive Plus",
        "Orbitrap Fusion Lumos",
        "Orbitrap Fusion",
        "Orbitrap Exploris 480",
        "Orbitrap Exploris 240",
        "Orbitrap Astral",
        "Orbitrap Eclipse",
        "Orbitrap Ascend",
        "LTQ Orbitrap",
        "LTQ Orbitrap Velos",
        "LTQ Orbitrap Elite",
        "LTQ Orbitrap XL",
        "timsTOF Pro",
        "timsTOF Pro 2",
        "timsTOF HT",
        "TripleTOF 5600",
        "TripleTOF 5600+",
        "TripleTOF 6600",
        "Orbitrap Tribrid",
        "TSQ Altis",
        "TSQ Vantage",
        "impact II",
        "maXis",
    )
}
INSTRUMENT_CANON.update(
    {
        "q exactive hfx": "Q Exactive HF-X",
        "q-exactive": "Q Exactive",
        "q-exactive hf": "Q Exactive HF",
        "q-exactive hf-x": "Q Exactive HF-X",
        "q-exactive hfx": "Q Exactive HF-X",
        "orbitrap fusion lumos tribrid": "Orbitrap Fusion Lumos",
    }
)

MOD_CANON = {
    "oxidation": "Oxidation",
    "carbamidomethyl": "Carbamidomethyl",
    "acetyl": "Acetyl",
    "phospho": "Phospho",
    "deamidated": "Deamidated",
    "tmt6plex": "TMT6plex",
    "tmt10plex": "TMT10plex",
    "tmt11plex": "TMT11plex",
    "tmtpro": "TMTpro",
    "itraq4plex": "iTRAQ4plex",
    "itraq8plex": "iTRAQ8plex",
    "glygly": "GlyGly",
    "methyl": "Methyl",
    "dimethyl": "Dimethyl",
    "gg": "GlyGly",
    "gln->pyro-glu": "Gln→pyro-Glu",
    "glu->pyro-glu": "Glu→pyro-Glu",
    "gln->pyro glu": "Gln→pyro-Glu",
    "glu->pyro glu": "Glu→pyro-Glu",
    "pyro-glu": "Pyro-Glu",
    "carbamyl": "Carbamyl",
    "cam": "Carbamidomethyl",
}

ENZYME_CANON = {
    "trypsin": "Trypsin",
    "trypsin/p": "Trypsin/P",
    "lys-c": "Lys-C",
    "lys-c/p": "Lys-C/P",
    "lys/c": "Lys-C",
    "chymotrypsin": "Chymotrypsin",
    "glutamyl endopeptidase": "Glu-C",
    "glu-c": "Glu-C",
    "asp-n": "Asp-N",
    "arg-c": "Arg-C",
    "pepsin": "Pepsin",
    "thermolysin": "Thermolysin",
    "proteinase k": "Proteinase K",
    "unspecific cleavage": "Unspecific",
    "no cleavage": "None",
}

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


def canonicalize_instrument(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name).strip()
    if not cleaned:
        return cleaned
    mapped = INSTRUMENT_CANON.get(cleaned.lower())
    if mapped:
        return mapped
    parts = []
    for tok in cleaned.split(" "):
        low = tok.lower()
        if low in {"ltq", "q", "xl", "ht"}:
            parts.append(low.upper())
        elif low in {"hf", "hf-x"}:
            parts.append("HF-X" if "x" in low else "HF")
        elif low == "orbitrap":
            parts.append("Orbitrap")
        elif low == "exactive":
            parts.append("Exactive")
        elif low == "timstof":
            parts.append("timsTOF")
        elif low.startswith("tripletof"):
            parts.append("TripleTOF" + tok[len("tripletof") :])
        else:
            parts.append(tok[:1].upper() + tok[1:] if tok else tok)
    return " ".join(parts)


def canonicalize_mod(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name).strip()
    return MOD_CANON.get(cleaned.lower(), cleaned)


def canonicalize_enzyme(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", name).strip()
    return ENZYME_CANON.get(cleaned.lower(), cleaned)


def parse_modification(raw: str | None) -> tuple[str | None, str | None]:
    """Return (modification name, Fixed|Variable|None) from an SDRF cell."""
    if raw is None:
        return None, None
    text = str(raw).strip()
    if not text or text.lower() in NA_TOKENS:
        return None, None
    keys: dict[str, str] = {}
    for part in text.split(";"):
        part = part.strip()
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        keys[key.strip().upper()] = value.strip()
    name = keys.get("NT") or normalize_term(text)
    if not name or name.lower() in NA_TOKENS:
        return None, None
    mtype = None
    mt = keys.get("MT", "")
    if not mt:
        match = _MT_RE.search(text)
        mt = match.group(1).strip() if match else ""
    if mt:
        low = mt.lower()
        if low.startswith("fix"):
            mtype = "Fixed"
        elif low.startswith("var"):
            mtype = "Variable"
    return canonicalize_mod(name), mtype


def bin_run_count(n: int) -> str:
    for low, high, label in RUN_BINS:
        if high is None:
            if n >= low:
                return label
        elif low <= n <= high:
            return label
    return RUN_BINS[-1][2]


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
        "instrument": lambda hs: find_header(
            hs, lambda h: h == "comment[instrument]"
        ),
        "fraction": lambda hs: find_header(
            hs, lambda h: "fraction identifier" in h
        ),
    }
    if kind not in lookup:
        raise ValueError(f"unknown column kind: {kind}")
    return lookup[kind](headers)


def iter_sdrf_files() -> list[Path]:
    if not DATASETS_DIR.exists():
        return []
    return sorted(DATASETS_DIR.rglob("*.sdrf.tsv"))


def _http_get(url: str, *, timeout: int) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": HTTP_UA, "Accept": "application/json, text/plain"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def _load_previous_coverage() -> dict:
    path = STATS_DIR / "summary.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    cov = payload.get("coverage")
    return cov if isinstance(cov, dict) else {}


def fetch_repository_coverage(accessions: set[str]) -> dict:
    """Compare curated accessions to live ProteomeXchange and PRIDE catalogues."""
    local = {name.upper() for name in accessions}
    px_like = {
        name
        for name in local
        if name.startswith(PX_ACCESSION_PREFIXES)
    }
    pad = {name for name in local if name.startswith("PAD")}
    previous = _load_previous_coverage()
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    coverage = {
        "proteomexchange_public": int(previous.get("proteomexchange_public") or 0),
        "proteomexchange_annotated": len(px_like),
        "pride_public": int(previous.get("pride_public") or 0),
        "pride_annotated": int(previous.get("pride_annotated") or 0),
        "pride_match": previous.get("pride_match") or "prefix",
        "fetched_at": previous.get("fetched_at") or "",
        "source_px": PROXI_DATASETS_URL,
        "source_pride": PRIDE_COUNT_URL,
    }

    try:
        payload = json.loads(_http_get(f"{PROXI_DATASETS_URL}?pageSize=1", timeout=60))
        px_total = int(payload["result_set"]["n_available_rows"])
        if px_total > 0:
            coverage["proteomexchange_public"] = px_total
            coverage["fetched_at"] = fetched_at
        print(f"  ProteomeXchange public datasets: {px_total:,}")
    except (OSError, urllib.error.URLError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"  warning: could not fetch ProteomeXchange catalogue ({exc})")

    pride_ids: set[str] = set()
    try:
        payload = json.loads(
            _http_get(
                f"{PROXI_DATASETS_URL}?repository=PRIDE&pageSize=100000",
                timeout=180,
            )
        )
        pride_ids = {
            str(row[0]).upper()
            for row in payload.get("datasets") or []
            if row
        }
        print(f"  ProteomeCentral PRIDE datasets: {len(pride_ids):,}")
    except (OSError, urllib.error.URLError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"  warning: could not fetch PRIDE accessions from ProteomeCentral ({exc})")

    pride_public = 0
    try:
        pride_public = int(_http_get(PRIDE_COUNT_URL, timeout=45).decode("utf-8").strip())
        if pride_public > 0:
            coverage["pride_public"] = pride_public
            coverage["fetched_at"] = fetched_at
        print(f"  PRIDE Archive projects: {pride_public:,}")
    except (OSError, urllib.error.URLError, TypeError, ValueError) as exc:
        print(f"  warning: could not fetch PRIDE project count ({exc})")
        if not coverage["pride_public"] and pride_ids:
            coverage["pride_public"] = len(pride_ids)

    if pride_ids:
        coverage["pride_annotated"] = len((local & pride_ids) | pad)
        coverage["pride_match"] = "proteomecentral"
    else:
        coverage["pride_annotated"] = len(
            {name for name in local if name.startswith(("PXD", "PAD"))}
        )
        coverage["pride_match"] = "prefix"

    return coverage


def classify_contributor(name: str, email: str) -> str | None:
    """Return an agent label, or None if this looks like a human identity."""
    email_l = (email or "").strip().lower()
    name_s = (name or "").strip()
    if email_l in AGENT_EMAILS:
        return AGENT_EMAILS[email_l]
    for pattern, label in AGENT_NAME_PATTERNS:
        if pattern.search(name_s) or pattern.search(email_l):
            return label
    return None


def _is_ignored_identity(name: str, email: str) -> bool:
    """Bots and empty identities are neither human nor AI contributors."""
    email_l = (email or "").strip().lower()
    name_s = (name or "").strip()
    if not name_s and not email_l:
        return True
    lowered = name_s.lower()
    if lowered.endswith("[bot]"):
        return True
    if lowered in {"github actions", "dependabot", "web-flow"}:
        return True
    if "github-actions" in email_l:
        return True
    return False


def _human_key(name: str, email: str) -> str:
    """Stable identity for unique-contributor counts; never published."""
    cleaned = re.sub(r"\s+", " ", (name or "")).strip()
    if cleaned:
        return HUMAN_NAME_ALIASES.get(cleaned.lower(), cleaned)
    return (email or "").strip().lower()


def _add_identity(
    name: str, email: str, agents: set[str], humans: set[str]
) -> None:
    label = classify_contributor(name, email)
    if label:
        agents.add(label)
        return
    if _is_ignored_identity(name, email):
        return
    key = _human_key(name, email)
    if key:
        humans.add(key)


def _strip_bot_boilerplate(text: str) -> str:
    """Drop CodeRabbit / similar auto-inserted PR blocks before scanning."""
    if not text:
        return ""
    return _CODERABBIT_BLOCK_RE.sub(" ", text)


def _parse_agent_text(text: str) -> set[str]:
    """Agent labels declared in free text (commit / PR / comment)."""
    labels: set[str] = set()
    if not text:
        return labels
    for pattern, label in _AGENT_TEXT_PATTERNS:
        if pattern.search(text):
            labels.add(label)
    return labels


def _campaign_agent(title: str, body: str = "") -> str | None:
    """Cursor campaigns that later dropped explicit trailers on squash."""
    if _MIGRATION_TITLE_RE.search(title or ""):
        return None
    if _CAMPAIGN_TITLE_RE.search(title or ""):
        return "Cursor"
    if _CAMPAIGN_BODY_RE.search(f"{title or ''}\n{body or ''}"):
        return "Cursor"
    return None


def _normalize_github_login(login: str) -> str:
    lowered = (login or "").strip().lower()
    if lowered.startswith("app/"):
        lowered = lowered[4:]
    if lowered.endswith("[bot]"):
        lowered = lowered[:-5]
    return lowered


def _agent_from_login(login: str) -> str | None:
    return _AGENT_LOGINS.get(_normalize_github_login(login))


def _pr_number_from_subject(subject: str) -> int | None:
    text = (subject or "").strip()
    match = _PR_NUMBER_SUBJECT_RE.search(text)
    if match:
        return int(match.group(1))
    match = _PR_MERGE_SUBJECT_RE.search(text)
    if match:
        return int(match.group(1))
    return None


def _is_annotation_pr(title: str) -> bool:
    """PRs that (re)annotate datasets, not corpus-wide mechanical edits."""
    title = title or ""
    if _MECHANICAL_PR_RE.search(title) or _MIGRATION_TITLE_RE.search(title):
        return False
    return bool(_ANNOTATION_PR_RE.search(title) or _CAMPAIGN_TITLE_RE.search(title))


def _parse_commit_identities(author_name: str, author_email: str, body: str):
    agents: set[str] = set()
    humans: set[str] = set()
    _add_identity(author_name, author_email, agents, humans)
    for line in body.splitlines():
        match = _COAUTHOR_RE.match(line.strip())
        if not match:
            continue
        _add_identity(match.group(1), match.group(2), agents, humans)
    agents.update(_parse_agent_text(body))
    subject = body.splitlines()[0] if body.strip() else ""
    campaign = _campaign_agent(subject, body)
    if campaign:
        agents.add(campaign)
    return agents, humans


def _git_output(args: list[str], *, timeout: int) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), *args],
            text=True,
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return ""


def _git_commit_identities() -> dict[str, tuple[frozenset[str], frozenset[str]]]:
    """Map commit SHA to agent labels and human identities (for counts only)."""
    raw = _git_output(
        ["log", "--pretty=format:%H%x00%an%x00%ae%x00%s%x00%B%x1e"],
        timeout=120,
    )
    identities: dict[str, tuple[frozenset[str], frozenset[str]]] = {}
    for record in raw.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split("\x00", 4)
        if len(parts) != 5:
            continue
        sha, name, email, subject, body = parts
        agents, humans = _parse_commit_identities(name, email, body)
        campaign = _campaign_agent(subject, body)
        if campaign:
            agents.add(campaign)
        identities[sha] = (frozenset(agents), frozenset(humans))
    return identities


def _git_first_add_paths() -> dict[str, str]:
    """Map datasets/ path to the oldest commit that added it."""
    raw = _git_output(
        [
            "log",
            "--reverse",
            "--diff-filter=A",
            "--name-only",
            "--pretty=format:COMMIT %H",
            "--",
            "datasets",
        ],
        timeout=180,
    )
    first: dict[str, str] = {}
    sha = None
    for line in raw.splitlines():
        if line.startswith("COMMIT "):
            sha = line.split(" ", 1)[1].strip()
            continue
        path = line.strip()
        if sha and path.endswith(".sdrf.tsv") and path not in first:
            first[path] = sha
    return first


def _git_pr_file_map(*, diff_filter: str) -> dict[int, set[str]]:
    """Map GitHub PR number → datasets/ SDRF paths from squash/merge commits."""
    raw = _git_output(
        [
            "log",
            f"--diff-filter={diff_filter}",
            "--name-only",
            "--pretty=format:COMMIT %s",
            "--",
            "datasets",
        ],
        timeout=180,
    )
    mapping: dict[int, set[str]] = defaultdict(set)
    pr_number = None
    for line in raw.splitlines():
        if line.startswith("COMMIT "):
            pr_number = _pr_number_from_subject(line[len("COMMIT ") :])
            continue
        path = line.strip()
        if pr_number and path.endswith(".sdrf.tsv"):
            mapping[pr_number].add(path)
    return mapping


def _git_first_add_for_path(rel: str) -> tuple[str, str, str] | None:
    out = _git_output(
        [
            "log",
            "--follow",
            "--diff-filter=A",
            "-1",
            "--pretty=format:%an%x09%ae%n%B",
            "--",
            rel,
        ],
        timeout=15,
    )
    if not out.strip():
        return None
    first, _, rest = out.partition("\n")
    if "\t" not in first:
        return None
    name, email = first.split("\t", 1)
    return name, email, rest


def _github_token() -> str:
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        value = (os.environ.get(key) or "").strip()
        if value:
            return value
    try:
        return subprocess.check_output(
            ["gh", "auth", "token"],
            text=True,
            errors="replace",
            timeout=10,
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def _origin_repo() -> tuple[str, str]:
    url = _git_output(["remote", "get-url", "origin"], timeout=10).strip()
    url = re.sub(r"\.git$", "", url)
    match = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/]+)$", url)
    if match:
        return match.group("owner"), match.group("repo")
    return "bigbio", "sdrf-annotated-datasets"


def _github_graphql(query: str, variables: dict, token: str) -> dict:
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": HTTP_UA,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        parsed = json.loads(response.read().decode("utf-8"))
    if parsed.get("errors"):
        message = parsed["errors"][0].get("message", "GraphQL error")
        raise RuntimeError(message)
    return parsed.get("data") or {}


def _fetch_merged_pull_requests() -> tuple[list[dict], str]:
    """Merged PRs with title/body/commits/comments for agent evidence."""
    token = _github_token()
    if not token:
        print("  warning: no GitHub token; PR comment/body scan skipped")
        return [], "skipped"

    owner, repo = _origin_repo()
    query = """
    query($owner: String!, $name: String!, $cursor: String) {
      repository(owner: $owner, name: $name) {
        pullRequests(
          states: MERGED
          first: 25
          after: $cursor
          orderBy: {field: CREATED_AT, direction: ASC}
        ) {
          pageInfo { hasNextPage endCursor }
          nodes {
            number
            title
            body
            headRefName
            author { login }
            commits(first: 40) {
              nodes {
                commit {
                  message
                  authors(first: 8) {
                    nodes { name email user { login } }
                  }
                }
              }
            }
            comments(first: 40) {
              nodes { author { login } body }
            }
            reviews(first: 20) {
              nodes {
                author { login }
                body
                comments(first: 15) {
                  nodes { author { login } body }
                }
              }
            }
          }
        }
      }
    }
    """
    nodes: list[dict] = []
    cursor = None
    try:
        while True:
            data = _github_graphql(
                query,
                {"owner": owner, "name": repo, "cursor": cursor},
                token,
            )
            pull_requests = (
                ((data.get("repository") or {}).get("pullRequests")) or {}
            )
            nodes.extend(pull_requests.get("nodes") or [])
            page = pull_requests.get("pageInfo") or {}
            if not page.get("hasNextPage"):
                break
            cursor = page.get("endCursor")
    except (OSError, urllib.error.URLError, RuntimeError, TimeoutError, ValueError) as exc:
        print(f"  warning: GitHub PR fetch failed ({exc})")
        return nodes, "failed"
    print(f"  scanned {len(nodes)} merged PRs for agent evidence")
    return nodes, "ok"


def _walk_pr_comment_nodes(pr: dict):
    for comment in (pr.get("comments") or {}).get("nodes") or []:
        yield comment
    for review in (pr.get("reviews") or {}).get("nodes") or []:
        yield review
        for comment in (review.get("comments") or {}).get("nodes") or []:
            yield comment


def _classify_pull_request_agents(pr: dict) -> set[str]:
    title = pr.get("title") or ""
    if _MIGRATION_TITLE_RE.search(title):
        return set()

    labels: set[str] = set()
    author_login = ((pr.get("author") or {}) or {}).get("login") or ""
    login_agent = _agent_from_login(author_login)
    if login_agent:
        labels.add(login_agent)

    head = pr.get("headRefName") or ""
    if head.lower().startswith("cursor/"):
        labels.add("Cursor")

    body = _strip_bot_boilerplate(f"{title}\n{pr.get('body') or ''}")
    labels.update(_parse_agent_text(body))
    campaign = _campaign_agent(title, pr.get("body") or "")
    if campaign:
        labels.add(campaign)

    for node in (pr.get("commits") or {}).get("nodes") or []:
        commit = node.get("commit") or {}
        message = commit.get("message") or ""
        labels.update(_parse_agent_text(message))
        subject = message.splitlines()[0] if message else ""
        campaign = _campaign_agent(subject, message)
        if campaign:
            labels.add(campaign)
        for actor in (commit.get("authors") or {}).get("nodes") or []:
            user_login = ((actor.get("user") or {}) or {}).get("login") or ""
            ident = _agent_from_login(user_login)
            if ident:
                labels.add(ident)
            agents: set[str] = set()
            humans: set[str] = set()
            _add_identity(
                actor.get("name") or "",
                actor.get("email") or "",
                agents,
                humans,
            )
            labels.update(agents)

    for comment in _walk_pr_comment_nodes(pr):
        login = ((comment.get("author") or {}) or {}).get("login") or ""
        if _normalize_github_login(login) in _REVIEW_BOT_LOGINS:
            continue
        ident = _agent_from_login(login)
        if ident:
            labels.add(ident)
        labels.update(_parse_agent_text(_strip_bot_boilerplate(comment.get("body") or "")))
    return labels


def collect_contributions(current_files: list[Path]) -> dict:
    """Attribute current datasets/ SDRFs using first-add git history and PRs.

    A file is agent-assisted if the commit that first added it, or a merged
    annotation PR (title, description, commits, or comments), shows an AI
    agent. Review bots and corpus-wide mechanical cleanups are ignored.
    PRIDE easy-target and automated E. coli campaigns count as Cursor when
    later squash-merges dropped Co-authored-by trailers. Migration-only PRs
    are not treated as annotation evidence.
    """
    current = {p.resolve().relative_to(REPO_ROOT).as_posix() for p in current_files}
    file_agents: dict[str, set[str]] = defaultdict(set)
    file_humans: dict[str, set[str]] = defaultdict(set)

    identities = _git_commit_identities()
    added = _git_first_add_paths()

    for path in current:
        sha = added.get(path)
        if sha and sha in identities:
            agents, humans = identities[sha]
            file_agents[path].update(agents)
            file_humans[path].update(humans)

    for path in sorted(current):
        if path in file_agents or path in file_humans:
            continue
        ident = _git_first_add_for_path(path)
        if not ident:
            continue
        name, email, body = ident
        agents, humans = _parse_commit_identities(name, email, body)
        file_agents[path].update(agents)
        file_humans[path].update(humans)

    pr_added = _git_pr_file_map(diff_filter="A")
    pr_modified = _git_pr_file_map(diff_filter="M")
    pull_requests, pr_fetch = _fetch_merged_pull_requests()
    prs_with_agent = 0
    for pr in pull_requests:
        labels = _classify_pull_request_agents(pr)
        if not labels:
            continue
        number = int(pr.get("number") or 0)
        title = pr.get("title") or ""
        if _MECHANICAL_PR_RE.search(title) or _MIGRATION_TITLE_RE.search(title):
            continue
        prs_with_agent += 1
        for path in pr_added.get(number, ()):
            if path in current:
                file_agents[path].update(labels)
        if _is_annotation_pr(title):
            for path in pr_modified.get(number, ()):
                if path in current:
                    file_agents[path].update(labels)

    acc_agents: dict[str, set[str]] = defaultdict(set)
    file_agent_counts: Counter = Counter()
    file_origin = Counter()
    acc_origin: dict[str, str] = {}
    all_humans: set[str] = set()
    attributed = 0

    for path in current:
        agents = file_agents.get(path, set())
        humans = file_humans.get(path, set())
        if not agents and not humans:
            continue
        attributed += 1
        accession = Path(path).parent.name
        all_humans.update(humans)
        if agents:
            file_origin["Agent-assisted"] += 1
            acc_origin[accession] = "Agent-assisted"
            for agent in agents:
                file_agent_counts[agent] += 1
                acc_agents[accession].add(agent)
        elif humans:
            file_origin["Human-only"] += 1
            acc_origin.setdefault(accession, "Human-only")

    origin_acc = Counter(acc_origin.values())
    agent_acc: Counter = Counter()
    for agents in acc_agents.values():
        agent_acc.update(agents)

    print(
        "  contributions: "
        f"{int(origin_acc.get('Agent-assisted', 0)):,} agent-assisted / "
        f"{int(origin_acc.get('Human-only', 0)):,} human-only accessions "
        f"({pr_fetch} PR scan, {prs_with_agent} PRs with agent evidence)"
    )

    return {
        "attributed_files": attributed,
        "unattributed_files": len(current) - attributed,
        "human_contributors": len(all_humans),
        "ai_agents": len(agent_acc),
        "github_prs_scanned": len(pull_requests),
        "github_prs_with_agent": prs_with_agent,
        "github_pr_fetch": pr_fetch,
        "origin": [
            {
                "name": "Human-only",
                "accessions": int(origin_acc.get("Human-only", 0)),
                "files": int(file_origin.get("Human-only", 0)),
            },
            {
                "name": "Agent-assisted",
                "accessions": int(origin_acc.get("Agent-assisted", 0)),
                "files": int(file_origin.get("Agent-assisted", 0)),
            },
        ],
        "agents": [
            {
                "name": name,
                "accessions": count,
                "files": int(file_agent_counts[name]),
            }
            for name, count in agent_acc.most_common()
        ],
    }


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
    accession_instruments: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    accession_mods: dict[str, dict[str, set[str]]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(set))
    )
    accession_enzymes: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    accession_run_files: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )
    accession_fractions: dict[str, set[str]] = field(
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
                "instrument",
                "fraction",
            )
        }
        tmpl_idxs = [
            i
            for i, header in enumerate(headers)
            if header.lower() == "comment[sdrf template]"
        ]
        mod_idxs = [
            i
            for i, header in enumerate(headers)
            if "modification parameter" in header.lower()
        ]
        cleav_idxs = [
            i
            for i, header in enumerate(headers)
            if "cleavage agent" in header.lower()
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
                state.accession_run_files[accession].add(data_file)

            inst = normalize_term(_cell(row, idx["instrument"]) or None)
            if inst:
                state.accession_instruments[accession].add(
                    canonicalize_instrument(inst)
                )
            frac = _cell(row, idx["fraction"]).strip()
            if frac and completeness_status(frac) == "filled":
                state.accession_fractions[accession].add(frac.lower())
            for mi in mod_idxs:
                mod_name, mtype = parse_modification(_cell(row, mi) or None)
                if mod_name:
                    state.accession_mods[accession][mod_name].add(
                        mtype or "Unspecified"
                    )
            for ci in cleav_idxs:
                enzyme = normalize_term(_cell(row, ci) or None)
                if enzyme:
                    state.accession_enzymes[accession].add(
                        canonicalize_enzyme(enzyme)
                    )

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

    instruments: Counter = Counter()
    for insts in state.accession_instruments.values():
        instruments.update(insts)

    modifications: Counter = Counter()
    mod_types: Counter = Counter()
    for mods in state.accession_mods.values():
        for name, types in mods.items():
            modifications[name] += 1
            if "Variable" in types:
                mod_types["Variable"] += 1
            elif "Fixed" in types:
                mod_types["Fixed"] += 1
            else:
                mod_types["Unspecified"] += 1

    enzymes: Counter = Counter()
    for enz in state.accession_enzymes.values():
        enzymes.update(enz)

    run_counts = [len(files_) for files_ in state.accession_run_files.values()]
    run_bins: Counter = Counter()
    for n in run_counts:
        run_bins[bin_run_count(n)] += 1
    run_bin_rows = [
        {"name": label, "count": int(run_bins.get(label, 0))}
        for _lo, _hi, label in RUN_BINS
    ]
    run_sorted = sorted(run_counts)
    median_runs = 0
    if run_sorted:
        mid = len(run_sorted) // 2
        if len(run_sorted) % 2:
            median_runs = run_sorted[mid]
        else:
            median_runs = int(
                round((run_sorted[mid - 1] + run_sorted[mid]) / 2)
            )
    n_fractionated = sum(
        1 for fracs in state.accession_fractions.values() if len(fracs) > 1
    )

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
            "instruments": len(instruments),
            "median_runs": median_runs,
            "max_runs": max(run_counts) if run_counts else 0,
            "accessions_with_mods": len(state.accession_mods),
            "fractionated_accessions": n_fractionated,
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
        "contributions": collect_contributions(files),
        "instruments": instruments.most_common(),
        "modifications": modifications.most_common(),
        "modification_types": mod_types.most_common(),
        "enzymes": enzymes.most_common(),
        "run_bins": run_bin_rows,
        "coverage": fetch_repository_coverage({p.parent.name for p in files}),
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


def _draw_vbar(
    ax,
    items: list[tuple[str, int]],
    *,
    color: str = "#1F4E79",
    xlabel: str = "",
    ylabel: str = "Accessions",
) -> None:
    if not items:
        ax.set_axis_off()
        ax.text(0.5, 0.5, "No data", ha="center", va="center", color=MUTED)
        return
    names = [k for k, _ in items]
    values = [v for _, v in items]
    x = list(range(len(names)))
    bars = ax.bar(
        x,
        values,
        color=color,
        edgecolor=FACE,
        linewidth=0.6,
        width=0.78,
        zorder=3,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=8.5)
    ymax = max(values) if values else 1
    ax.set_ylim(0, ymax * 1.22)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID, linewidth=0.7, linestyle="-")
    ax.tick_params(axis="x", length=0, pad=4)
    ax.tick_params(axis="y", length=3, width=0.6, color=AXIS)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(AXIS)
    ax.yaxis.set_major_formatter(FuncFormatter(_count_tick))
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9, color=MUTED, labelpad=6)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9, color=MUTED, labelpad=6)
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + ymax * 0.03,
            f"{value:,}",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=INK,
            clip_on=False,
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


def _draw_coverage_bar(
    ax,
    *,
    letter: str,
    title: str,
    annotated: int,
    total: int,
    color: str,
) -> None:
    _panel_title(ax, letter, title)
    if total <= 0:
        ax.set_axis_off()
        ax.text(0.5, 0.35, "Catalogue total unavailable", ha="center", va="center", color=MUTED)
        return
    pct = 100.0 * annotated / total
    ax.barh([0], [100], color="#EEF1F4", height=0.42, zorder=1, linewidth=0)
    ax.barh([0], [pct], color=color, height=0.42, zorder=2, linewidth=0)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.95, 0.72)
    ax.set_yticks([])
    ax.tick_params(axis="x", length=3, width=0.6, color=AXIS, labelsize=8.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{int(v)}%"))
    ax.set_xlabel("% of public datasets", fontsize=9, color=MUTED, labelpad=4)
    label_x = pct + 1.8 if pct < 82 else max(pct - 2.0, 1)
    ax.text(
        label_x,
        0,
        f"{pct:.1f}%",
        ha="left" if pct < 82 else "right",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=INK if pct < 82 else FACE,
        zorder=3,
    )
    ax.text(
        0,
        -0.72,
        f"{annotated:,} curated SDRFs  ·  {total:,} public datasets",
        ha="left",
        va="center",
        fontsize=8.5,
        color=MUTED,
        clip_on=False,
    )


def render_coverage_figure(path: Path, coverage: dict) -> None:
    px_ann = int(coverage.get("proteomexchange_annotated") or 0)
    px_tot = int(coverage.get("proteomexchange_public") or 0)
    pride_ann = int(coverage.get("pride_annotated") or 0)
    pride_tot = int(coverage.get("pride_public") or 0)
    if not px_tot and not pride_tot:
        _empty_figure(path, "Annotation coverage")
        return

    fetched = str(coverage.get("fetched_at") or "")
    when = f" Catalogue totals fetched {fetched[:10]}." if fetched else ""
    fig, axes = _make_figure(
        nrows=2,
        ncols=1,
        figsize=(10.4, 5.4),
        title="How much of public proteomics is annotated?",
        subtitle=(
            "Share of public ProteomeXchange and PRIDE datasets with a curated "
            f"SDRF in this repository. Open a PR to move the bar.{when}"
        ),
        hspace=0.55,
        left=0.06,
        right=0.97,
        bottom=0.10,
        header_ratio=0.28,
    )
    _draw_coverage_bar(
        axes[0],
        letter="A",
        title="ProteomeXchange",
        annotated=px_ann,
        total=px_tot,
        color="#1F4E79",
    )
    _draw_coverage_bar(
        axes[1],
        letter="B",
        title="PRIDE",
        annotated=pride_ann,
        total=pride_tot,
        color="#1A7F7A",
    )
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

ORIGIN_COLORS = {
    "Human": "#1F4E79",
    "Human-only": "#1F4E79",
    "AI-assisted": "#D36B2F",
    "Agent-assisted": "#D36B2F",
}

MOD_TYPE_COLORS = {
    "Fixed": "#1F4E79",
    "Variable": "#D36B2F",
    "Unspecified": OTHER_COLOR,
}

PTM_COLORS = {
    "Carbamidomethyl": "#1F4E79",
    "Oxidation": "#D36B2F",
    "Acetyl": "#1A7F7A",
    "Phospho": "#8E4A73",
    "Deamidated": "#2E86AB",
    "TMT6plex": "#C4922A",
    "TMT10plex": "#C4922A",
    "TMTpro": "#C44536",
    "GlyGly": "#3D8B5C",
    "Methyl": "#5C6B8A",
}

ENZYME_COLORS = {
    "Trypsin": "#1F4E79",
    "Trypsin/P": "#2E86AB",
    "Lys-C": "#1A7F7A",
    "Lys-C/P": "#3D8B5C",
    "Chymotrypsin": "#D36B2F",
    "Glu-C": "#8E4A73",
    "Asp-N": "#C4922A",
    "Arg-C": "#5C6B8A",
}

AGENT_COLORS = {
    "Cursor": "#F54E00",
    "Claude": "#D97757",
    "Copilot": "#6E40C9",
    "SDRF Annotator": "#1A7F7A",
    "ChatGPT": "#10A37F",
    "Codex": "#3D8B5C",
    "Gemini": "#4285F4",
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


def render_analytical_figure(
    path: Path,
    instruments: list[tuple[str, int]],
    run_bins: list[dict],
    modifications: list[tuple[str, int]],
    enzymes: list[tuple[str, int]],
    totals: dict,
) -> None:
    if not instruments and not run_bins and not modifications:
        _empty_figure(path, "Mass spectrometry setup")
        return

    n_inst = int(totals.get("instruments", 0))
    median_runs = int(totals.get("median_runs", 0))
    n_frac = int(totals.get("fractionated_accessions", 0))
    n_mod_acc = int(totals.get("accessions_with_mods", 0))
    n_acc = int(totals.get("accessions", 0))
    top_enzyme = enzymes[0][0] if enzymes else None
    n_enzyme = enzymes[0][1] if enzymes else 0
    enzyme_note = (
        f"{top_enzyme} in {n_enzyme:,} accessions."
        if top_enzyme
        else "enzyme rarely declared."
    )
    fig, axes = _make_figure(
        nrows=2,
        ncols=2,
        figsize=(10.4, 8.8),
        title="Instruments, runs, and modifications",
        subtitle=(
            f"{n_inst:,} distinct instruments; median {median_runs:,} runs per "
            f"accession; {n_frac:,} fractionated. "
            f"{n_mod_acc:,} of {n_acc:,} accessions declare modification "
            f"parameters; {enzyme_note}"
        ),
        hspace=0.42,
        wspace=0.30,
        left=0.18,
        right=0.97,
        bottom=0.08,
        header_ratio=0.16,
    )

    _panel_title(axes[0][0], "A", "Mass spectrometer")
    inst_items = top_with_other(instruments, 10)
    inst_map = _organism_colors([k for k, _ in inst_items])
    inst_colors = [inst_map.get(n, OTHER_COLOR) for n, _ in inst_items]
    _draw_hbar(
        axes[0][0],
        inst_items,
        colors=inst_colors,
        xlabel="Accessions",
    )

    _panel_title(axes[0][1], "B", "Runs per accession")
    bin_items = [(row["name"], int(row["count"])) for row in run_bins]
    _draw_vbar(
        axes[0][1],
        bin_items,
        color="#1A7F7A",
        xlabel="Unique comment[data file] values",
        ylabel="Accessions",
    )

    _panel_title(axes[1][0], "C", "Modifications (PTMs)")
    mod_items = top_with_other(modifications, 10)
    mod_colors = [PTM_COLORS.get(name, "#5C6B8A") for name, _ in mod_items]
    _draw_hbar(
        axes[1][0],
        mod_items,
        colors=mod_colors,
        xlabel="Accessions",
    )

    _panel_title(axes[1][1], "D", "Digestion enzyme")
    enz_items = top_with_other(enzymes, 8)
    enz_colors = [ENZYME_COLORS.get(name, OTHER_COLOR) for name, _ in enz_items]
    _draw_hbar(
        axes[1][1],
        enz_items,
        colors=enz_colors,
        xlabel="Accessions",
    )

    _save(fig, path)


def render_contributions_figure(path: Path, contributions: dict) -> None:
    origin = contributions.get("origin") or []
    agents = contributions.get("agents") or []
    if not origin and not agents:
        _empty_figure(path, "Contributions")
        return

    unattr = int(contributions.get("unattributed_files", 0))
    attributed = int(contributions.get("attributed_files", 0))
    extra = (
        f"{unattr:,} current files could not be matched to an add commit."
        if unattr
        else f"{attributed:,} current SDRF files attributed from git history."
    )

    fig, axes = _make_figure(
        nrows=1,
        ncols=3,
        figsize=(10.4, 4.8),
        title="Human and AI annotation",
        subtitle=(
            "First-add git commit plus merged annotation PRs (title, body, "
            "commits, comments). Review bots and corpus-wide cleanups are "
            "ignored. PRIDE easy-target and automated E. coli campaigns count "
            f"as Cursor when squash-merges dropped the trailer. {extra}"
        ),
        width_ratios=[1.15, 1.0, 1.55],
        wspace=0.18,
        left=0.04,
        right=0.97,
        bottom=0.12,
        header_ratio=0.28,
    )

    origin_rename = {
        "Human-only": "Human",
        "Agent-assisted": "AI-assisted",
    }
    origin_items = [
        (
            origin_rename.get(row["name"], row["name"]),
            int(row["accessions"]),
        )
        for row in origin
        if int(row["accessions"])
    ]
    _panel_title(axes[0], "A", "Human vs AI")
    _draw_donut(
        axes[0],
        origin_items,
        color_map=ORIGIN_COLORS,
        center_caption="accessions",
        legend="none",
    )
    axes[1].set_title(" ", pad=8)
    _draw_color_key(axes[1], origin_items, ORIGIN_COLORS)

    _panel_title(axes[2], "B", "AI agent")
    agent_items = [
        (row["name"], int(row["accessions"]))
        for row in agents
        if int(row["accessions"])
    ]
    agent_colors = [
        AGENT_COLORS.get(name, OTHER_COLOR) for name, _ in agent_items
    ]
    _draw_hbar(
        axes[2],
        agent_items,
        colors=agent_colors,
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
        "coverage": "plots/coverage.png",
        "organisms": "plots/organisms.png",
        "diseases": "plots/diseases.png",
        "methods": "plots/methods.png",
        "analytical": "plots/analytical.png",
        "completeness": "plots/completeness.png",
        "templates": "plots/templates.png",
        "contributions": "plots/contributions.png",
    }

    render_coverage_figure(
        STATS_DIR / paths["coverage"],
        stats.get("coverage") or {},
    )
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
    render_analytical_figure(
        STATS_DIR / paths["analytical"],
        stats.get("instruments") or [],
        stats.get("run_bins") or [],
        stats.get("modifications") or [],
        stats.get("enzymes") or [],
        stats.get("totals") or {},
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
    render_contributions_figure(
        STATS_DIR / paths["contributions"],
        stats.get("contributions") or {},
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
    contrib = stats.get("contributions") or {}
    origin_map = {row["name"]: int(row["accessions"]) for row in contrib.get("origin", [])}
    n_human = origin_map.get("Human-only", 0)
    n_agent = origin_map.get("Agent-assisted", 0)
    n_people = int(contrib.get("human_contributors") or 0)
    n_ai_agents = int(
        contrib.get("ai_agents") or len(contrib.get("agents") or [])
    )
    top_agent = (
        contrib.get("agents", [{}])[0].get("name") if contrib.get("agents") else None
    )
    n_instruments = int(totals.get("instruments", 0))
    median_runs = int(totals.get("median_runs", 0))
    n_mod_acc = int(totals.get("accessions_with_mods", 0))
    top_inst = stats["instruments"][0][0] if stats.get("instruments") else None
    top_mod = (
        stats["modifications"][0][0] if stats.get("modifications") else None
    )
    coverage = stats.get("coverage") or {}
    px_ann = int(coverage.get("proteomexchange_annotated") or 0)
    px_tot = int(coverage.get("proteomexchange_public") or 0)
    pride_ann = int(coverage.get("pride_annotated") or 0)
    pride_tot = int(coverage.get("pride_public") or 0)
    px_pct = 100.0 * px_ann / px_tot if px_tot else 0.0
    pride_pct = 100.0 * pride_ann / pride_tot if pride_tot else 0.0

    completeness_bits = []
    if disease_pct is not None:
        completeness_bits.append(f"disease {disease_pct:.0f}%")
    if age_pct is not None:
        completeness_bits.append(f"age {age_pct:.0f}%")

    highlight_parts = [
        f"most common organism is **{top_org}**",
        f"**{fmt_int(dia)}** DIA assay rows",
        f"**{fmt_int(tmt)}** TMT and **{fmt_int(lfq)}** LFQ assay rows",
        f"**{fmt_int(n_single)}** single-cell, **{fmt_int(n_cell)}** cell-line, "
        f"and **{fmt_int(n_meta)}** metaproteomics accessions",
    ]
    if completeness_bits:
        highlight_parts.append(
            "sample-field completeness (applicable samples): "
            + ", ".join(completeness_bits)
        )
    if n_agent:
        agent_bit = f"**{fmt_int(n_agent)}** accessions are agent-assisted"
        if top_agent:
            agent_bit += f" (mostly **{top_agent}**)"
        highlight_parts.append(agent_bit)
    if top_inst:
        highlight_parts.append(f"most common instrument is **{top_inst}**")
    if top_mod:
        highlight_parts.append(f"most common modification is **{top_mod}**")
    if px_tot:
        highlight_parts.append(
            f"**{px_pct:.1f}%** of public ProteomeXchange datasets have a "
            "curated SDRF here"
        )
    if pride_tot:
        highlight_parts.append(
            f"**{pride_pct:.1f}%** of PRIDE projects are annotated"
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
        f"| Human contributors | {fmt_int(n_people)} |",
        f"| AI agents | {fmt_int(n_ai_agents)} |",
        f"| Human-only accessions | {fmt_int(n_human)} |",
        f"| Agent-assisted accessions | {fmt_int(n_agent)} |",
        f"| Distinct instruments | {fmt_int(n_instruments)} |",
        f"| Median runs per accession | {fmt_int(median_runs)} |",
        f"| Accessions with modification parameters | {fmt_int(n_mod_acc)} |",
        (
            f"| ProteomeXchange coverage | {fmt_int(px_ann)} / {fmt_int(px_tot)} "
            f"({px_pct:.1f}%) |"
            if px_tot
            else f"| ProteomeXchange datasets annotated | {fmt_int(px_ann)} |"
        ),
        (
            f"| PRIDE coverage | {fmt_int(pride_ann)} / {fmt_int(pride_tot)} "
            f"({pride_pct:.1f}%) |"
            if pride_tot
            else f"| PRIDE datasets annotated | {fmt_int(pride_ann)} |"
        ),
        "",
        "**Highlights:** " + "; ".join(highlight_parts) + ".",
        "",
        f"![How much of public proteomics is annotated]"
        f"(docs/stats/{plot_paths['coverage']})",
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
        f"![Instruments, runs, and modifications]"
        f"(docs/stats/{plot_paths['analytical']})",
        "",
        f"![Annotation completeness]"
        f"(docs/stats/{plot_paths['completeness']})",
        "",
        f"![Templates and specialized collections]"
        f"(docs/stats/{plot_paths['templates']})",
        "",
        f"![Human and AI annotation]"
        f"(docs/stats/{plot_paths['contributions']})",
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
        "contributions": payload.get("contributions") or {},
        "instruments": pairs("instruments") if "instruments" in payload else [],
        "modifications": pairs("modifications")
        if "modifications" in payload
        else [],
        "modification_types": pairs("modification_types")
        if "modification_types" in payload
        else [],
        "enzymes": pairs("enzymes") if "enzymes" in payload else [],
        "run_bins": payload.get("run_bins") or [],
        "coverage": payload.get("coverage") or {},
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
        "contributions": stats.get("contributions") or {},
        "instruments": [
            {"name": k, "count": v} for k, v in stats.get("instruments") or []
        ],
        "modifications": [
            {"name": k, "count": v}
            for k, v in stats.get("modifications") or []
        ],
        "modification_types": [
            {"name": k, "count": v}
            for k, v in stats.get("modification_types") or []
        ],
        "enzymes": [
            {"name": k, "count": v} for k, v in stats.get("enzymes") or []
        ],
        "run_bins": stats.get("run_bins") or [],
        "coverage": stats.get("coverage") or {},
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
    cov = stats.get("coverage") or {}
    if cov.get("proteomexchange_public"):
        print(
            "  PX coverage: "
            f"{int(cov['proteomexchange_annotated']):,} / "
            f"{int(cov['proteomexchange_public']):,}"
        )
    if cov.get("pride_public"):
        print(
            "  PRIDE coverage: "
            f"{int(cov['pride_annotated']):,} / "
            f"{int(cov['pride_public']):,}"
        )
    print(f"  wrote: {STATS_DIR.relative_to(REPO_ROOT)} and README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
