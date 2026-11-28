from pathlib import Path

import pytest

from northwind_agent.budget import load_config, run_budget

CONFIG = Path(__file__).resolve().parent.parent / "config" / "provider_limits.json"


def test_gemini_flash_lite_routine_budget() -> None:
    cfg = load_config(CONFIG)
    budget = run_budget(cfg, "gemini", "Gemini 3.5 Flash Lite", milestone=False)
    assert budget.max_requests == 125
    assert budget.max_tokens is None


def test_gemini_flash_lite_milestone_budget() -> None:
    cfg = load_config(CONFIG)
    budget = run_budget(cfg, "gemini", "Gemini 3.5 Flash Lite", milestone=True)
    assert budget.max_requests == 300


def test_groq_qwen_budgets() -> None:
    cfg = load_config(CONFIG)
    routine = run_budget(cfg, "groq", "qwen/qwen3.8-27b", milestone=False)
    milestone = run_budget(cfg, "groq", "qwen/qwen3.8-27b", milestone=True)
    assert (routine.max_requests, routine.max_tokens) == (250, 50_000)
    assert (milestone.max_requests, milestone.max_tokens) == (600, 120_000)


def test_unknown_model_is_an_error() -> None:
    cfg = load_config(CONFIG)
    with pytest.raises(KeyError, match="no recorded limits"):
        run_budget(cfg, "groq", "no-such-model", milestone=False)
