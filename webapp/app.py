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
    learn_page,
    nav,
    replay_page,
    sizer_page,
)
from views.state import level_info  # noqa: E402

st.set_page_config(page_title="Trading Skills", page_icon="📈", layout="wide")

sections = {
    "": [st.Page(home_page.render, title="Home", icon="🏠", url_path="home", default=True)],
    "Train": [
        st.Page(learn_page.render, title="Learning Path", icon="🎓", url_path="learn"),
        st.Page(replay_page.render, title="Chart Replay", icon="⏪", url_path="replay"),
        st.Page(demo_page.render, title="Demo Account", icon="💼", url_path="demo"),
    ],
    "Tools": [
        st.Page(chart_page.render, title="Price Chart", icon="📊", url_path="chart"),
        st.Page(sizer_page.render, title="Position Sizer", icon="🧮", url_path="sizer"),
        st.Page(breadth_page.render, title="Market Breadth", icon="🌡️", url_path="breadth"),
        st.Page(catalog_page.render, title="Skill Catalog", icon="📚", url_path="catalog"),
    ],
}
pages = [p for group in sections.values() for p in group]

nav.PAGES.update({p.url_path: p for p in pages})
navigation = st.navigation(sections)
level, info, _, _ = level_info()
st.sidebar.markdown(f"### Level {level}: {info['name']}")
st.sidebar.progress(level / 4)
st.sidebar.caption(
    "For education and analysis only — not financial advice. "
    "Always verify numbers before placing a trade."
)
navigation.run()
