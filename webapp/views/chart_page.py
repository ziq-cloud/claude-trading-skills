import plotly.graph_objects as go
import streamlit as st
from core import instruments as ins
from core import prices
from plotly.subplots import make_subplots

from views import nav
from views.common import bars, instrument_picker
from views.lang import t


def _vs(price, ref):
    # The delta must start with its sign so Streamlit colours the arrow correctly.
    return None if ref != ref else f"{(price / ref - 1) * 100:+.2f}%"


def render():
    st.title("📊 " + t("nav.chart"))
    c1, c2 = st.columns([2, 1])
    code = instrument_picker("chart_code", c1)
    lookback = c2.selectbox(
        t("chart.show_last"),
        [60, 120, 250, 500],
        index=2,
        format_func=lambda n: t("chart.days", n=n),
    )
    inst = ins.get(code)
    try:
        df, used = bars(code)
    except prices.PriceDataError:
        st.error(t("common.price_error"))
        return
    view = df.tail(lookback)
    last, prev = df.iloc[-1], df.iloc[-2]
    p = lambda v: "—" if v != v else ins.fmt_price(inst, v)  # noqa: E731

    m = st.columns(5)
    m[0].metric(t("chart.close"), p(last.close), f"{(last.close / prev.close - 1) * 100:+.2f}%")
    m[1].metric("SMA 50", p(last.sma_50), _vs(last.close, last.sma_50))
    m[2].metric("SMA 200", p(last.sma_200), _vs(last.close, last.sma_200))
    m[3].metric("RSI 14", "—" if last.rsi_14 != last.rsi_14 else f"{last.rsi_14:.1f}")
    m[4].metric(
        "ATR 14",
        f"{ins.pips(inst, last.atr_14, 0):,.0f} pips",
        delta_color="off",
        delta=t("chart.atr_pct", pct=f"{last.atr_14 / last.close * 100:.2f}"),
    )

    has_vol = view.volume.sum() > 0
    rows = 3 if has_vol else 2
    heights = [0.62, 0.18, 0.20] if has_vol else [0.75, 0.25]
    fig = make_subplots(
        rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=heights
    )
    fig.add_trace(
        go.Candlestick(
            x=view.index,
            open=view.open,
            high=view.high,
            low=view.low,
            close=view.close,
            name=inst.name,
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
    if has_vol:
        fig.add_trace(
            go.Bar(x=view.index, y=view.volume, name=t("chart.volume"), marker_color="#8899aa"),
            row=2,
            col=1,
        )
    fig.add_trace(
        go.Scatter(x=view.index, y=view.rsi_14, name="RSI 14", line=dict(color="#7d3c98")),
        row=rows,
        col=1,
    )
    for lvl in (30, 70):
        fig.add_hline(y=lvl, line_dash="dot", line_color="gray", row=rows, col=1)
    fig.update_layout(
        height=640,
        xaxis_rangeslider_visible=False,
        margin=dict(t=10, b=10),
        legend=dict(orientation="h", y=1.02),
    )
    if inst.kind != "crypto":
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    st.plotly_chart(fig, use_container_width=True)
    st.caption(t("chart.caption", src=used, date=df.index[-1].date()))

    if st.button("🧮 " + t("nav.calc"), type="primary"):
        st.session_state["calc_prefill"] = {
            "code": code,
            "entry": float(last.close),
            "atr": float(last.atr_14),
        }
        st.session_state["calc_code"] = code
        nav.go("calc")
