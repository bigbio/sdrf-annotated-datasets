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


@pytest.mark.parametrize(
    "text",
    [
        "Add 198 SDRF annotations from sdrf-agentic-annotator (DeepSeek-V4-Flash-0731, agent workflow)",
        "Add SDRF annotations from DeepSeek-v4-pro LLM",
        "Co-authored-by: deepseek <noreply@deepseek.com>",
    ],
)
def test_text_declares_deepseek(text):
    assert "DeepSeek" in g._parse_agent_text(text)


def test_deepseek_branch_prefix():
    assert g._agent_from_branch("deepseek/pxd000001") == "DeepSeek"
    assert g._agent_from_branch("ypriverol:deepseek/batch") == "DeepSeek"


@pytest.mark.parametrize(
    "text,expected",
    [
        ("DeepSeek-V4-Flash-0731", {"DeepSeek V4 Flash"}),
        ("deepseek-v4-flash", {"DeepSeek V4 Flash"}),
        ("DeepSeek-v4-pro LLM", {"DeepSeek V4 Pro"}),
        ("Model used for annotation: **deepseek pro4.1**", {"DeepSeek Pro 4.1"}),
        ("Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>", {"Claude Opus 5.5"}),
        ("Co-Authored-By: claude-opus-5-5[1m] <noreply@anthropic.com>", {"Claude Opus 5.5"}),
        ("Co-Authored-By: claude-opus-5[1m] <noreply@anthropic.com>", {"Claude Opus 5"}),
        ("Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>", {"Claude Opus 4.8"}),
        ("Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>", {"Claude Sonnet 5"}),
        ("Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>", {"Claude Sonnet 5.5"}),
        ("claude-haiku-5-5", {"Claude Haiku 5.5"}),
        ("gemma2:9b review", {"Gemma 2 (9B)"}),
        ("Ollama qwen2.5:3b summarizer", {"Qwen 2.5 (3B)"}),
        ("gemini-2.0-flash", {"Gemini 2"}),
        ("grok 4.7 benchmark", {"Grok 4.7"}),
        ("grok-4.7", {"Grok 4.7"}),
        ("Import from crosslinking-datasets bulk annotation project", {"Community import (XL-MS)"}),
        ("produced with the sdrf-skills workflow on top of sdrf-pipelines", {"Claude (sdrf-skills)"}),
    ],
)
def test_parse_model_text(text, expected):
    assert g.parse_model_text(text) == expected


def test_read_sdrf_annotation_tool(tmp_path):
    sdrf = tmp_path / "test.sdrf.tsv"
    sdrf.write_text("source name\tcomment[sdrf annotation tool]\nSample 1\tNT=sdrf-skeleton-gen;VV=v2.0.0\n")
    assert g._read_sdrf_annotation_tool(sdrf) == "NT=sdrf-skeleton-gen;VV=v2.0.0"


def test_render_models_figure(tmp_path):
    contrib = {
        "ai_models": 4,
        "models": [
            {"name": "Grok 4.7 (Cursor)", "accessions": 7000, "files": 7000},
            {"name": "DeepSeek V4 Flash", "accessions": 198, "files": 198},
            {"name": "Claude Opus 5.5", "accessions": 150, "files": 170},
            {"name": "Cursor (unspecified model)", "accessions": 500, "files": 500},
        ],
        "origin": [{"name": "Agent-assisted", "accessions": 7848}],
    }
    out_png = tmp_path / "models.png"
    g.render_models_figure(out_png, contrib, {"accessions": 7848})
    assert out_png.exists()
    assert out_png.stat().st_size > 1000

