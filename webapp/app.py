"""Trading Skills Web App — Streamlit entry point.

Run from the repository root:
    streamlit run webapp/app.py
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from views import breadth_page, catalog_page, chart_page, home_page, nav, sizer_page  # noqa: E402

st.set_page_config(page_title="Trading Skills", page_icon="📈", layout="wide")

pages = [
    st.Page(home_page.render, title="Home", icon="🏠", url_path="home", default=True),
    st.Page(chart_page.render, title="Price Chart", icon="📊", url_path="chart"),
    st.Page(sizer_page.render, title="Position Sizer", icon="🧮", url_path="sizer"),
    st.Page(breadth_page.render, title="Market Breadth", icon="🌡️", url_path="breadth"),
    st.Page(catalog_page.render, title="Skill Catalog", icon="📚", url_path="catalog"),
]

nav.PAGES.update({p.url_path: p for p in pages})
navigation = st.navigation(pages)
st.sidebar.caption(
    "For education and analysis only — not financial advice. "
    "Always verify numbers before placing a trade."
)
navigation.run()
