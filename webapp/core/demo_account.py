"""Demo (paper) trading account for forex, gold, BTC and WTI.

* Buy or sell, fixed lot sizes only (instruments.LOT_SIZES), stop-loss mandatory.
* Leveraged: opening a trade reserves margin; balance changes only when a trade closes.
* Two account types like retail brokers:
    standard — USD balance, $100 to $1,000
    cent     — USC balance, 10,000 to 1,000,000 USC ($100 to $10,000); each lot is
               1/100 of the standard contract, so P&L numbers look the same but in cents.
* Stop-out: when margin level (equity / used margin) falls below 50%, the worst losing
  trade is closed until the level recovers.
All amounts are stored in USD.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import pandas as pd

from . import instruments as ins
from .training import STATE_DIR, write_json_atomic

ACCOUNT_FILE = STATE_DIR / "demo_account.json"
STOP_OUT_LEVEL = 50.0

ACCOUNT_TYPES = {
    # type: (min, max, units per USD, choices in account units, contract scale)
    "standard": (100, 1_000, 1, [100, 200, 300, 500, 750, 1_000], 1.0),
    "cent": (
        10_000,
        1_000_000,
        100,
        [10_000, 25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000],
        0.01,
    ),
}
DEFAULT_LEVERAGE = 100


class RuleViolation(ValueError):
    """A trade breaks one of the account's rules. `code` maps to a UI message."""

    def __init__(self, code: str, message: str, **params):
        super().__init__(message)
        self.code = code
        self.params = params


def new_account(starting_balance: float, account_type: str = "standard") -> dict:
    if account_type not in ACCOUNT_TYPES:
        raise ValueError(f"Unknown account type: {account_type}")
    lo, hi, per_usd, _, _ = ACCOUNT_TYPES[account_type]
    if not lo <= starting_balance <= hi:
        raise ValueError(f"{account_type} balance must be between {lo:,} and {hi:,}")
    usd = float(starting_balance) / per_usd
    return {
        "account_type": account_type,
        "leverage": DEFAULT_LEVERAGE,
        "starting_balance": usd,
        "balance": usd,
        "open": [],
        "closed": [],
    }


def scale(acct: dict) -> float:
    return ACCOUNT_TYPES[acct["account_type"]][4]


def fmt_money(acct: dict, usd: float) -> str:
    per_usd = ACCOUNT_TYPES[acct.get("account_type", "standard")][2]
    value = usd * per_usd
    if per_usd == 1:
        value = round(value, 2)
        return f"{'-' if value < 0 else ''}${abs(value):,.2f}"
    value = round(value)  # cents are the smallest unit
    return f"{'-' if value < 0 else ''}{abs(value):,} USC"


def fmt_lots(lots: float) -> str:
    return f"{lots:.2f}"


def _direction(side: str) -> int:
    return 1 if side == "buy" else -1


def trade_pnl(acct: dict, trade: dict, price: float) -> float:
    inst = ins.get(trade["code"])
    move = (price - trade["entry"]) * _direction(trade["side"])
    return ins.move_value_usd(inst, move, trade["lots"], price, scale(acct))


def floating_pnl(acct: dict, last_prices: dict[str, float]) -> float:
    return sum(trade_pnl(acct, t, last_prices.get(t["code"], t["entry"])) for t in acct["open"])


def equity(acct: dict, last_prices: dict[str, float]) -> float:
    return acct["balance"] + floating_pnl(acct, last_prices)


def used_margin(acct: dict) -> float:
    return sum(t["margin_usd"] for t in acct["open"])


def free_margin(acct: dict, last_prices: dict[str, float]) -> float:
    return equity(acct, last_prices) - used_margin(acct)


def margin_level(acct: dict, last_prices: dict[str, float]) -> float | None:
    used = used_margin(acct)
    return None if used == 0 else equity(acct, last_prices) / used * 100


def open_trade(
    acct: dict,
    code: str,
    side: str,
    lots: float,
    entry: float,
    stop: float,
    target: float | None,
    date: str,
    max_risk_pct: float,
    note: str = "",
    last_prices: dict[str, float] | None = None,
) -> dict:
    inst = ins.get(code)
    if side not in ("buy", "sell"):
        raise RuleViolation("side", "Side must be buy or sell")
    if round(lots, 2) not in ins.LOT_SIZES:
        raise RuleViolation("lot", f"Lot size must be one of {ins.LOT_SIZES}")
    d = _direction(side)
    if stop is None or (entry - stop) * d <= 0:
        raise RuleViolation("stop", "Stop-loss must be on the losing side of the entry")
    if target is not None and (target - entry) * d <= 0:
        raise RuleViolation("target", "Target must be on the winning side of the entry")

    prices = dict(last_prices or {})
    prices.setdefault(code, entry)
    eq = equity(acct, prices)
    sc = scale(acct)
    risk = ins.risk_usd(inst, lots, entry, stop, sc)
    risk_pct = risk / eq * 100
    if risk_pct > max_risk_pct + 1e-9:
        raise RuleViolation(
            "risk",
            f"Trade risk {risk_pct:.2f}% exceeds the limit of {max_risk_pct}%",
            pct=round(risk_pct, 2),
            limit=max_risk_pct,
        )
    margin = ins.margin_usd(inst, lots, entry, sc)
    free = free_margin(acct, prices)
    if margin > free + 1e-9:
        raise RuleViolation(
            "margin",
            f"Not enough free margin: need {margin:,.2f}, have {free:,.2f}",
            need=margin,
            have=free,
        )
    trade = {
        "id": uuid.uuid4().hex[:8],
        "code": code,
        "side": side,
        "lots": round(lots, 2),
        "entry": float(entry),
        "stop": float(stop),
        "target": None if target is None else float(target),
        "entry_date": str(date),
        "risk_usd": round(risk, 4),
        "risk_pct": round(risk_pct, 2),
        "margin_usd": round(margin, 4),
        "note": note,
    }
    acct["open"].append(trade)
    return trade


def close_trade(acct: dict, trade_id: str, price: float, date: str, reason: str) -> dict:
    idx = next((i for i, t in enumerate(acct["open"]) if t["id"] == trade_id), None)
    if idx is None:
        raise KeyError(trade_id)
    t = acct["open"].pop(idx)
    pnl = trade_pnl(acct, t, price)
    closed = {
        **t,
        "exit_price": round(float(price), 6),
        "exit_date": str(date),
        "exit_reason": reason,
        "pnl": round(pnl, 4),
        "r_multiple": round(
            (price - t["entry"]) * _direction(t["side"]) / abs(t["entry"] - t["stop"]), 2
        )
        + 0.0,
    }
    acct["balance"] += pnl
    acct["closed"].append(closed)
    return closed


def check_exits(acct: dict, bars_by_code: dict[str, pd.DataFrame]) -> list[dict]:
    """Close trades whose stop or target was touched on a daily bar after the entry date.

    Conservative fills: gaps through the stop fill at the open, and a bar touching both
    levels counts as a stop.
    """
    exits = []
    for t in list(acct["open"]):
        bars = bars_by_code.get(t["code"])
        if bars is None or bars.empty:
            continue
        buy = t["side"] == "buy"
        after = bars[bars.index > pd.Timestamp(t["entry_date"])]
        for ts, bar in after.iterrows():
            hit_stop = bar["low"] <= t["stop"] if buy else bar["high"] >= t["stop"]
            hit_target = t["target"] is not None and (
                bar["high"] >= t["target"] if buy else bar["low"] <= t["target"]
            )
            if hit_stop:
                price = min(bar["open"], t["stop"]) if buy else max(bar["open"], t["stop"])
                reason = "stop"
            elif hit_target:
                price = max(bar["open"], t["target"]) if buy else min(bar["open"], t["target"])
                reason = "target"
            else:
                continue
            exits.append(close_trade(acct, t["id"], float(price), ts.date().isoformat(), reason))
            break
    return exits


def stop_out(acct: dict, last_prices: dict[str, float], date: str) -> list[dict]:
    """Close the worst losing trades while margin level is below STOP_OUT_LEVEL."""
    closed = []
    while acct["open"]:
        level = margin_level(acct, last_prices)
        if level is None or level >= STOP_OUT_LEVEL:
            break
        worst = min(
            acct["open"], key=lambda t: trade_pnl(acct, t, last_prices.get(t["code"], t["entry"]))
        )
        price = last_prices.get(worst["code"], worst["entry"])
        closed.append(close_trade(acct, worst["id"], price, date, "stop_out"))
    return closed


def load(path: Path = ACCOUNT_FILE) -> dict | None:
    try:
        with open(path, encoding="utf-8") as fh:
            acct = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    trades = acct.get("open", []) + acct.get("closed", [])
    if "balance" not in acct or any("code" not in t for t in trades):
        return None  # account from the older stock-trading version: start fresh
    return acct


def save(acct: dict, path: Path = ACCOUNT_FILE) -> None:
    write_json_atomic(acct, path)
