"""Every UI string must exist in all four languages with matching placeholders."""

import string
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core import i18n, training  # noqa: E402


def _fields(text):
    return {f for _, f, _, _ in string.Formatter().parse(text) if f}


@pytest.mark.parametrize("key", sorted(i18n.STRINGS))
def test_all_languages_present_and_consistent(key):
    entry = i18n.STRINGS[key]
    assert set(entry) == set(i18n.LANGUAGES), key
    en = entry["en"]
    for lang, value in entry.items():
        assert value, f"{key}/{lang} empty"
        if isinstance(en, list):
            assert isinstance(value, list) and len(value) == len(en), f"{key}/{lang}"
        else:
            assert _fields(value) == _fields(en), f"{key}/{lang} placeholders differ"


def test_lookup_and_fallback():
    assert i18n.t("nav.home", "ms") == "Laman Utama"
    assert i18n.t("nav.home", "xx") == i18n.t("nav.home", "en")
    assert i18n.t("no.such.key", "en") == "no.such.key"
    assert "3" in i18n.t("replay.more", "zh", n=3)


def test_training_content_is_translated():
    for n, lv in training.LEVELS.items():
        for part in ("name", "goal", "unlock"):
            assert f"level.{n}.{part}" in i18n.STRINGS
        for lesson in lv["lessons"]:
            assert f"lesson.{lesson}.title" in i18n.STRINGS
            assert f"lesson.{lesson}.body" in i18n.STRINGS
    for i, q in enumerate(training.QUIZ, start=1):
        opts = i18n.STRINGS[f"quiz.{i}.opts"]["en"]
        assert 0 <= q["answer"] < len(opts)
