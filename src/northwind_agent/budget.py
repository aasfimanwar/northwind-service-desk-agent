"""Per-run request and token budgets derived from the recorded free-tier limits.

The numbers come from config/provider_limits.json (read from the provider consoles) and the
rules in ADR-0008 as amended by ADR-0016: routine runs may use a fraction of each model's
daily limit, milestone runs a larger fraction, checked per dimension.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelLimits:
    provider: str
    model: str
    rpm: int
    rpd: int
    tpm: int
    tpd: int | None  # None when the provider shows no daily token limit


@dataclass(frozen=True)
class RunBudget:
    max_requests: int
    max_tokens: int | None  # None means no daily token limit to budget against


@dataclass(frozen=True)
class LimitsConfig:
    models: dict[tuple[str, str], ModelLimits]
    routine_fraction: float
    milestone_fraction: float


def load_config(path: Path) -> LimitsConfig:
    raw = json.loads(path.read_text(encoding="utf-8"))
    models: dict[tuple[str, str], ModelLimits] = {}
    for name, v in raw["providers"]["groq"]["chat_models"].items():
        models[("groq", name)] = ModelLimits("groq", name, v["rpm"], v["rpd"], v["tpm"], v["tpd"])
    gemini = raw["providers"]["gemini"]
    for section in ("text_out_models_available", "other_models"):
        for name, v in gemini[section].items():
            models[("gemini", name)] = ModelLimits(
                "gemini", name, v["rpm"], v["rpd"], v["tpm"], None
            )
    rule = raw["budget_rule"]
    return LimitsConfig(
        models=models,
        routine_fraction=float(rule["routine_fraction_of_daily_limit_per_run"]),
        milestone_fraction=float(rule["milestone_fraction_of_daily_limit_per_run"]),
    )


def _share(limit: int, fraction: float) -> int:
    # small epsilon so values like 1000 * 0.6 never round down by floating-point error
    return math.floor(limit * fraction + 1e-9)


def run_budget(config: LimitsConfig, provider: str, model: str, *, milestone: bool) -> RunBudget:
    try:
        limits = config.models[(provider, model)]
    except KeyError:
        raise KeyError(f"no recorded limits for {provider} / {model}") from None
    fraction = config.milestone_fraction if milestone else config.routine_fraction
    tokens = None if limits.tpd is None else _share(limits.tpd, fraction)
    return RunBudget(max_requests=_share(limits.rpd, fraction), max_tokens=tokens)
