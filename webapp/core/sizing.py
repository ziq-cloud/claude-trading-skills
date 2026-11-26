"""Thin wrapper around skills/position-sizer/scripts/position_sizer.py."""

from __future__ import annotations

import importlib.util
import sys

from .paths import SKILLS_DIR

_SCRIPT = SKILLS_DIR / "position-sizer" / "scripts" / "position_sizer.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("_webapp_position_sizer", _SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_ps = _load_module()


def size_position(
    account_size: float,
    entry: float | None = None,
    stop: float | None = None,
    risk_pct: float | None = None,
    atr: float | None = None,
    atr_multiplier: float = 2.0,
    win_rate: float | None = None,
    avg_win: float | None = None,
    avg_loss: float | None = None,
    max_position_pct: float | None = None,
    max_sector_pct: float | None = None,
    sector: str | None = None,
    current_sector_exposure: float = 0.0,
    fractional_shares: bool = False,
) -> dict:
    """Run the position-sizer skill. Raises ValueError on invalid input."""
    params = _ps.SizingParameters(
        account_size=account_size,
        entry_price=entry,
        stop_price=stop,
        risk_pct=risk_pct,
        atr=atr,
        atr_multiplier=atr_multiplier,
        win_rate=win_rate,
        avg_win=avg_win,
        avg_loss=avg_loss,
        max_position_pct=max_position_pct,
        max_sector_pct=max_sector_pct,
        sector=sector or None,
        current_sector_exposure=current_sector_exposure,
        fractional_shares=fractional_shares,
    )
    return _ps.calculate_position(params)


def markdown_report(result: dict) -> str:
    return _ps.generate_markdown_report(result)
