"""Shared helpers for the trader's level and saved state."""

from core import demo_account, training


def level_info() -> tuple[int, dict, training.Progress, dict | None]:
    progress = training.load_progress()
    acct = demo_account.load()
    closed = acct["closed"] if acct else []
    level = training.current_level(progress, closed)
    return level, training.LEVELS[level], progress, acct
