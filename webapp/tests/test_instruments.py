"""Forex / gold / BTC / WTI contract maths and fixed lot sizes."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import instruments as ins  # noqa: E402


def test_catalogue_is_forex_metals_crypto_oil_only():
    codes = set(ins.INSTRUMENTS)
    assert {"EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "NZDUSD", "USDCAD"} <= codes
    assert {"XAUUSD", "BTCUSD", "WTI"} <= codes
    assert len(codes) == 10


def test_fixed_lot_sizes():
    assert ins.LOT_SIZES == [0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00]


def test_pip_value_eurusd_standard_lot():
    eur = ins.get("EURUSD")
    assert ins.pip_value_usd(eur, 1.0, price=1.10) == pytest.approx(10.0)
    assert ins.pip_value_usd(eur, 0.01, price=1.10) == pytest.approx(0.10)


def test_pip_value_usdjpy_converts_from_yen():
    jpy = ins.get("USDJPY")
    # 0.01 JPY × 100,000 = 1,000 JPY = $6.67 at 150
    assert ins.pip_value_usd(jpy, 1.0, price=150.0) == pytest.approx(1000 / 150)


def test_gold_btc_wti_move_values():
    assert ins.move_value_usd(ins.get("XAUUSD"), 10.0, lots=0.01, price=3500) == pytest.approx(10)
    assert ins.move_value_usd(ins.get("BTCUSD"), 1000, lots=0.01, price=60000) == pytest.approx(10)
    assert ins.move_value_usd(ins.get("WTI"), 1.0, lots=0.01, price=70) == pytest.approx(10)


def test_cent_scale_is_one_hundredth():
    eur = ins.get("EURUSD")
    assert ins.pip_value_usd(eur, 0.01, price=1.1, scale=0.01) == pytest.approx(0.001)


def test_margin_uses_leverage():
    eur = ins.get("EURUSD")
    assert ins.margin_usd(eur, 1.0, price=1.10) == pytest.approx(110_000 / 100)
    jpy = ins.get("USDJPY")
    assert ins.margin_usd(jpy, 1.0, price=150) == pytest.approx(100_000 / 100)
    btc = ins.get("BTCUSD")
    assert btc.leverage == 20
    assert ins.margin_usd(btc, 0.1, price=60_000) == pytest.approx(6000 / 20)


def test_pips_between():
    assert ins.pips(ins.get("EURUSD"), 1.1000, 1.0980) == pytest.approx(20)
    assert ins.pips(ins.get("USDJPY"), 150.00, 150.35) == pytest.approx(35)


def test_suggest_lot_picks_largest_fixed_size_within_risk_and_margin():
    eur = ins.get("EURUSD")
    # $1,000, 1% = $10; 20-pip stop -> $0.50/pip -> 0.05 lot exactly
    lot = ins.suggest_lot(eur, equity=1000, free_margin=1000, entry=1.1, stop=1.098, risk_pct=1)
    assert lot == 0.05
    # 30-pip stop -> exact 0.033 -> nearest fixed size below is 0.02
    lot = ins.suggest_lot(eur, equity=1000, free_margin=1000, entry=1.1, stop=1.097, risk_pct=1)
    assert lot == 0.02
    # even 0.01 too risky
    assert ins.suggest_lot(eur, 100, 100, 1.1, 1.09, risk_pct=0.5) is None
    # cent account makes it possible
    assert ins.suggest_lot(eur, 100, 100, 1.1, 1.09, risk_pct=0.5, scale=0.01) == 0.05


def test_suggest_lot_respects_margin():
    gold = ins.get("XAUUSD")
    # 0.01 lot gold needs $35 margin at 3500 / 1:100
    assert ins.suggest_lot(gold, 1000, 20, 3500, 3490, risk_pct=2) is None
