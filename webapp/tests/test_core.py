"""Unit tests for the web app's pure helper modules (no network)."""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

WEBAPP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WEBAPP))

from core import breadth, catalog, indicators, prices, sizing  # noqa: E402

# ---------------------------------------------------------------- catalog


def test_load_catalog_reads_repo_index():
    skills = catalog.load_skills()
    ids = {s.id for s in skills}
    assert "position-sizer" in ids
    assert "market-breadth-analyzer" in ids
    ps = next(s for s in skills if s.id == "position-sizer")
    assert ps.api_level == "none"
    assert ps.display_name == "Position Sizer"


def test_api_level_classification():
    req = [{"id": "fmp", "requirement": "required"}]
    opt = [{"id": "fmp", "requirement": "optional"}]
    free = [{"id": "websearch", "requirement": "required"}]
    assert catalog.classify_api_level(req) == "required"
    assert catalog.classify_api_level(opt) == "optional"
    assert catalog.classify_api_level(free) == "none"
    assert catalog.classify_api_level([]) == "none"


def test_filter_skills():
    skills = catalog.load_skills()
    only_free = catalog.filter_skills(skills, api_levels={"none"})
    assert only_free and all(s.api_level == "none" for s in only_free)
    found = catalog.filter_skills(skills, query="dividend")
    assert found and all("dividend" in (s.display_name + s.summary).lower() for s in found)


# ---------------------------------------------------------------- sizing


def test_sizing_fixed_fractional():
    r = sizing.size_position(account_size=100_000, entry=155.0, stop=148.5, risk_pct=1.0)
    assert r["final_recommended_shares"] == 153
    assert r["final_risk_dollars"] == pytest.approx(994.5)


def test_sizing_rejects_stop_above_entry():
    with pytest.raises(ValueError):
        sizing.size_position(account_size=100_000, entry=100.0, stop=110.0, risk_pct=1.0)


def test_sizing_markdown_report():
    r = sizing.size_position(account_size=50_000, entry=50.0, stop=48.0, risk_pct=0.5)
    md = sizing.markdown_report(r)
    assert "Position" in md


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


# ---------------------------------------------------------------- breadth


def test_breadth_load_latest_report(tmp_path):
    (tmp_path / "market_breadth_2026-11-25_010101.json").write_text(json.dumps({"composite": 1}))
    (tmp_path / "market_breadth_2026-11-26_010101.json").write_text(
        json.dumps({"composite": {"composite_score": 62.5}})
    )
    (tmp_path / "market_breadth_history.json").write_text("[]")
    data = breadth.load_latest_report(tmp_path)
    assert data["composite"]["composite_score"] == 62.5


def test_breadth_component_table():
    analysis = {
        "components": {
            "ma_crossover": {"score": 40, "signal": "Weak"},
            "divergence": {"score": 80, "signal": "OK"},
        }
    }
    rows = breadth.component_rows(analysis)
    assert rows[0] == {
        "component": "8MA vs 200MA Crossover",
        "weight": "20%",
        "score": 40,
        "signal": "Weak",
    }
    assert len(rows) == 2
