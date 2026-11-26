import streamlit as st
from core import catalog

from views import nav
from views.state import level_info


def render():
    st.title("📈 Trading Skills")
    st.write(
        "Learn to trade step by step, from zero to an advanced, rule-based process, "
        "with virtual money first. The tools use the same Python scripts as the Claude skills."
    )
    level, info, _, _ = level_info()
    with st.container(border=True):
        st.markdown(f"**You are at Level {level}: {info['name']}**: {info['goal']}")
        st.caption(f"Next: {info['unlock']}")
        st.page_link(nav.PAGES["learn"], label="Continue on the Learning Path →", icon="🎓")
    skills = catalog.load_skills()
    free = sum(1 for s in skills if s.api_level == "none")
    c1, c2, c3 = st.columns(3)
    c1.metric("Skills in catalog", len(skills))
    c2.metric("Work without a paid API", free)
    c3.metric("Need FMP / FINVIZ / Alpaca", len(skills) - free)

    st.subheader("Tools")
    cols = st.columns(2)
    tools = [
        ("replay", "⏪ Chart Replay", "Practise entries on hidden historical charts."),
        ("demo", "💼 Demo Account", "Paper trade with virtual money on real prices."),
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
        "Path: **Learning Path** (lessons + quiz) → **Chart Replay** (10 practice trades) → "
        "**Demo Account** (10 paper trades with positive expectancy) → Advanced tools."
    )
