"""Registry of StreamlitPage objects so pages can link to each other."""

PAGES: dict = {}


def go(url_path: str):
    import streamlit as st

    st.switch_page(PAGES[url_path])
