"""Trading Skills Web App — Streamlit entry point.

Run from the repository root:
    streamlit run webapp/app.py
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from views import (  # noqa: E402
    breadth_page,
    catalog_page,
    chart_page,
    demo_page,
    home_page,
    lang,
    learn_page,
    nav,
    replay_page,
    sizer_page,
)
from views.lang import t  # noqa: E402
from views.state import level_info  # noqa: E402

st.set_page_config(page_title="Trading Skills", page_icon="📈", layout="wide")
lang.selector()


def page(fn, key, icon, default=False):
    return st.Page(fn, title=t(f"nav.{key}"), icon=icon, url_path=key, default=default)


sections = {
    "": [page(home_page.render, "home", "🏠", default=True)],
    t("nav.train"): [
        page(learn_page.render, "learn", "🎓"),
        page(replay_page.render, "replay", "⏪"),
        page(demo_page.render, "demo", "💼"),
    ],
    t("nav.tools"): [
        page(chart_page.render, "chart", "📊"),
        page(sizer_page.render, "sizer", "🧮"),
        page(breadth_page.render, "breadth", "🌡️"),
        page(catalog_page.render, "catalog", "📚"),
    ],
}
nav.PAGES.update({p.url_path: p for group in sections.values() for p in group})
navigation = st.navigation(sections)

level, info, _, _ = level_info()
st.sidebar.markdown("### " + t("side.level", n=level, name=info["name"]))
st.sidebar.progress(level / 4)
st.sidebar.caption(t("side.disclaimer"))
navigation.run()
