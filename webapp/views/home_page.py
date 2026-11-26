import streamlit as st
from core import catalog

from views import nav
from views.lang import t
from views.state import level_info


def render():
    st.title("📈 Trading Skills")
    st.write(t("home.intro"))
    level, info, _, _ = level_info()
    with st.container(border=True):
        st.markdown(t("home.you_are", n=level, name=info["name"], goal=info["goal"]))
        st.caption(t("home.next", unlock=info["unlock"]))
        st.page_link(nav.PAGES["learn"], label=t("home.continue"), icon="🎓")

    skills = catalog.load_skills()
    free = sum(1 for s in skills if s.api_level == "none")
    c1, c2, c3 = st.columns(3)
    c1.metric(t("home.m_skills"), len(skills))
    c2.metric(t("home.m_free"), free)
    c3.metric(t("home.m_paid"), len(skills) - free)

    st.subheader(t("home.tools"))
    cols = st.columns(2)
    tools = [
        ("replay", "⏪"),
        ("demo", "💼"),
        ("chart", "📊"),
        ("sizer", "🧮"),
        ("breadth", "🌡️"),
        ("catalog", "📚"),
    ]
    for i, (key, icon) in enumerate(tools):
        with cols[i % 2].container(border=True):
            st.page_link(nav.PAGES[key], label=f"**{t('nav.' + key)}**", icon=icon)
            st.caption(t(f"home.desc.{key}"))
    st.info(t("home.path"))
