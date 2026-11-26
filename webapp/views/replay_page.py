import random

import plotly.graph_objects as go
import streamlit as st
from core import indicators, prices, training

from views.state import level_info

POOL = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "META",
    "GOOGL",
    "TSLA",
    "AMD",
    "NFLX",
    "JPM",
    "XOM",
    "COST",
    "AVGO",
    "LLY",
    "CRM",
    "SPY",
    "QQQ",
    "IWM",
    "KO",
    "DIS",
]
VISIBLE = 120
HORIZON = 20


@st.cache_data(ttl=3600, show_spinner=False)
def _history(symbol):
    df, _ = prices.fetch_daily(symbol)
    return indicators.add_indicators(df)


def _new_round():
    for _ in range(5):
        sym = random.choice(POOL)
        try:
            df = _history(sym)
        except prices.PriceDataError:
            continue
        if len(df) >= 220 + HORIZON:
            cut = random.randint(220, len(df) - HORIZON)
            st.session_state.replay = {"symbol": sym, "cut": cut, "result": None}
            return
    st.session_state.replay = None


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
            annotation_text="hidden future",
            annotation_position="top left",
        )
    if trade:
        for y, name, c in (
            (trade["stop"], "stop", "#c0392b"),
            (trade["target"], "target", "#27ae60"),
            (trade["entry"], "entry", "#555"),
        ):
            fig.add_hline(y=y, line_dash="dash", line_color=c, annotation_text=name)
    fig.update_layout(
        height=520,
        xaxis_rangeslider_visible=False,
        margin=dict(t=10, b=10),
        legend=dict(orientation="h", y=1.02),
        xaxis_title="bars (dates hidden)",
    )
    return fig


def render():
    level, info, progress, _ = level_info()
    st.title("⏪ Chart Replay")
    st.write(
        f"A random stock is shown up to a hidden point in the past. Decide: buy with a stop "
        f"and target, or skip. Then the next {HORIZON} days are revealed. Ticker and dates "
        "are hidden so you judge the chart, not the name."
    )

    if st.session_state.get("replay") is None:
        _new_round()
    rp = st.session_state.replay
    if rp is None:
        st.error("Could not load price data. Set TWELVEDATA_API_KEY or install yfinance.")
        return
    df = _history(rp["symbol"])
    cut = rp["cut"]
    last = df.iloc[cut - 1]
    entry = round(float(last.close), 2)
    atr = float(last.atr_14)

    stats = training.trade_stats(progress.replays)
    m = st.columns(4)
    m[0].metric("Replay trades", stats["trades"])
    m[1].metric("Win rate", f"{stats['win_rate']:.0%}" if stats["trades"] else "—")
    m[2].metric("Expectancy", f"{stats['expectancy_r']:+.2f}R" if stats["trades"] else "—")
    m[3].metric("Total", f"{stats['total_r']:+.1f}R" if stats["trades"] else "—")

    if rp["result"] is None:
        st.plotly_chart(_chart(df, cut, False), use_container_width=True)
        st.caption(
            f"Last close **{entry}** · ATR(14) **{atr:.2f}** · RSI(14) **{last.rsi_14:.0f}**"
        )
        with st.form("replay_form"):
            c1, c2, c3 = st.columns(3)
            stop = c1.number_input("Stop-loss", value=round(entry - 2 * atr, 2), step=0.01)
            target = c2.number_input("Target", value=round(entry + 4 * atr, 2), step=0.01)
            reason = c3.text_input("Why this trade? (one line)")
            if stop < entry:
                st.caption(
                    f"Risk {entry - stop:.2f} · reward {target - entry:.2f} · "
                    f"R:R = {(target - entry) / (entry - stop):.1f}"
                )
            b1, b2 = st.columns(2)
            buy = b1.form_submit_button(
                "🟢 Buy at last close", type="primary", use_container_width=True
            )
            skip = b2.form_submit_button("⏭ Skip — no trade", use_container_width=True)
        if buy:
            try:
                res = training.evaluate_trade(entry, stop, target, df.iloc[cut : cut + HORIZON])
            except ValueError as exc:
                st.error(str(exc))
                return
            res.update(
                {
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "symbol": rp["symbol"],
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
        reveal = f"**{rp['symbol']}**, {df.index[cut - 1].date()}"
        if res.get("skipped"):
            st.info(
                f"You skipped. Over the next {HORIZON} days price moved "
                f"{res['move_pct']:+.1f}%. ({reveal})"
            )
        else:
            msg = {
                "target": "🎯 Target hit",
                "stop": "🛑 Stopped out",
                "time": f"⏱ Neither hit in {HORIZON} days — exited at close",
            }[res["outcome"]]
            text = (
                f"{msg} after {res['bars_held']} bars at {res['exit_price']:.2f} → "
                f"**{res['r_multiple']:+.2f}R**. ({reveal})"
            )
            (st.success if res["r_multiple"] > 0 else st.error)(text)
            if res["outcome"] == "stop" and abs(res["entry"] - res["stop"]) < atr:
                st.caption(
                    "Tip: your stop was tighter than 1 ATR, so normal daily noise can hit it."
                )
        if st.button("Next chart ▶", type="primary"):
            _new_round()
            st.rerun()

    if level < 3:
        left = training.REPLAYS_FOR_LEVEL_3 - len(progress.replays)
        if level == 2 and left > 0:
            st.caption(f"{left} more replay trades to reach Level 3.")
