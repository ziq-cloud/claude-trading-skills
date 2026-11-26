"""Skill catalog loaded from the repository's skills-index.yaml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .paths import SKILLS_INDEX

# Integrations that need a paid key / brokerage account.
PAID_INTEGRATIONS = {"fmp", "finviz", "finviz_elite", "alpaca"}

CATEGORY_LABELS = {
    "market-regime": "Market Regime",
    "core-portfolio": "Core Portfolio",
    "dividend-income": "Dividend Income",
    "swing-opportunity": "Swing Opportunity",
    "trade-planning": "Trade Planning",
    "trade-memory": "Trade Memory",
    "strategy-research": "Strategy Research",
    "advanced-satellite": "Advanced Satellite",
    "meta": "Meta",
}

API_LEVEL_LABELS = {
    "none": "No paid API",
    "optional": "Paid API optional",
    "required": "Paid API required",
}


@dataclass(frozen=True)
class Skill:
    id: str
    display_name: str
    category: str
    status: str
    summary: str
    timeframe: str
    difficulty: str
    api_level: str
    integrations: list = field(default_factory=list)
    workflows: list = field(default_factory=list)

    @property
    def category_label(self) -> str:
        return CATEGORY_LABELS.get(self.category, self.category)


def classify_api_level(integrations: list[dict]) -> str:
    """Return 'required', 'optional' or 'none' for paid-API dependence."""
    levels = {
        (i.get("requirement") or "").lower()
        for i in integrations or []
        if (i.get("id") or "").lower() in PAID_INTEGRATIONS
    }
    if "required" in levels:
        return "required"
    if levels:
        return "optional"
    return "none"


def load_skills(index_path: Path = SKILLS_INDEX) -> list[Skill]:
    with open(index_path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    skills = []
    for raw in data.get("skills", []):
        integrations = raw.get("integrations") or []
        skills.append(
            Skill(
                id=raw["id"],
                display_name=raw.get("display_name", raw["id"]),
                category=raw.get("category", ""),
                status=raw.get("status", ""),
                summary=(raw.get("summary") or "").strip(),
                timeframe=raw.get("timeframe", ""),
                difficulty=raw.get("difficulty", ""),
                api_level=classify_api_level(integrations),
                integrations=integrations,
                workflows=raw.get("workflows") or [],
            )
        )
    return sorted(skills, key=lambda s: s.display_name.lower())


def filter_skills(
    skills: list[Skill],
    query: str = "",
    categories: set[str] | None = None,
    api_levels: set[str] | None = None,
) -> list[Skill]:
    q = query.strip().lower()
    out = []
    for s in skills:
        if categories and s.category not in categories:
            continue
        if api_levels and s.api_level not in api_levels:
            continue
        if q and q not in (s.display_name + " " + s.summary + " " + s.id).lower():
            continue
        out.append(s)
    return out
