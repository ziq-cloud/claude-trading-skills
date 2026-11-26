"""Forex Trading Trainer — Streamlit entry point.

Run from the repository root:
    streamlit run webapp/app.py
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from views import (  # noqa: E402
    calc_page,
    chart_page,
    demo_page,
    home_page,
    lang,
    learn_page,
    nav,
    replay_page,
)
from views.lang import t  # noqa: E402
from views.state import level_info  # noqa: E402

st.set_page_config(page_title="Trading Skills", page_icon="📈", layout="wide")
lang.selector()


def page(fn, key, icon, default=False):
    # The default page is served at "/", so it must not get its own url_path.
    p = st.Page(
        fn,
        title=t(f"nav.{key}"),
        icon=icon,
        default=default,
        **({} if default else {"url_path": key}),
    )
    nav.PAGES[key] = p
    return p


sections = {
    "": [page(home_page.render, "home", "🏠", default=True)],
    t("nav.train"): [
        page(learn_page.render, "learn", "🎓"),
        page(replay_page.render, "replay", "⏪"),
        page(demo_page.render, "demo", "💼"),
    ],
    t("nav.tools"): [
        page(chart_page.render, "chart", "📊"),
        page(calc_page.render, "calc", "🧮"),
    ],
}
navigation = st.navigation(sections)

level, info, _, _ = level_info()
st.sidebar.markdown("### " + t("side.level", n=level, name=info["name"]))
st.sidebar.progress(level / 4)
st.sidebar.caption(t("side.disclaimer"))
navigation.run()
