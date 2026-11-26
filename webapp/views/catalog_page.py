import streamlit as st
from core import catalog

from views.lang import t


@st.cache_data
def _skills():
    return catalog.load_skills()


def render():
    st.title("📚 " + t("nav.catalog"))
    skills = _skills()
    c1, c2, c3 = st.columns(3)
    query = c1.text_input(t("catalog.search"), placeholder=t("catalog.placeholder"))
    cats = c2.multiselect(
        t("catalog.category"), list(catalog.CATEGORY_LABELS), format_func=lambda c: t(f"cat.{c}")
    )
    apis = c3.multiselect(
        t("catalog.api"), list(catalog.API_LEVEL_LABELS), format_func=lambda a: t(f"api.{a}")
    )
    found = catalog.filter_skills(skills, query, set(cats) or None, set(apis) or None)
    st.caption(t("catalog.count", n=len(found), total=len(skills)))

    badge = {"none": "🟢", "optional": "🟡", "required": "🔴"}
    for s in found:
        with st.expander(f"{badge[s.api_level]} **{s.display_name}** — {t('cat.' + s.category)}"):
            st.write(s.summary)
            st.caption(
                t(
                    "catalog.meta",
                    status=s.status,
                    tf=s.timeframe or "—",
                    diff=s.difficulty or "—",
                    api=t(f"api.{s.api_level}"),
                )
            )
            if s.integrations:
                st.markdown(f"**{t('catalog.integrations')}**")
                for i in s.integrations:
                    note = f" — {i['note']}" if i.get("note") else ""
                    st.markdown(f"- `{i.get('id')}` ({i.get('requirement', '?')}){note}")
            st.caption(f"skills/{s.id}/SKILL.md")
