"""Paper-trading (demo) account: long-only, stop-loss mandatory, stored as local JSON."""

from __future__ import annotations

import json
import uuid
from pathlib import Path

import pandas as pd

from .training import STATE_DIR, write_json_atomic

ACCOUNT_FILE = STATE_DIR / "demo_account.json"


class RuleViolation(ValueError):
    """A trade breaks one of the demo account's risk rules."""


def new_account(starting_balance: float) -> dict:
    if starting_balance <= 0:
        raise ValueError("Starting balance must be positive")
    return {
        "starting_balance": float(starting_balance),
        "cash": float(starting_balance),
        "open": [],
        "closed": [],
    }


def equity(acct: dict, last_prices: dict[str, float]) -> float:
    value = acct["cash"]
    for t in acct["open"]:
        value += t["shares"] * last_prices.get(t["symbol"], t["entry"])
    return value


def open_trade(
    acct: dict,
    symbol: str,
    entry: float,
    stop: float,
    target: float | None,
    shares: float,
    date: str,
    max_risk_pct: float,
    note: str = "",
) -> dict:
    if shares <= 0:
        raise RuleViolation("Shares must be positive")
    if stop is None or stop >= entry:
        raise RuleViolation("A stop-loss below the entry price is required")
    if target is not None and target <= entry:
        raise RuleViolation("Target must be above entry")
    cost = entry * shares
    if cost > acct["cash"] + 1e-9:
        raise RuleViolation(f"Not enough cash: need ${cost:,.2f}, have ${acct['cash']:,.2f}")
    risk = (entry - stop) * shares
    account_value = acct["cash"] + sum(t["entry"] * t["shares"] for t in acct["open"])
    risk_pct = risk / account_value * 100
    if risk_pct > max_risk_pct + 1e-9:
        raise RuleViolation(
            f"Trade risk {risk_pct:.2f}% exceeds your level's limit of {max_risk_pct}%. "
            "Reduce shares or tighten the stop."
        )
    trade = {
        "id": uuid.uuid4().hex[:8],
        "symbol": symbol,
        "entry": float(entry),
        "stop": float(stop),
        "target": None if target is None else float(target),
        "shares": shares,
        "entry_date": str(date),
        "risk_dollars": round(risk, 2),
        "risk_pct": round(risk_pct, 2),
        "note": note,
    }
    acct["cash"] -= cost
    acct["open"].append(trade)
    return trade


def close_trade(acct: dict, trade_id: str, price: float, date: str, reason: str) -> dict:
    idx = next((i for i, t in enumerate(acct["open"]) if t["id"] == trade_id), None)
    if idx is None:
        raise KeyError(trade_id)
    t = acct["open"].pop(idx)
    pnl = (price - t["entry"]) * t["shares"]
    closed = {
        **t,
        "exit_price": float(price),
        "exit_date": str(date),
        "exit_reason": reason,
        "pnl": round(pnl, 2),
        "r_multiple": round((price - t["entry"]) / (t["entry"] - t["stop"]), 2),
    }
    acct["cash"] += price * t["shares"]
    acct["closed"].append(closed)
    return closed


def check_exits(acct: dict, bars_by_symbol: dict[str, pd.DataFrame]) -> list[dict]:
    """Close open trades whose stop or target was touched on a bar after the entry date."""
    exits = []
    for t in list(acct["open"]):
        bars = bars_by_symbol.get(t["symbol"])
        if bars is None or bars.empty:
            continue
        after = bars[bars.index > pd.Timestamp(t["entry_date"])]
        for ts, bar in after.iterrows():
            if bar["low"] <= t["stop"]:
                price, reason = min(bar["open"], t["stop"]), "stop"
            elif t["target"] is not None and bar["high"] >= t["target"]:
                price, reason = max(bar["open"], t["target"]), "target"
            else:
                continue
            exits.append(close_trade(acct, t["id"], float(price), ts.date().isoformat(), reason))
            break
    return exits


def load(path: Path = ACCOUNT_FILE) -> dict | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save(acct: dict, path: Path = ACCOUNT_FILE) -> None:
    write_json_atomic(acct, path)
