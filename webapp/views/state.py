"""Shared helpers for the trader's level and saved state."""

from core import demo_account, training

from views.lang import t


def level_info() -> tuple[int, dict, training.Progress, dict | None]:
    progress = training.load_progress()
    acct = demo_account.load()
    closed = acct["closed"] if acct else []
    level = training.current_level(progress, closed)
    info = {
        **training.LEVELS[level],
        "name": t(f"level.{level}.name"),
        "goal": t(f"level.{level}.goal"),
        "unlock": unlock_text(level),
    }
    return level, info, progress, acct


def unlock_text(level: int) -> str:
    n = {2: training.REPLAYS_FOR_LEVEL_3, 3: training.DEMO_TRADES_FOR_LEVEL_4}.get(level)
    return t(f"level.{level}.unlock", **({"n": n} if n else {}))
