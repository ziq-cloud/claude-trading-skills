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


def _acct(balance=1_000, kind="standard"):
    return demo_account.new_account(balance, kind)


def test_new_account_ranges_and_types():
    a = demo_account.new_account(100, "standard")
    assert a["balance"] == 100 and a["leverage"] == 100
    with pytest.raises(ValueError):
        demo_account.new_account(99, "standard")
    with pytest.raises(ValueError):
        demo_account.new_account(1_001, "standard")
    cent = demo_account.new_account(1_000_000, "cent")
    assert cent["account_type"] == "cent"
    assert cent["balance"] == pytest.approx(10_000)  # stored in USD
    with pytest.raises(ValueError):
        demo_account.new_account(9_999, "cent")
    with pytest.raises(ValueError):
        demo_account.new_account(500, "gold")


def test_money_formatting():
    std = _acct()
    cent = demo_account.new_account(10_000, "cent")
    assert demo_account.fmt_money(std, 1234.5) == "$1,234.50"
    assert demo_account.fmt_money(std, -5) == "-$5.00"
    assert demo_account.fmt_money(cent, 12.345) == "1,234 USC"
    assert demo_account.fmt_money(cent, -0.5) == "-50 USC"
    assert demo_account.fmt_money(cent, 0.004) == "0 USC"
    assert demo_account.fmt_money(std, -0.001) == "$0.00"


def test_buy_eurusd_reserves_margin_and_enforces_rules():
    acct = _acct()
    t = demo_account.open_trade(
        acct,
        "EURUSD",
        "buy",
        0.05,
        entry=1.1000,
        stop=1.0980,
        target=1.1040,
        date="2026-11-25",
        max_risk_pct=1,
    )
    assert t["risk_usd"] == pytest.approx(10)
    assert t["margin_usd"] == pytest.approx(55)
    assert acct["balance"] == 1_000  # balance only changes on close
    assert demo_account.free_margin(acct, {"EURUSD": 1.1}) == pytest.approx(945)

    with pytest.raises(demo_account.RuleViolation) as exc:
        demo_account.open_trade(acct, "EURUSD", "buy", 0.03, 1.1, 1.09, 1.12, "d", 1)
    assert exc.value.code == "lot"  # fixed lot sizes only
    with pytest.raises(demo_account.RuleViolation) as exc:
        demo_account.open_trade(acct, "EURUSD", "buy", 0.10, 1.1, 1.098, 1.12, "d", 1)
    assert exc.value.code == "risk"
    with pytest.raises(demo_account.RuleViolation) as exc:
        demo_account.open_trade(acct, "EURUSD", "buy", 0.01, 1.1, 1.1, 1.12, "d", 1)
    assert exc.value.code == "stop"
    with pytest.raises(demo_account.RuleViolation) as exc:
        demo_account.open_trade(acct, "EURUSD", "sell", 0.01, 1.1, 1.09, 1.08, "d", 1)
    assert exc.value.code == "stop"  # a sell needs its stop above entry


def test_margin_check():
    acct = _acct(100)
    with pytest.raises(demo_account.RuleViolation) as exc:
        demo_account.open_trade(acct, "XAUUSD", "buy", 0.05, 3500, 3499.9, 3510, "d", 2)
    assert exc.value.code == "margin"  # needs $175 margin


def test_sell_profit_and_r_multiple():
    acct = _acct()
    t = demo_account.open_trade(
        acct, "EURUSD", "sell", 0.05, 1.1000, 1.1020, 1.0960, "2026-11-25", 1
    )
    assert demo_account.floating_pnl(acct, {"EURUSD": 1.0980}) == pytest.approx(10)
    closed = demo_account.close_trade(acct, t["id"], 1.0960, "2026-11-30", "target")
    assert closed["pnl"] == pytest.approx(20)
    assert closed["r_multiple"] == pytest.approx(2.0)
    assert acct["balance"] == pytest.approx(1_020)


def test_usdjpy_pnl_in_usd():
    acct = _acct()
    t = demo_account.open_trade(acct, "USDJPY", "buy", 0.02, 150.00, 149.50, 151.0, "d", 1)
    closed = demo_account.close_trade(acct, t["id"], 151.00, "d2", "target")
    assert closed["pnl"] == pytest.approx(1.0 * 2_000 / 151.0, abs=1e-3)


def test_cent_account_trades_one_hundredth():
    acct = demo_account.new_account(10_000, "cent")  # $100
    t = demo_account.open_trade(acct, "EURUSD", "buy", 0.05, 1.1, 1.09, 1.12, "d", 0.5)
    assert t["risk_usd"] == pytest.approx(0.5)  # shown as 50 USC
    closed = demo_account.close_trade(acct, t["id"], 1.12, "d2", "target")
    assert demo_account.fmt_money(acct, closed["pnl"]) == "100 USC"


def test_auto_exit_from_bars_after_entry_buy_and_sell():
    acct = _acct()
    b = demo_account.open_trade(acct, "EURUSD", "buy", 0.05, 1.1, 1.098, 1.104, "2026-01-05", 1)
    s = demo_account.open_trade(acct, "GBPUSD", "sell", 0.01, 1.3, 1.31, 1.28, "2026-01-05", 1)
    eur = _bars([(1.1, 1.101, 1.099, 1.1), (1.1, 1.1, 1.097, 1.0975)])
    gbp = _bars([(1.3, 1.301, 1.299, 1.3), (1.29, 1.29, 1.279, 1.28)])
    exits = {e["id"]: e for e in demo_account.check_exits(acct, {"EURUSD": eur, "GBPUSD": gbp})}
    assert exits[b["id"]]["exit_reason"] == "stop" and exits[b["id"]]["exit_price"] == 1.098
    assert exits[s["id"]]["exit_reason"] == "target"
    assert acct["open"] == []


def test_stop_out_closes_worst_position_below_50pct_margin_level():
    acct = _acct(100)
    demo_account.open_trade(acct, "XAUUSD", "buy", 0.01, 3500, 3450, 3600, "d", 100)
    # margin $35; at 3434 floating -$66 -> equity $34 -> level 97%: fine
    assert demo_account.stop_out(acct, {"XAUUSD": 3434}, "d2") == []
    # at 3420 floating -$80 -> equity $20 -> level 57%: fine; at 3410 -> 29%: stop out
    out = demo_account.stop_out(acct, {"XAUUSD": 3410}, "d2")
    assert len(out) == 1 and out[0]["exit_reason"] == "stop_out"
    assert acct["balance"] == pytest.approx(10)


def test_account_roundtrip(tmp_path):
    f = tmp_path / "acct.json"
    acct = demo_account.new_account(50_000, "cent")
    demo_account.save(acct, f)
    assert demo_account.load(f) == acct
    assert demo_account.load(tmp_path / "none.json") is None


# ---------------------------------------------------------------- short trades (forex)


def test_replay_short_hits_target():
    future = _bars([(100, 101, 95, 96), (96, 97, 89, 90)])
    r = training.evaluate_trade(entry=100, stop=105, target=90, future=future, side="sell")
    assert r["outcome"] == "target"
    assert r["r_multiple"] == pytest.approx(2.0)


def test_replay_short_gap_above_stop():
    future = _bars([(108, 109, 107, 108)])
    r = training.evaluate_trade(entry=100, stop=105, target=90, future=future, side="sell")
    assert r["outcome"] == "stop"
    assert r["exit_price"] == 108
    assert r["r_multiple"] == pytest.approx(-1.6)


def test_replay_short_rejects_stop_below_entry():
    with pytest.raises(ValueError):
        training.evaluate_trade(100, 95, 90, _bars([(1, 1, 1, 1)]), side="sell")
