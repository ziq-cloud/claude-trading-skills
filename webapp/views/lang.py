"""Current UI language (sidebar selector, remembered in the ?lang= URL parameter)."""

import streamlit as st
from core import i18n


def current() -> str:
    return st.session_state.get("lang", i18n.DEFAULT_LANG)


def t(key: str, **kwargs):
    return i18n.t(key, current(), **kwargs)


def selector() -> None:
    if "lang" not in st.session_state:
        qp = st.query_params.get("lang")
        st.session_state.lang = qp if qp in i18n.LANGUAGES else i18n.DEFAULT_LANG
    st.sidebar.selectbox(
        "🌐 " + " / ".join(["Language", "Bahasa", "மொழி", "语言"]),
        list(i18n.LANGUAGES),
        format_func=i18n.LANGUAGES.get,
        key="lang",
    )
    st.query_params["lang"] = st.session_state.lang
