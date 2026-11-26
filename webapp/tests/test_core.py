"""Unit tests for the web app's pure helper modules (no network)."""

import sys
from pathlib import Path

import pandas as pd
import pytest

WEBAPP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WEBAPP))

from core import indicators, instruments, prices  # noqa: E402

# ---------------------------------------------------------------- indicators


def _ohlc(n=60):
    closes = [100 + i for i in range(n)]
    return pd.DataFrame(
        {
            "open": closes,
            "high": [c + 2 for c in closes],
            "low": [c - 2 for c in closes],
            "close": closes,
            "volume": [1000] * n,
        },
        index=pd.date_range("2026-01-01", periods=n, freq="D"),
    )


def test_sma_and_atr():
    df = indicators.add_indicators(_ohlc(), sma_windows=(10,))
    assert df["sma_10"].iloc[-1] == pytest.approx(sum(range(150, 160)) / 10)
    # high-low range is 4, gaps are 1 -> true range is 4 throughout
    assert df["atr_14"].iloc[-1] == pytest.approx(4.0)


def test_rsi_all_gains_is_100():
    df = indicators.add_indicators(_ohlc(), sma_windows=())
    assert df["rsi_14"].iloc[-1] == pytest.approx(100.0)


# ---------------------------------------------------------------- prices


def test_parse_twelvedata_payload():
    payload = {
        "status": "ok",
        "values": [
            {
                "datetime": "2026-11-25",
                "open": "2",
                "high": "3",
                "low": "1",
                "close": "2.5",
                "volume": "10",
            },
            {
                "datetime": "2026-11-24",
                "open": "1",
                "high": "2",
                "low": "0.5",
                "close": "1.5",
                "volume": "20",
            },
        ],
    }
    df = prices.parse_twelvedata(payload)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert df.index.is_monotonic_increasing
    assert df["close"].iloc[-1] == 2.5


def test_parse_twelvedata_error():
    with pytest.raises(prices.PriceDataError, match="bad symbol"):
        prices.parse_twelvedata({"status": "error", "message": "bad symbol"})


def test_symbol_validation():
    assert prices.clean_symbol(" aapl ") == "AAPL"
    assert prices.clean_symbol("BRK.B") == "BRK.B"
    with pytest.raises(ValueError):
        prices.clean_symbol("AAPL; rm -rf")


def test_fetch_instrument_skips_twelvedata_without_symbol(monkeypatch):
    calls = []

    def fake_yf(symbol, period="2y"):
        calls.append(symbol)
        return pd.DataFrame()

    monkeypatch.setattr(prices, "fetch_yfinance", fake_yf)
    monkeypatch.setattr(prices, "fetch_twelvedata", lambda *a, **k: pytest.fail("no TD symbol"))
    prices.fetch_instrument(instruments.get("WTI"))
    assert calls == ["CL=F"]


def test_yfinance_network_errors_become_price_data_error(monkeypatch):
    import types

    class Boom:
        def __init__(self, *_):
            pass

        def history(self, **_):
            raise ConnectionError("proxy said no")

    monkeypatch.setitem(sys.modules, "yfinance", types.SimpleNamespace(Ticker=Boom))
    with pytest.raises(prices.PriceDataError, match="proxy said no"):
        prices.fetch_yfinance("CL=F")
