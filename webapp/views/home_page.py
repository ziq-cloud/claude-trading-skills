import streamlit as st
from core import catalog

from views import nav


def render():
    st.title("📈 Trading Skills")
    st.write(
        "A web front end for the skills in this repository. "
        "Each tool here calls the same Python scripts the Claude skills use."
    )
    skills = catalog.load_skills()
    free = sum(1 for s in skills if s.api_level == "none")
    c1, c2, c3 = st.columns(3)
    c1.metric("Skills in catalog", len(skills))
    c2.metric("Work without a paid API", free)
    c3.metric("Need FMP / FINVIZ / Alpaca", len(skills) - free)

    st.subheader("Tools")
    cols = st.columns(2)
    tools = [
        ("chart", "📊 Price Chart", "Candles, SMA 20/50/200, RSI and ATR for any ticker."),
        ("sizer", "🧮 Position Sizer", "Risk-based share count: fixed %, ATR or Kelly."),
        ("breadth", "🌡️ Market Breadth", "0–100 breadth health score from public CSV data."),
        ("catalog", "📚 Skill Catalog", "Browse all skills, filter by category and API need."),
    ]
    for i, (path, title, desc) in enumerate(tools):
        with cols[i % 2].container(border=True):
            st.page_link(nav.PAGES[path], label=f"**{title}**")
            st.caption(desc)

    st.info(
        "Suggested flow: check **Market Breadth** for the overall regime → look at a "
        "ticker in **Price Chart** → send its ATR to the **Position Sizer** to get a share count."
    )
