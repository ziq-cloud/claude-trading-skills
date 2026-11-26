import streamlit as st
from core import demo_account, instruments

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

    c1, c2, c3 = st.columns(3)
    c1.metric(t("home.m_instruments"), len(instruments.INSTRUMENTS))
    c2.metric(t("home.m_lots"), f"{instruments.LOT_SIZES[0]:.2f} – {instruments.LOT_SIZES[-1]:.2f}")
    c3.metric(t("home.m_leverage"), f"1:{demo_account.DEFAULT_LEVERAGE}")
    st.caption(" · ".join(i.name for i in instruments.INSTRUMENTS.values()))

    st.subheader(t("home.tools"))
    cols = st.columns(2)
    for i, (key, icon) in enumerate(
        [("replay", "⏪"), ("demo", "💼"), ("chart", "📊"), ("calc", "🧮")]
    ):
        with cols[i % 2].container(border=True):
            st.page_link(nav.PAGES[key], label=f"**{t('nav.' + key)}**", icon=icon)
            st.caption(t(f"home.desc.{key}"))
    st.info(t("home.path"))
