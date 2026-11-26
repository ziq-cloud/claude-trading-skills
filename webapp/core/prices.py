"""Daily OHLCV fetching: Twelve Data first, yfinance as a fallback."""

from __future__ import annotations

import os
import re

import pandas as pd
import requests

TWELVEDATA_URL = "https://api.twelvedata.com/time_series"
TIMEOUT = 20
_SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-^=/]{0,14}$")


class PriceDataError(RuntimeError):
    pass


def clean_symbol(symbol: str) -> str:
    s = (symbol or "").strip().upper()
    if not _SYMBOL_RE.match(s):
        raise ValueError(f"Invalid ticker symbol: {symbol!r}")
    return s


def parse_twelvedata(payload: dict) -> pd.DataFrame:
    if payload.get("status") == "error" or "values" not in payload:
        raise PriceDataError(payload.get("message", "Twelve Data returned no values"))
    df = pd.DataFrame(payload["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").sort_index()
    cols = ["open", "high", "low", "close", "volume"]
    if "volume" not in df:
        df["volume"] = 0
    return df[cols].astype(float)


def fetch_twelvedata(symbol: str, outputsize: int = 500) -> pd.DataFrame:
    params = {"symbol": symbol, "interval": "1day", "outputsize": outputsize}
    key = os.environ.get("TWELVEDATA_API_KEY")
    if key:
        params["apikey"] = key
    try:
        resp = requests.get(TWELVEDATA_URL, params=params, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise PriceDataError(f"Twelve Data request failed: {exc}") from exc
    if resp.status_code != 200:
        raise PriceDataError(f"Twelve Data HTTP {resp.status_code}")
    return parse_twelvedata(resp.json())


def fetch_yfinance(symbol: str, period: str = "2y") -> pd.DataFrame:
    try:
        import yfinance as yf
    except ImportError as exc:
        raise PriceDataError("yfinance not installed (pip install yfinance)") from exc
    try:
        df = yf.Ticker(symbol).history(period=period, interval="1d", auto_adjust=False)
    except Exception as exc:  # network/proxy/parse errors from yfinance's HTTP stack
        raise PriceDataError(f"yfinance request failed: {exc}") from exc
    if df is None or df.empty:
        raise PriceDataError(f"yfinance returned no data for {symbol}")
    df = df.rename(columns=str.lower)[["open", "high", "low", "close", "volume"]]
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df.astype(float)


def fetch_instrument(inst, source: str = "auto") -> tuple[pd.DataFrame, str]:
    """Daily OHLC for an instruments.Instrument: Twelve Data, then Yahoo Finance."""
    errors = []
    order = ["twelvedata", "yfinance"] if source == "auto" else [source]
    for src in order:
        try:
            if src == "twelvedata":
                if not inst.td_symbol:
                    continue
                return fetch_twelvedata(inst.td_symbol), "Twelve Data"
            return fetch_yfinance(inst.yf_symbol), "Yahoo Finance"
        except PriceDataError as exc:
            errors.append(f"{src}: {exc}")
    raise PriceDataError("; ".join(errors) or "no data source for this instrument")


def fetch_daily(symbol: str, source: str = "auto") -> tuple[pd.DataFrame, str]:
    """Return (dataframe, source_used). source: 'auto' | 'twelvedata' | 'yfinance'."""
    symbol = clean_symbol(symbol)
    errors = []
    order = ["twelvedata", "yfinance"] if source == "auto" else [source]
    for src in order:
        try:
            if src == "twelvedata":
                return fetch_twelvedata(symbol), "Twelve Data"
            return fetch_yfinance(symbol), "yfinance"
        except PriceDataError as exc:
            errors.append(f"{src}: {exc}")
    raise PriceDataError("; ".join(errors))
