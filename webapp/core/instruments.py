"""Tradable instruments: major forex pairs, gold, bitcoin and WTI crude.

Contract sizes follow common retail-broker specs (they vary by broker):
  forex 100,000 units/lot · XAUUSD 100 oz/lot · BTCUSD 1 BTC/lot · WTI 1,000 bbl/lot.
Every pair either quotes in USD (EURUSD, XAUUSD, ...) or has USD as the base
(USDJPY, USDCHF, USDCAD), so P&L converts to USD without a third rate.

A cent account trades 1/100 of the standard contract (`scale=0.01`): the same lot size
shows the same numbers, but in US cents instead of dollars.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

LOT_SIZES = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00]


@dataclass(frozen=True)
class Instrument:
    code: str
    name: str
    kind: str  # forex | metal | crypto | energy
    contract_size: float
    pip: float
    digits: int
    leverage: int
    td_symbol: str | None  # Twelve Data
    yf_symbol: str  # Yahoo Finance fallback

    @property
    def usd_base(self) -> bool:
        """True for USDJPY-style pairs where P&L is in the quote currency."""
        return self.code.startswith("USD") and self.kind == "forex"


def _fx(code, pip=0.0001, digits=5):
    return Instrument(
        code,
        f"{code[:3]}/{code[3:]}",
        "forex",
        100_000,
        pip,
        digits,
        100,
        f"{code[:3]}/{code[3:]}",
        f"{code}=X",
    )


INSTRUMENTS: dict[str, Instrument] = {
    i.code: i
    for i in [
        _fx("EURUSD"),
        _fx("GBPUSD"),
        _fx("USDJPY", pip=0.01, digits=3),
        _fx("USDCHF"),
        _fx("AUDUSD"),
        _fx("NZDUSD"),
        _fx("USDCAD"),
        Instrument("XAUUSD", "XAU/USD (Gold)", "metal", 100, 0.1, 2, 100, "XAU/USD", "GC=F"),
        Instrument("BTCUSD", "BTC/USD (Bitcoin)", "crypto", 1, 1.0, 2, 20, "BTC/USD", "BTC-USD"),
        # Twelve Data's WTI spot needs a paid plan, so WTI comes from Yahoo futures.
        Instrument("WTI", "WTI Crude Oil", "energy", 1_000, 0.01, 2, 100, None, "CL=F"),
    ]
}


def get(code: str) -> Instrument:
    return INSTRUMENTS[code]


def units(inst: Instrument, lots: float, scale: float = 1.0) -> float:
    return lots * inst.contract_size * scale


def move_value_usd(
    inst: Instrument, move: float, lots: float, price: float, scale: float = 1.0
) -> float:
    """USD value of a `move` in price for `lots` (positive move = price up)."""
    value = move * units(inst, lots, scale)
    return value / price if inst.usd_base else value


def pip_value_usd(inst: Instrument, lots: float, price: float, scale: float = 1.0) -> float:
    return move_value_usd(inst, inst.pip, lots, price, scale)


def notional_usd(inst: Instrument, lots: float, price: float, scale: float = 1.0) -> float:
    u = units(inst, lots, scale)
    return u if inst.usd_base else u * price


def margin_usd(inst: Instrument, lots: float, price: float, scale: float = 1.0) -> float:
    return notional_usd(inst, lots, price, scale) / inst.leverage


def pips(inst: Instrument, a: float, b: float) -> float:
    return abs(a - b) / inst.pip


def risk_usd(inst: Instrument, lots: float, entry: float, stop: float, scale: float = 1.0) -> float:
    return move_value_usd(inst, abs(entry - stop), lots, entry, scale)


def suggest_lot(
    inst: Instrument,
    equity: float,
    free_margin: float,
    entry: float,
    stop: float,
    risk_pct: float,
    scale: float = 1.0,
) -> float | None:
    """Largest fixed lot size whose stop-loss risk and margin both fit, else None."""
    if entry == stop or not math.isfinite(entry) or not math.isfinite(stop):
        return None
    cap = equity * risk_pct / 100
    best = None
    for lot in LOT_SIZES:
        if (
            risk_usd(inst, lot, entry, stop, scale) <= cap + 1e-9
            and margin_usd(inst, lot, entry, scale) <= free_margin + 1e-9
        ):
            best = lot
    return best


def fmt_price(inst: Instrument, price: float) -> str:
    return f"{price:,.{inst.digits}f}"
