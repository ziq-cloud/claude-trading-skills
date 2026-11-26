import random

import plotly.graph_objects as go
import streamlit as st
from core import instruments as ins
from core import prices, training

from views.common import bars, price_input
from views.lang import t
from views.state import level_info

POOL = list(ins.INSTRUMENTS)
VISIBLE = 120
HORIZON = 20


def _new_round():
    for _ in range(6):
        code = random.choice(POOL)
        try:
            df, _ = bars(code)
        except prices.PriceDataError:
            continue
        if len(df) >= 220 + HORIZON:
            cut = random.randint(220, len(df) - HORIZON)
            st.session_state.replay_round = {"code": code, "cut": cut, "result": None}
            return
    st.session_state.replay_round = None


def _chart(df, cut, show_future, trade=None):
    end = cut + (HORIZON if show_future else 0)
    view = df.iloc[cut - VISIBLE : end]
    x = list(range(len(view)))
    fig = go.Figure(
        go.Candlestick(
            x=x, open=view.open, high=view.high, low=view.low, close=view.close, name="price"
        )
    )
    for w, c in ((20, "#f2a900"), (50, "#2f7ed8"), (200, "#c0392b")):
        fig.add_trace(
            go.Scatter(x=x, y=view[f"sma_{w}"], name=f"SMA {w}", line=dict(width=1.3, color=c))
        )
    if show_future:
        fig.add_vrect(
            x0=VISIBLE - 0.5,
            x1=len(view) - 0.5,
            fillcolor="#2f7ed8",
            opacity=0.08,
            line_width=0,
            annotation_text=t("replay.hidden"),
            annotation_position="top left",
        )
    if trade:
        lines = (
            (trade["stop"], t("common.stop"), "#c0392b"),
            (trade["target"], t("common.target"), "#27ae60"),
            (trade["entry"], t("common.entry"), "#555"),
        )
        for y, name, c in lines:
            fig.add_hline(y=y, line_dash="dash", line_color=c, annotation_text=name)
    fig.update_layout(
        height=520,
        xaxis_rangeslider_visible=False,
        margin=dict(t=10, b=10),
        legend=dict(orientation="h", y=1.02),
        xaxis_title=t("replay.axis"),
    )
    return fig


def render():
    level, _, progress, _ = level_info()
    st.title("⏪ " + t("nav.replay"))
    st.write(t("replay.intro", h=HORIZON))

    if st.session_state.get("replay_round") is None:
        _new_round()
    rp = st.session_state.replay_round
    if rp is None:
        st.error(t("common.price_error"))
        return
    inst = ins.get(rp["code"])
    df, _ = bars(rp["code"])
    cut = rp["cut"]
    last = df.iloc[cut - 1]
    entry = round(float(last.close), inst.digits)
    atr = float(last.atr_14)

    stats = training.trade_stats(progress.replays)
    has = stats["trades"] > 0
    m = st.columns(4)
    m[0].metric(t("replay.m_trades"), stats["trades"])
    m[1].metric(t("common.win_rate"), f"{stats['win_rate']:.0%}" if has else "—")
    m[2].metric(t("common.expectancy"), f"{stats['expectancy_r']:+.2f}R" if has else "—")
    m[3].metric(t("replay.m_total"), f"{stats['total_r']:+.1f}R" if has else "—")

    if rp["result"] is None:
        st.plotly_chart(_chart(df, cut, False), use_container_width=True)
        st.caption(
            t(
                "replay.caption",
                close=ins.fmt_price(inst, entry),
                atr=f"{ins.pips(inst, atr, 0):,.0f} pips",
                rsi=f"{last.rsi_14:.0f}",
            )
        )
        side = st.radio(
            t("replay.side"),
            ["buy", "sell"],
            horizontal=True,
            format_func=lambda s: t(f"replay.{s}"),
            key=f"side_{rp['cut']}",
        )
        d = 1 if side == "buy" else -1
        c1, c2, c3 = st.columns(3)
        key = f"{rp['code']}_{cut}_{side}"
        stop = price_input(c1, t("common.stop"), inst, entry - d * atr, f"rs_{key}")
        target = price_input(c2, t("common.target"), inst, entry + d * 2 * atr, f"rt_{key}")
        reason = c3.text_input(t("replay.reason"), key=f"rr_{cut}")
        if (entry - stop) * d > 0:
            st.caption(
                t(
                    "replay.rr",
                    risk=f"{ins.pips(inst, entry, stop):,.0f} pips",
                    reward=f"{ins.pips(inst, entry, target):,.0f} pips",
                    rr=f"{abs(target - entry) / abs(entry - stop):.1f}",
                )
            )
        b1, b2 = st.columns(2)
        place = b1.button(t("replay.place"), type="primary", use_container_width=True)
        skip = b2.button(t("replay.skip"), use_container_width=True)
        if place:
            try:
                res = training.evaluate_trade(
                    entry, stop, target, df.iloc[cut : cut + HORIZON], side=side
                )
            except ValueError:
                bad_stop = (entry - stop) * d <= 0
                st.error(t("demo.err.stop") if bad_stop else t("demo.err.target"))
                return
            res.update(
                {
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "code": rp["code"],
                    "side": side,
                    "reason": reason,
                    "date": str(df.index[cut - 1].date()),
                }
            )
            progress.replays.append(res)
            training.save_progress(progress)
            rp["result"] = res
            st.rerun()
        if skip:
            fut = df.iloc[cut : cut + HORIZON]
            rp["result"] = {"skipped": True, "move_pct": (fut.close.iloc[-1] / entry - 1) * 100}
            st.rerun()
    else:
        res = rp["result"]
        trade = None if res.get("skipped") else res
        st.plotly_chart(_chart(df, cut, True, trade), use_container_width=True)
        reveal = f"**{inst.name}**, {df.index[cut - 1].date()}"
        if res.get("skipped"):
            st.info(t("replay.skipped", h=HORIZON, move=f"{res['move_pct']:+.2f}%", reveal=reveal))
        else:
            msg = {
                "target": t("replay.target_hit"),
                "stop": t("replay.stopped"),
                "time": t("replay.time", h=HORIZON),
            }[res["outcome"]]
            text = t(
                "replay.result",
                msg=msg,
                bars=res["bars_held"],
                price=ins.fmt_price(inst, res["exit_price"]),
                r=f"{res['r_multiple']:+.2f}",
                reveal=reveal,
            )
            (st.success if res["r_multiple"] > 0 else st.error)(text)
            if res["outcome"] == "stop" and abs(res["entry"] - res["stop"]) < atr:
                st.caption(t("replay.tip_tight"))
        if st.button(t("replay.next"), type="primary"):
            _new_round()
            st.rerun()

    left = training.REPLAYS_FOR_LEVEL_3 - len(progress.replays)
    if level == 2 and left > 0:
        st.caption(t("replay.more", n=left))
