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

LEVELS = {
    1: {
        "name": "Beginner",
        "goal": "Learn to read a chart and understand why every trade needs a stop-loss.",
        "unlock": "Pass the basics quiz (80% or better).",
        "max_risk_pct": 0.5,
        "lessons": [
            (
                "Candlesticks",
                "Each candle is one period (here: one day). The **body** spans open to close; "
                "green means close > open, red means close < open. The **wicks** show the high "
                "and low. Long lower wicks mean buyers pushed price back up; long upper wicks "
                "mean sellers pushed it down.",
            ),
            (
                "Trend",
                "An **uptrend** makes higher highs and higher lows. A quick test: price above a "
                "rising 50-day and 200-day moving average. Beginners do best trading *with* the "
                "trend, not trying to catch tops and bottoms.",
            ),
            (
                "Support and resistance",
                "**Support** is a price area where buying has stopped declines before; "
                "**resistance** is where selling has stopped rallies. These areas are natural "
                "places for entries and stops.",
            ),
            (
                "Why a stop-loss is mandatory",
                "A stop-loss is the price where your idea is proven wrong and you exit. Without "
                "one, a single bad trade can wipe out months of gains. In this app you **cannot** "
                "open a demo trade without a stop.",
            ),
            (
                "The 1% rule",
                "Risk a small, fixed slice of your account per trade, e.g. 0.5–1%. With $10,000 "
                "and 1% risk you may lose at most $100 if the stop is hit. Ten losses in a row "
                "then cost about 10%, which you can recover from.",
            ),
        ],
    },
    2: {
        "name": "Risk Control",
        "goal": "Practise entries with a stop and a target on historical charts.",
        "unlock": f"Complete {REPLAYS_FOR_LEVEL_3} Chart Replay trades.",
        "max_risk_pct": 1.0,
        "lessons": [
            (
                "R-multiples",
                "**1R** is the amount you risk (entry − stop). A trade that gains twice the risk "
                "is **+2R**; a stopped-out trade is **−1R**. Measuring in R lets you compare "
                "trades of any size.",
            ),
            (
                "Reward-to-risk",
                "Aim for targets of at least 2R. With 2R winners you can be right only 40% of the "
                "time and still make money: 0.4 × 2 − 0.6 × 1 = +0.2R per trade.",
            ),
            (
                "Position sizing",
                "Shares = (account × risk %) ÷ (entry − stop). Use the **Position Sizer** page "
                "or the ATR method: stop = entry − 2 × ATR.",
            ),
        ],
    },
    3: {
        "name": "Trend & Context",
        "goal": "Trade the demo account on live prices and read the market backdrop first.",
        "unlock": f"Close {DEMO_TRADES_FOR_LEVEL_4} demo trades with positive expectancy.",
        "max_risk_pct": 1.0,
        "lessons": [
            (
                "Market breadth",
                "Most stocks follow the overall market. Check **Market Breadth** before trading: "
                "a weak score means smaller size or fewer trades.",
            ),
            (
                "RSI and ATR",
                "**RSI** above 70 is stretched, below 30 is washed out; in uptrends, pullbacks to "
                "40–50 are often better entries than chasing above 70. **ATR** measures normal "
                "daily movement; a stop tighter than ~1 ATR is often hit by noise.",
            ),
            (
                "Expectancy",
                "Expectancy = average R per trade. It matters more than win rate. Keep a journal "
                "(the demo account does this for you) and review your losers.",
            ),
        ],
    },
    4: {
        "name": "Advanced",
        "goal": "Use the repository's screeners and setups to build a repeatable process.",
        "unlock": "Top level.",
        "max_risk_pct": 2.0,
        "lessons": [
            (
                "Setups",
                "Explore the **Skill Catalog**: VCP Screener, Breakout Trade Planner, PEAD "
                "Screener, CANSLIM and others encode specific, testable entry rules.",
            ),
            (
                "Process over outcome",
                "Write a rule set, test it (Chart Replay, Backtest Expert), then trade it small. "
                "Change one thing at a time and judge it over 20+ trades, not one.",
            ),
        ],
    },
}

QUIZ = [
    {
        "q": "A green candle means…",
        "options": ["Close above open", "Close below open", "High volume", "Price gapped up"],
        "answer": 0,
    },
    {
        "q": "An uptrend is best described as…",
        "options": [
            "Lower highs and lower lows",
            "Higher highs and higher lows",
            "Price stuck in a range",
            "RSI above 70",
        ],
        "answer": 1,
    },
    {
        "q": "Account $10,000, risk 1%, entry $50, stop $48. How many shares?",
        "options": ["20", "200", "50", "100"],
        "answer": 2,
    },
    {
        "q": "When should you decide on your stop-loss?",
        "options": [
            "After the trade goes against you",
            "Never; just hold",
            "When the news changes",
            "Before you enter the trade",
        ],
        "answer": 3,
    },
    {
        "q": "Entry $100, stop $95, exit $110. The result is…",
        "options": ["+2R", "+1R", "+10R", "−1R"],
        "answer": 0,
    },
]


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
