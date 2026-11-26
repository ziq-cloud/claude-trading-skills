"""Simple technical indicators on an OHLCV DataFrame."""

from __future__ import annotations

import pandas as pd


def add_indicators(
    df: pd.DataFrame, sma_windows=(20, 50, 200), rsi_period: int = 14, atr_period: int = 14
) -> pd.DataFrame:
    out = df.copy()
    for w in sma_windows:
        out[f"sma_{w}"] = out["close"].rolling(w).mean()

    # RSI (Wilder smoothing)
    delta = out["close"].diff()
    gain = (
        delta.clip(lower=0).ewm(alpha=1 / rsi_period, adjust=False, min_periods=rsi_period).mean()
    )
    loss = (
        (-delta.clip(upper=0))
        .ewm(alpha=1 / rsi_period, adjust=False, min_periods=rsi_period)
        .mean()
    )
    rs = gain / loss
    rsi = 100 - 100 / (1 + rs)
    out[f"rsi_{rsi_period}"] = rsi.where(loss != 0, 100.0).where(gain.notna())

    # ATR (Wilder smoothing)
    prev_close = out["close"].shift(1)
    tr = pd.concat(
        [
            out["high"] - out["low"],
            (out["high"] - prev_close).abs(),
            (out["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    out[f"atr_{atr_period}"] = tr.ewm(
        alpha=1 / atr_period, adjust=False, min_periods=atr_period
    ).mean()
    return out
