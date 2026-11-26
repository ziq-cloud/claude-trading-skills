import math
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import demo_account, indicators, prices, training

from views.state import level_info


def _money(v: float) -> str:
    return f"-${abs(v):,.2f}" if v < -0.005 else f"${abs(v):,.2f}"


@st.cache_data(ttl=600, show_spinner=False)
def _bars(symbol):
    df, _ = prices.fetch_daily(symbol)
    return indicators.add_indicators(df)


def _setup():
    st.write("Start a paper-trading account with virtual money. Prices are real daily closes.")
    with st.form("new_acct"):
        bal = st.select_slider(
            "Starting balance (virtual $)",
            [1_000, 5_000, 10_000, 25_000, 50_000, 100_000],
            value=10_000,
        )
        if st.form_submit_button("Create demo account", type="primary"):
            demo_account.save(demo_account.new_account(bal))
            st.rerun()


def render():
    level, info, _, acct = level_info()
    st.title("💼 Demo Account")
    st.caption(
        f"Level {level} · {info['name']} — max risk per trade **{info['max_risk_pct']}%**. "
        "Long trades only. Every trade needs a stop-loss and a reason."
    )
    if acct is None:
        _setup()
        return

    # ---- refresh prices, auto-exit stops/targets
    last_prices, bars = {}, {}
    for sym in {t["symbol"] for t in acct["open"]}:
        try:
            bars[sym] = _bars(sym)
            last_prices[sym] = float(bars[sym].close.iloc[-1])
        except prices.PriceDataError:
            pass
    exits = demo_account.check_exits(acct, bars)
    if exits:
        demo_account.save(acct)
        for e in exits:
            st.toast(
                f"{e['symbol']} {e['exit_reason']} hit at {e['exit_price']:.2f} "
                f"({e['r_multiple']:+.2f}R)"
            )

    eq = demo_account.equity(acct, last_prices)
    stats = training.trade_stats(acct["closed"])
    m = st.columns(5)
    change = (eq / acct["starting_balance"] - 1) * 100
    m[0].metric("Equity", _money(eq), f"{change:+.2f}%" if abs(change) >= 0.005 else None)
    m[1].metric("Cash", f"${acct['cash']:,.2f}")
    m[2].metric("Closed trades", stats["trades"])
    m[3].metric("Win rate", f"{stats['win_rate']:.0%}" if stats["trades"] else "—")
    m[4].metric("Expectancy", f"{stats['expectancy_r']:+.2f}R" if stats["trades"] else "—")

    tab_new, tab_open, tab_journal = st.tabs(
        ["New trade", f"Open ({len(acct['open'])})", f"Journal ({len(acct['closed'])})"]
    )
    with tab_new:
        _new_trade(acct, level, info, eq)
    with tab_open:
        _open_positions(acct, last_prices)
    with tab_journal:
        _journal(acct)

    with st.expander("Reset account"):
        st.warning("This deletes all demo trades and history.")
        if st.button("Reset demo account"):
            demo_account.ACCOUNT_FILE.unlink(missing_ok=True)
            st.rerun()


def _new_trade(acct, level, info, eq):
    c1, c2 = st.columns([3, 1])
    sym_in = c1.text_input(
        "Ticker", value=st.session_state.get("demo_symbol", ""), placeholder="e.g. AAPL"
    )
    if c2.button("Get quote", use_container_width=True) and sym_in:
        st.session_state["demo_symbol"] = sym_in
    sym = st.session_state.get("demo_symbol")
    if not sym:
        return
    try:
        sym = prices.clean_symbol(sym)
        df = _bars(sym)
    except (ValueError, prices.PriceDataError) as exc:
        st.error(str(exc))
        return

    last = df.iloc[-1]
    entry = round(float(last.close), 2)
    atr = float(last.atr_14)
    trend_ok = last.close > last.sma_50 > last.sma_200 if not math.isnan(last.sma_200) else False
    st.markdown(
        f"**{sym}** last close **{entry}** ({df.index[-1].date()}) · ATR {atr:.2f} · "
        f"RSI {last.rsi_14:.0f} · trend: {'🟢 up (above 50 & 200 SMA)' if trend_ok else '🟠 not a clean uptrend'}"
    )

    view = df.tail(120)
    fig = go.Figure(
        go.Candlestick(
            x=view.index, open=view.open, high=view.high, low=view.low, close=view.close, name=sym
        )
    )
    for w, c in ((50, "#2f7ed8"), (200, "#c0392b")):
        fig.add_trace(
            go.Scatter(
                x=view.index, y=view[f"sma_{w}"], name=f"SMA {w}", line=dict(width=1.3, color=c)
            )
        )
    fig.update_layout(
        height=320, xaxis_rangeslider_visible=False, margin=dict(t=10, b=10), showlegend=False
    )
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    st.plotly_chart(fig, use_container_width=True)

    default_stop = round(entry - 2 * atr, 2)
    with st.form("trade_form"):
        c1, c2, c3 = st.columns(3)
        stop = c1.number_input("Stop-loss", value=default_stop, step=0.01)
        target = c2.number_input("Target", value=round(entry + 4 * atr, 2), step=0.01)
        risk_cap = eq * info["max_risk_pct"] / 100
        max_shares = int(risk_cap / (entry - stop)) if stop < entry else 0
        max_shares = min(max_shares, int(acct["cash"] // entry))
        shares = c3.number_input(
            "Shares",
            min_value=0,
            value=max_shares,
            step=1,
            help=f"Default = most shares allowed by your {info['max_risk_pct']}% "
            "risk limit and your cash.",
        )
        reason = st.text_input("Why are you taking this trade? (required)")
        st.markdown("**Pre-trade checklist**")
        k1 = st.checkbox("I know where I'm wrong (stop) before entering")
        k2 = st.checkbox("The reward is at least 2× the risk")
        k3 = st.checkbox("I checked the overall market (Market Breadth)") if level >= 3 else True
        if st.form_submit_button("Buy at last close", type="primary"):
            if not reason.strip():
                st.error("Write a reason first — it goes into your journal.")
            elif not (k1 and k2 and k3):
                st.error("Tick every checklist item first.")
            else:
                try:
                    t = demo_account.open_trade(
                        acct,
                        sym,
                        entry,
                        stop,
                        target,
                        shares,
                        str(df.index[-1].date()),
                        info["max_risk_pct"],
                        note=reason.strip(),
                    )
                except demo_account.RuleViolation as exc:
                    st.error(str(exc))
                else:
                    demo_account.save(acct)
                    st.success(
                        f"Bought {shares} {sym} at {entry}. Risk ${t['risk_dollars']:,.2f} "
                        f"({t['risk_pct']}%)."
                    )
                    st.rerun()


def _open_positions(acct, last_prices):
    if not acct["open"]:
        st.caption("No open positions.")
        return
    st.caption("Stops and targets are checked against each new daily bar when this page loads.")
    for t in list(acct["open"]):
        px = last_prices.get(t["symbol"], t["entry"])
        r = (px - t["entry"]) / (t["entry"] - t["stop"])
        with st.container(border=True):
            c = st.columns([2, 2, 2, 2, 1])
            c[0].markdown(f"**{t['symbol']}** × {t['shares']}  \n{t['entry_date']}")
            c[1].markdown(f"Entry {t['entry']}  \nNow **{px:.2f}**")
            c[2].markdown(f"Stop {t['stop']}  \nTarget {t['target']}")
            c[3].markdown(f"P&L **{_money((px - t['entry']) * t['shares'])}**  \n{r + 0:+.2f}R")
            if c[4].button("Close", key=f"close_{t['id']}"):
                demo_account.close_trade(acct, t["id"], px, date.today().isoformat(), "manual")
                demo_account.save(acct)
                st.rerun()
            if t.get("note"):
                st.caption(f"Reason: {t['note']}")


def _journal(acct):
    if not acct["closed"]:
        st.caption("Closed trades appear here.")
        return
    df = pd.DataFrame(acct["closed"])
    df["cum_pnl"] = df["pnl"].cumsum()
    fig = go.Figure(
        go.Scatter(
            x=list(range(1, len(df) + 1)),
            y=acct["starting_balance"] + df["cum_pnl"],
            mode="lines+markers",
        )
    )
    fig.update_layout(
        height=260, margin=dict(t=10, b=10), xaxis_title="trade #", yaxis_title="account ($)"
    )
    st.plotly_chart(fig, use_container_width=True)
    cols = [
        "symbol",
        "entry_date",
        "exit_date",
        "entry",
        "exit_price",
        "stop",
        "shares",
        "exit_reason",
        "pnl",
        "r_multiple",
        "note",
    ]
    st.dataframe(df[cols].iloc[::-1], hide_index=True, use_container_width=True)
    worst = df.nsmallest(1, "r_multiple").iloc[0]
    if worst["r_multiple"] < -1.05:
        st.warning(
            f"Your worst trade ({worst['symbol']}) lost {worst['r_multiple']:.2f}R — more "
            "than your planned risk. That usually means a gap or a moved stop."
        )
