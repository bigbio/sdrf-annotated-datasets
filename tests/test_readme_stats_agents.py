"""Agent attribution rules in .github/scripts/generate_readme_stats.py (Gemini/Antigravity)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

pytest.importorskip("matplotlib")  # the stats script imports it at module level

_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "generate_readme_stats.py"
_spec = importlib.util.spec_from_file_location("generate_readme_stats", _PATH)
g = importlib.util.module_from_spec(_spec)
sys.modules["generate_readme_stats"] = g  # dataclasses resolve annotations via sys.modules
_spec.loader.exec_module(g)
L = g.GEMINI_LABEL


@pytest.mark.parametrize(
    "text",
    [
        "Generated with Google Antigravity",
        "Generated with [Gemini CLI](https://github.com/google-gemini/gemini-cli)",
        "Co-authored-by: Gemini <noreply@google.com>",
    ],
)
def test_text_declares_gemini(text):
    assert g._parse_agent_text(text) == {L}


@pytest.mark.parametrize("ref", ["gemini/x", "antigravity/x", "Yixuan39:gemini/x"])
def test_branch_prefix(ref):
    assert g._agent_from_branch(ref) == L


def test_identity():
    assert g.classify_contributor("Gemini CLI", "a@b.c") == L
    assert g.classify_contributor("Antigravity", "a@b.c") == L


def test_review_bot_and_gemma_are_not_annotators():
    assert g.classify_contributor("gemini-code-assist[bot]", "a@b.c") is None
    assert g._parse_agent_text("Generated with Gemini Code Assist") == set()
    assert g._parse_agent_text("gemma2:9b draft, independently reviewed") == set()
