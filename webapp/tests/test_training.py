"""Tests for the learning path, chart replay evaluation and demo account."""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import demo_account, training  # noqa: E402


def _bars(rows):
    return pd.DataFrame(
        rows,
        columns=["open", "high", "low", "close"],
        index=pd.date_range("2026-01-05", periods=len(rows), freq="B"),
    )


# ---------------------------------------------------------------- replay


def test_replay_hits_target():
    future = _bars([(100, 103, 99, 102), (102, 111, 101, 110)])
    r = training.evaluate_trade(entry=100, stop=95, target=110, future=future)
    assert r["outcome"] == "target"
    assert r["exit_price"] == 110
    assert r["r_multiple"] == pytest.approx(2.0)
    assert r["bars_held"] == 2


def test_replay_hits_stop():
    future = _bars([(100, 101, 94, 96)])
    r = training.evaluate_trade(entry=100, stop=95, target=110, future=future)
    assert r["outcome"] == "stop"
    assert r["r_multiple"] == pytest.approx(-1.0)


def test_replay_gap_below_stop_fills_at_open():
    future = _bars([(90, 92, 88, 91)])
    r = training.evaluate_trade(entry=100, stop=95, target=110, future=future)
    assert r["exit_price"] == 90
    assert r["r_multiple"] == pytest.approx(-2.0)


def test_replay_same_bar_assumes_stop_first():
    future = _bars([(100, 112, 94, 105)])
    r = training.evaluate_trade(entry=100, stop=95, target=110, future=future)
    assert r["outcome"] == "stop"


def test_replay_time_exit():
    future = _bars([(100, 102, 98, 101), (101, 104, 99, 103)])
    r = training.evaluate_trade(entry=100, stop=95, target=110, future=future)
    assert r["outcome"] == "time"
    assert r["exit_price"] == 103


def test_replay_rejects_bad_levels():
    with pytest.raises(ValueError):
        training.evaluate_trade(entry=100, stop=101, target=110, future=_bars([(1, 1, 1, 1)]))
    with pytest.raises(ValueError):
        training.evaluate_trade(entry=100, stop=95, target=99, future=_bars([(1, 1, 1, 1)]))


# ---------------------------------------------------------------- levels


def test_quiz_grading():
    answers = [q["answer"] for q in training.QUIZ]
    assert training.grade_quiz(answers) == len(training.QUIZ)
    wrong = [(a + 1) % 4 for a in answers]
    assert training.grade_quiz(wrong) == 0


def test_level_progression():
    p = training.Progress()
    assert training.current_level(p, demo_closed=[]) == 1
    p.quiz_score = len(training.QUIZ)
    assert training.current_level(p, demo_closed=[]) == 2
    p.replays = [{"r_multiple": 1.0}] * 10
    assert training.current_level(p, demo_closed=[]) == 3
    closed = [{"r_multiple": 0.5}] * 10
    assert training.current_level(p, demo_closed=closed) == 4


def test_level_four_needs_positive_expectancy():
    p = training.Progress(quiz_score=len(training.QUIZ), replays=[{"r_multiple": -1}] * 10)
    closed = [{"r_multiple": -0.5}] * 10
    assert training.current_level(p, demo_closed=closed) == 3


def test_progress_roundtrip(tmp_path):
    f = tmp_path / "progress.json"
    p = training.Progress(quiz_score=3, replays=[{"r_multiple": 2.0}])
    training.save_progress(p, f)
    assert training.load_progress(f) == p
    assert training.load_progress(tmp_path / "missing.json") == training.Progress()


def test_stats():
    s = training.trade_stats([{"r_multiple": 2.0}, {"r_multiple": -1.0}, {"r_multiple": 1.0}])
    assert s["trades"] == 3
    assert s["win_rate"] == pytest.approx(2 / 3)
    assert s["expectancy_r"] == pytest.approx(2 / 3)
    assert training.trade_stats([])["trades"] == 0


# ---------------------------------------------------------------- demo account


def test_open_trade_deducts_cash_and_enforces_rules():
    acct = demo_account.new_account(10_000)
    t = demo_account.open_trade(
        acct, "AAPL", entry=100, stop=95, target=115, shares=10, date="2026-11-25", max_risk_pct=1
    )
    assert acct["cash"] == pytest.approx(9_000)
    assert t["risk_dollars"] == pytest.approx(50)
    with pytest.raises(demo_account.RuleViolation, match="risk"):
        demo_account.open_trade(acct, "MSFT", 100, 90, 130, 20, "2026-11-25", max_risk_pct=1)
    with pytest.raises(demo_account.RuleViolation, match="cash"):
        demo_account.open_trade(acct, "MSFT", 100, 99.9, 101, 95, "2026-11-25", max_risk_pct=1)
    with pytest.raises(demo_account.RuleViolation, match="stop"):
        demo_account.open_trade(acct, "MSFT", 100, 100, 110, 1, "2026-11-25", max_risk_pct=1)


def test_close_trade_records_pnl_and_r():
    acct = demo_account.new_account(10_000)
    t = demo_account.open_trade(acct, "AAPL", 100, 95, 115, 10, "2026-11-25", max_risk_pct=1)
    closed = demo_account.close_trade(acct, t["id"], price=110, date="2026-11-30", reason="manual")
    assert closed["pnl"] == pytest.approx(100)
    assert closed["r_multiple"] == pytest.approx(2.0)
    assert acct["cash"] == pytest.approx(10_100)
    assert acct["open"] == [] and len(acct["closed"]) == 1


def test_auto_exit_from_bars_after_entry():
    acct = demo_account.new_account(10_000)
    t = demo_account.open_trade(acct, "AAPL", 100, 95, 110, 10, "2026-01-05", max_risk_pct=1)
    bars = _bars([(100, 101, 99, 100), (100, 102, 94, 96)])  # 01-05 (entry day), 01-06
    exits = demo_account.check_exits(acct, {"AAPL": bars})
    assert len(exits) == 1 and exits[0]["exit_reason"] == "stop"
    assert exits[0]["id"] == t["id"]
    assert acct["cash"] == pytest.approx(9_950)


def test_equity_marks_open_positions():
    acct = demo_account.new_account(10_000)
    demo_account.open_trade(acct, "AAPL", 100, 95, 115, 10, "2026-11-25", max_risk_pct=1)
    assert demo_account.equity(acct, {"AAPL": 105}) == pytest.approx(10_050)


def test_account_roundtrip(tmp_path):
    f = tmp_path / "acct.json"
    acct = demo_account.new_account(5_000)
    demo_account.save(acct, f)
    assert demo_account.load(f) == acct
    assert demo_account.load(tmp_path / "none.json") is None
