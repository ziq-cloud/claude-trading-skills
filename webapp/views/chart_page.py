import plotly.graph_objects as go
import streamlit as st
from core import indicators, prices
from plotly.subplots import make_subplots

from views import nav
from views.lang import t


@st.cache_data(ttl=900, show_spinner=False)
def _load(symbol: str, source: str):
    return prices.fetch_daily(symbol, source)


def _fmt(v, nd=2):
    return "—" if v != v else f"{v:,.{nd}f}"  # NaN check


def _vs(price, ref):
    return None if ref != ref else t("chart.vs", pct=f"{(price / ref - 1) * 100:+.1f}")


def render():
    st.title("📊 " + t("nav.chart"))
    c1, c2, c3 = st.columns([2, 1, 1])
    symbol = c1.text_input(t("common.ticker"), value=st.session_state.get("chart_symbol", "AAPL"))
    source = c2.selectbox(t("chart.source"), ["auto", "twelvedata", "yfinance"])
    lookback = c3.selectbox(
        t("chart.show_last"),
        [60, 120, 250, 500],
        index=2,
        format_func=lambda n: t("chart.days", n=n),
    )
    try:
        sym = prices.clean_symbol(symbol)
        df, used = _load(sym, source)
    except ValueError as exc:
        st.error(str(exc))
        return
    except prices.PriceDataError:
        st.error(t("common.price_error"))
        return

    st.session_state["chart_symbol"] = sym
    df = indicators.add_indicators(df)
    view = df.tail(lookback)
    last, prev = df.iloc[-1], df.iloc[-2]

    m = st.columns(5)
    m[0].metric(
        t("chart.close"), f"{last.close:,.2f}", f"{(last.close / prev.close - 1) * 100:+.2f}%"
    )
    m[1].metric("SMA 50", _fmt(last.sma_50), _vs(last.close, last.sma_50))
    m[2].metric("SMA 200", _fmt(last.sma_200), _vs(last.close, last.sma_200))
    m[3].metric("RSI 14", _fmt(last.rsi_14, 1))
    m[4].metric(
        "ATR 14",
        _fmt(last.atr_14),
        t("chart.atr_pct", pct=f"{last.atr_14 / last.close * 100:.2f}"),
        delta_color="off",
    )

    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.62, 0.18, 0.20]
    )
    fig.add_trace(
        go.Candlestick(
            x=view.index, open=view.open, high=view.high, low=view.low, close=view.close, name=sym
        ),
        row=1,
        col=1,
    )
    for w, color in ((20, "#f2a900"), (50, "#2f7ed8"), (200, "#c0392b")):
        fig.add_trace(
            go.Scatter(
                x=view.index, y=view[f"sma_{w}"], name=f"SMA {w}", line=dict(width=1.4, color=color)
            ),
            row=1,
            col=1,
        )
    fig.add_trace(
        go.Bar(x=view.index, y=view.volume, name=t("chart.volume"), marker_color="#8899aa"),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=view.index, y=view.rsi_14, name="RSI 14", line=dict(color="#7d3c98")),
        row=3,
        col=1,
    )
    for lvl in (30, 70):
        fig.add_hline(y=lvl, line_dash="dot", line_color="gray", row=3, col=1)
    fig.update_layout(
        height=680,
        xaxis_rangeslider_visible=False,
        margin=dict(t=10, b=10),
        legend=dict(orientation="h", y=1.02),
    )
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    st.plotly_chart(fig, use_container_width=True)
    st.caption(t("chart.caption", src=used, date=df.index[-1].date()))

    if st.button(t("chart.to_sizer"), type="primary"):
        st.session_state["sizer_prefill"] = {
            "symbol": sym,
            "entry": round(float(last.close), 2),
            "atr": round(float(last.atr_14), 2),
        }
        nav.go("sizer")
