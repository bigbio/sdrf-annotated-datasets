"""Make .github/scripts importable so the review gate can be tested directly.

The gate lives in .github/scripts/ rather than an installable package, so there is no import
path to it by default. Loading it by file keeps the script exactly where CI expects it.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = REPO_ROOT / ".github" / "scripts" / "sdrf_review.py"


def _load_gate():
    spec = importlib.util.spec_from_file_location("sdrf_review", GATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def gate():
    return _load_gate()


def load_script(name):
    path = REPO_ROOT / ".github" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def report_mod():
    return load_script("sdrf_change_report")


@pytest.fixture(scope="session")
def render_mod():
    return load_script("sdrf_change_render")


@pytest.fixture(scope="session")
def llm_mod():
    return load_script("sdrf_change_llm")


@pytest.fixture(scope="session")
def post_mod():
    return load_script("sdrf_change_post")


@pytest.fixture
def write_sdrf(tmp_path):
    """Write a TSV from a header list and row lists; returns the path."""
    def _write(header, rows, name="PXD000001.sdrf.tsv", root=None):
        base = Path(root) if root else tmp_path
        target = base / "datasets" / name.split(".")[0] / name
        target.parent.mkdir(parents=True, exist_ok=True)
        body = "\n".join(["\t".join(header)] + ["\t".join(r) for r in rows])
        target.write_text(body + "\n", encoding="utf-8")
        return target
    return _write
