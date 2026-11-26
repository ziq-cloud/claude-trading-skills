"""Learning path: levels, quiz, chart-replay evaluation and progress storage."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pandas as pd

from .paths import REPO_ROOT

STATE_DIR = REPO_ROOT / "state" / "webapp"
PROGRESS_FILE = STATE_DIR / "progress.json"

QUIZ_PASS_RATIO = 0.8
REPLAYS_FOR_LEVEL_3 = 10
DEMO_TRADES_FOR_LEVEL_4 = 10

# Text for levels, lessons and quiz lives in core/i18n.py
# (keys: level.<n>.name/goal/unlock, lesson.<id>.title/body, quiz.<i>.q/opts).
LEVELS = {
    1: {"max_risk_pct": 0.5, "lessons": ["candles", "trend", "sr", "stoploss", "onepct"]},
    2: {"max_risk_pct": 1.0, "lessons": ["rmultiple", "rr", "sizing"]},
    3: {"max_risk_pct": 1.0, "lessons": ["breadth", "rsi_atr", "expectancy"]},
    4: {"max_risk_pct": 2.0, "lessons": ["setups", "process"]},
}

# Correct option index for each question (quiz.1 … quiz.5 in i18n).
QUIZ = [{"answer": 0}, {"answer": 1}, {"answer": 2}, {"answer": 3}, {"answer": 0}]


@dataclass
class Progress:
    quiz_score: int = 0
    replays: list = field(default_factory=list)


def grade_quiz(answers: list[int]) -> int:
    return sum(1 for q, a in zip(QUIZ, answers) if a == q["answer"])


def quiz_passed(score: int) -> bool:
    return score >= QUIZ_PASS_RATIO * len(QUIZ)


def trade_stats(trades: list[dict]) -> dict:
    rs = [float(t["r_multiple"]) for t in trades if t.get("r_multiple") is not None]
    if not rs:
        return {"trades": 0, "win_rate": 0.0, "expectancy_r": 0.0, "total_r": 0.0}
    wins = [r for r in rs if r > 0]
    return {
        "trades": len(rs),
        "win_rate": len(wins) / len(rs),
        "expectancy_r": sum(rs) / len(rs),
        "total_r": sum(rs),
    }


def current_level(progress: Progress, demo_closed: list[dict]) -> int:
    if not quiz_passed(progress.quiz_score):
        return 1
    if len(progress.replays) < REPLAYS_FOR_LEVEL_3:
        return 2
    demo = trade_stats(demo_closed)
    if demo["trades"] < DEMO_TRADES_FOR_LEVEL_4 or demo["expectancy_r"] <= 0:
        return 3
    return 4


def evaluate_trade(entry: float, stop: float, target: float, future: pd.DataFrame) -> dict:
    """Simulate a long trade over future daily bars.

    Conservative fills: a gap through the stop fills at the open; if one bar touches
    both stop and target, the stop is assumed to hit first. If neither level is hit,
    the trade exits at the last bar's close.
    """
    if stop >= entry:
        raise ValueError("Stop must be below entry for a long trade")
    if target <= entry:
        raise ValueError("Target must be above entry")
    risk = entry - stop
    outcome, exit_price, held = "time", float(future["close"].iloc[-1]), len(future)
    for i, bar in enumerate(future.itertuples(), start=1):
        if bar.low <= stop:
            outcome, exit_price, held = "stop", float(min(bar.open, stop)), i
            break
        if bar.high >= target:
            outcome, exit_price, held = "target", float(max(bar.open, target)), i
            break
    return {
        "outcome": outcome,
        "exit_price": exit_price,
        "bars_held": held,
        "r_multiple": (exit_price - entry) / risk,
    }


def load_progress(path: Path = PROGRESS_FILE) -> Progress:
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return Progress()
    return Progress(quiz_score=int(data.get("quiz_score", 0)), replays=data.get("replays", []))


def save_progress(progress: Progress, path: Path = PROGRESS_FILE) -> None:
    write_json_atomic(asdict(progress), path)


def write_json_atomic(data, path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, default=str)
    os.replace(tmp, path)
