import streamlit as st
from core import catalog
from core.paths import SKILLS_DIR


@st.cache_data
def _skills():
    return catalog.load_skills()


def render():
    st.title("📚 Skill Catalog")
    skills = _skills()

    c1, c2, c3 = st.columns([2, 2, 2])
    query = c1.text_input("Search", placeholder="e.g. dividend, breakout, earnings")
    cats = c2.multiselect(
        "Category", list(catalog.CATEGORY_LABELS), format_func=catalog.CATEGORY_LABELS.get
    )
    apis = c3.multiselect(
        "API requirement", list(catalog.API_LEVEL_LABELS), format_func=catalog.API_LEVEL_LABELS.get
    )

    found = catalog.filter_skills(skills, query, set(cats) or None, set(apis) or None)
    st.caption(f"{len(found)} of {len(skills)} skills")

    badge = {"none": "🟢", "optional": "🟡", "required": "🔴"}
    for s in found:
        with st.expander(f"{badge[s.api_level]} **{s.display_name}** — {s.category_label}"):
            st.write(s.summary)
            st.caption(
                f"Status: {s.status} · Timeframe: {s.timeframe or '—'} · "
                f"Difficulty: {s.difficulty or '—'} · {catalog.API_LEVEL_LABELS[s.api_level]}"
            )
            if s.integrations:
                st.markdown("**Integrations**")
                for i in s.integrations:
                    note = f" — {i['note']}" if i.get("note") else ""
                    st.markdown(f"- `{i.get('id')}` ({i.get('requirement', '?')}){note}")
            skill_md = SKILLS_DIR / s.id / "SKILL.md"
            if skill_md.exists():
                st.caption(f"Definition: skills/{s.id}/SKILL.md")
