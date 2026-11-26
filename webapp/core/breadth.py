"""Run skills/market-breadth-analyzer and read its JSON report."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .paths import SKILLS_DIR

_SCRIPT = SKILLS_DIR / "market-breadth-analyzer" / "scripts" / "market_breadth_analyzer.py"

COMPONENTS = [
    ("breadth_level_trend", "Breadth Level & Trend", "25%"),
    ("ma_crossover", "8MA vs 200MA Crossover", "20%"),
    ("cycle_position", "Peak/Trough Cycle Position", "20%"),
    ("bearish_signal", "Bearish Signal Status", "15%"),
    ("historical_percentile", "Historical Percentile", "10%"),
    ("divergence", "S&P 500 vs Breadth Divergence", "10%"),
]


class BreadthError(RuntimeError):
    pass


def run_analyzer(output_dir: Path, extra_args: list[str] | None = None, timeout: int = 180) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(_SCRIPT), "--output-dir", str(output_dir), *(extra_args or [])]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        msg = (proc.stderr or proc.stdout).strip().splitlines()
        raise BreadthError(msg[-1] if msg else f"analyzer exited {proc.returncode}")
    return load_latest_report(output_dir)


def load_latest_report(output_dir: Path) -> dict:
    files = sorted(
        p for p in Path(output_dir).glob("market_breadth_*.json") if "history" not in p.name
    )
    if not files:
        raise BreadthError(f"No market_breadth report found in {output_dir}")
    with open(files[-1], encoding="utf-8") as fh:
        return json.load(fh)


def component_rows(analysis: dict) -> list[dict]:
    comps = analysis.get("components", {})
    rows = []
    for key, label, weight in COMPONENTS:
        if key in comps:
            c = comps[key]
            rows.append(
                {
                    "component": label,
                    "weight": weight,
                    "score": c.get("score"),
                    "signal": c.get("signal", ""),
                }
            )
    return rows
