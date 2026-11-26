"""Paper-trading (demo) account: long-only, stop-loss mandatory, stored as local JSON.

Two account types, like retail brokers offer:
  * standard — balance in USD, $100 to $1,000
  * cent     — balance in US cents (USC), 10,000 to 1,000,000 USC ($100 to $10,000)
All amounts are stored in USD; cent accounts are only displayed ×100.
Fractional shares are allowed so small accounts can trade high-priced stocks.
"""

from __future__ import annotations

import json
import math
import uuid
from pathlib import Path

import pandas as pd

from .training import STATE_DIR, write_json_atomic

ACCOUNT_FILE = STATE_DIR / "demo_account.json"

ACCOUNT_TYPES = {
    # type: (min, max, units per USD, choices in account units)
    "standard": (100, 1_000, 1, [100, 200, 300, 500, 750, 1_000]),
    "cent": (
        10_000,
        1_000_000,
        100,
        [10_000, 25_000, 50_000, 100_000, 250_000, 500_000, 1_000_000],
    ),
}
SHARE_DECIMALS = 4


class RuleViolation(ValueError):
    """A trade breaks one of the demo account's risk rules. `code` maps to a UI message."""

    def __init__(self, code: str, message: str, **params):
        super().__init__(message)
        self.code = code
        self.params = params


def new_account(starting_balance: float, account_type: str = "standard") -> dict:
    if account_type not in ACCOUNT_TYPES:
        raise ValueError(f"Unknown account type: {account_type}")
    lo, hi, per_usd, _ = ACCOUNT_TYPES[account_type]
    if not lo <= starting_balance <= hi:
        raise ValueError(f"{account_type} balance must be between {lo:,} and {hi:,}")
    usd = float(starting_balance) / per_usd
    return {
        "account_type": account_type,
        "starting_balance": usd,
        "cash": usd,
        "open": [],
        "closed": [],
    }


def fmt_money(acct: dict, usd: float) -> str:
    per_usd = ACCOUNT_TYPES[acct.get("account_type", "standard")][2]
    value = usd * per_usd
    if abs(value) < 0.005:
        value = 0.0
    sign = "-" if value < 0 else ""
    if per_usd == 1:
        return f"{sign}${abs(value):,.2f}"
    return f"{sign}{abs(value):,.2f} USC"


def fmt_shares(shares: float) -> str:
    return f"{shares:,.{SHARE_DECIMALS}f}".rstrip("0").rstrip(".")


def max_shares(cash: float, equity: float, entry: float, stop: float, risk_pct: float) -> float:
    """Largest share count (floored to SHARE_DECIMALS) allowed by the risk cap and cash."""
    if stop >= entry:
        return 0.0
    by_risk = equity * risk_pct / 100 / (entry - stop)
    by_cash = cash / entry
    scale = 10**SHARE_DECIMALS
    return math.floor(min(by_risk, by_cash) * scale) / scale


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
    shares = round(float(shares), SHARE_DECIMALS)
    if shares <= 0:
        raise RuleViolation("shares", "Shares must be positive")
    if stop is None or stop >= entry:
        raise RuleViolation("stop", "A stop-loss below the entry price is required")
    if target is not None and target <= entry:
        raise RuleViolation("target", "Target must be above entry")
    cost = entry * shares
    if cost > acct["cash"] + 1e-9:
        raise RuleViolation(
            "cash",
            f"Not enough cash: need {cost:,.2f}, have {acct['cash']:,.2f}",
            need=cost,
            have=acct["cash"],
        )
    risk = (entry - stop) * shares
    account_value = acct["cash"] + sum(t["entry"] * t["shares"] for t in acct["open"])
    risk_pct = risk / account_value * 100
    if risk_pct > max_risk_pct + 1e-9:
        raise RuleViolation(
            "risk",
            f"Trade risk {risk_pct:.2f}% exceeds the limit of {max_risk_pct}%",
            pct=round(risk_pct, 2),
            limit=max_risk_pct,
        )
    trade = {
        "id": uuid.uuid4().hex[:8],
        "symbol": symbol,
        "entry": float(entry),
        "stop": float(stop),
        "target": None if target is None else float(target),
        "shares": shares,
        "entry_date": str(date),
        "risk_dollars": round(risk, 4),
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
        "pnl": round(pnl, 4),
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
            acct = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    acct.setdefault("account_type", "standard")
    return acct


def save(acct: dict, path: Path = ACCOUNT_FILE) -> None:
    write_json_atomic(acct, path)
