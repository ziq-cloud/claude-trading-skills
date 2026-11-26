"""Shared UI helpers: instrument picker and cached daily prices."""

import streamlit as st
from core import indicators, prices
from core import instruments as ins

from views.lang import t


@st.cache_data(ttl=600, show_spinner=False)
def bars(code: str):
    df, source = prices.fetch_instrument(ins.get(code))
    return indicators.add_indicators(df), source


def instrument_picker(key: str, container=st, default: str = "EURUSD") -> str:
    codes = list(ins.INSTRUMENTS)
    return container.selectbox(
        t("common.instrument"),
        codes,
        index=codes.index(st.session_state.get(key, default)),
        format_func=lambda c: ins.get(c).name,
        key=key,
    )


def price_input(container, label, inst, value, key):
    return container.number_input(
        label,
        value=float(round(value, inst.digits)),
        step=inst.pip,
        format=f"%.{inst.digits}f",
        key=key,
    )
