import math
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import demo_account as da
from core import indicators, prices, training

from views.lang import t
from views.state import level_info


@st.cache_data(ttl=600, show_spinner=False)
def _bars(symbol):
    df, _ = prices.fetch_daily(symbol)
    return indicators.add_indicators(df)


def _setup():
    st.write(t("demo.setup"))
    acct_type = st.radio(
        t("demo.type"),
        list(da.ACCOUNT_TYPES),
        format_func=lambda k: t(f"demo.type.{k}"),
        horizontal=True,
    )
    if acct_type == "cent":
        st.caption(t("demo.cent_help"))
    choices = da.ACCOUNT_TYPES[acct_type][3]
    unit = "USC" if acct_type == "cent" else "USD"
    bal = st.select_slider(
        t("demo.balance"),
        choices,
        value=choices[len(choices) // 2],
        format_func=lambda v: f"{v:,} {unit}" if unit == "USC" else f"${v:,}",
    )
    if st.button(t("demo.create"), type="primary"):
        da.save(da.new_account(bal, acct_type))
        st.rerun()


def render():
    level, info, _, acct = level_info()
    st.title("💼 " + t("nav.demo"))
    st.caption(t("demo.caption", n=level, name=info["name"], pct=info["max_risk_pct"]))
    if acct is None:
        _setup()
        return
    money = lambda usd: da.fmt_money(acct, usd)  # noqa: E731

    last_prices, bars = {}, {}
    for sym in {tr["symbol"] for tr in acct["open"]}:
        try:
            bars[sym] = _bars(sym)
            last_prices[sym] = float(bars[sym].close.iloc[-1])
        except prices.PriceDataError:
            pass
    exits = da.check_exits(acct, bars)
    if exits:
        da.save(acct)
        for e in exits:
            st.toast(
                t(
                    "demo.toast",
                    sym=e["symbol"],
                    reason=t(f"demo.reason.{e['exit_reason']}"),
                    price=f"{e['exit_price']:.2f}",
                    r=f"{e['r_multiple']:+.2f}",
                )
            )

    eq = da.equity(acct, last_prices)
    stats = training.trade_stats(acct["closed"])
    has = stats["trades"] > 0
    st.markdown(
        t(
            "demo.acct",
            type=t(f"demo.type.{acct['account_type']}").split(":")[0],
            start=money(acct["starting_balance"]),
        )
    )
    change = (eq / acct["starting_balance"] - 1) * 100
    m = st.columns(5)
    m[0].metric(t("demo.m_equity"), money(eq), f"{change:+.2f}%" if abs(change) >= 0.005 else None)
    m[1].metric(t("demo.m_cash"), money(acct["cash"]))
    m[2].metric(t("demo.m_closed"), stats["trades"])
    m[3].metric(t("common.win_rate"), f"{stats['win_rate']:.0%}" if has else "—")
    m[4].metric(t("common.expectancy"), f"{stats['expectancy_r']:+.2f}R" if has else "—")

    tab_new, tab_open, tab_journal = st.tabs(
        [
            t("demo.tab_new"),
            t("demo.tab_open", n=len(acct["open"])),
            t("demo.tab_journal", n=len(acct["closed"])),
        ]
    )
    with tab_new:
        _new_trade(acct, level, info, eq, money)
    with tab_open:
        _open_positions(acct, last_prices, money)
    with tab_journal:
        _journal(acct, money)

    with st.expander(t("demo.reset_title")):
        st.warning(t("demo.reset_warn"))
        if st.button(t("demo.reset_btn")):
            da.ACCOUNT_FILE.unlink(missing_ok=True)
            st.rerun()


def _new_trade(acct, level, info, eq, money):
    c1, c2 = st.columns([3, 1])
    sym_in = c1.text_input(
        t("common.ticker"),
        value=st.session_state.get("demo_symbol", ""),
        placeholder=t("demo.placeholder"),
    )
    if c2.button(t("demo.quote"), use_container_width=True) and sym_in:
        st.session_state["demo_symbol"] = sym_in
    sym = st.session_state.get("demo_symbol")
    if not sym:
        return
    try:
        sym = prices.clean_symbol(sym)
        df = _bars(sym)
    except ValueError as exc:
        st.error(str(exc))
        return
    except prices.PriceDataError:
        st.error(t("common.price_error"))
        return

    last = df.iloc[-1]
    entry = round(float(last.close), 2)
    atr = float(last.atr_14)
    trend_ok = (not math.isnan(last.sma_200)) and last.close > last.sma_50 > last.sma_200
    st.markdown(
        t(
            "demo.quote_line",
            sym=sym,
            close=entry,
            date=df.index[-1].date(),
            atr=f"{atr:.2f}",
            rsi=f"{last.rsi_14:.0f}",
            trend=t("demo.trend_up") if trend_ok else t("demo.trend_no"),
        )
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

    c1, c2, c3 = st.columns(3)
    stop = c1.number_input(
        t("common.stop"), value=round(entry - 2 * atr, 2), step=0.01, key=f"stop_{sym}"
    )
    target = c2.number_input(
        t("common.target"), value=round(entry + 4 * atr, 2), step=0.01, key=f"target_{sym}"
    )
    default = da.max_shares(acct["cash"], eq, entry, stop, info["max_risk_pct"])
    shares = c3.number_input(
        t("demo.shares"),
        min_value=0.0,
        value=float(default),
        step=0.01,
        format="%.4f",
        key=f"shares_{sym}_{stop}",
        help=t("demo.shares_help", pct=info["max_risk_pct"]),
    )
    if stop < entry and shares > 0:
        risk = (entry - stop) * shares
        st.caption(
            t(
                "demo.risk_preview",
                cost=money(entry * shares),
                risk=money(risk),
                pct=f"{risk / eq * 100:.2f}",
            )
        )

    with st.form("trade_form"):
        reason = st.text_input(t("demo.reason"))
        st.markdown(t("demo.checklist"))
        k1 = st.checkbox(t("demo.chk1"))
        k2 = st.checkbox(t("demo.chk2"))
        k3 = st.checkbox(t("demo.chk3")) if level >= 3 else True
        if st.form_submit_button(t("demo.buy"), type="primary"):
            if not reason.strip():
                st.error(t("demo.err_reason"))
            elif not (k1 and k2 and k3):
                st.error(t("demo.err_check"))
            else:
                try:
                    tr = da.open_trade(
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
                except da.RuleViolation as exc:
                    params = dict(exc.params)
                    for k in ("need", "have"):
                        if k in params:
                            params[k] = money(params[k])
                    st.error(t(f"demo.err.{exc.code}", **params))
                else:
                    da.save(acct)
                    st.success(
                        t(
                            "demo.bought",
                            shares=da.fmt_shares(tr["shares"]),
                            sym=sym,
                            price=entry,
                            risk=money(tr["risk_dollars"]),
                            pct=tr["risk_pct"],
                        )
                    )
                    st.rerun()


def _open_positions(acct, last_prices, money):
    if not acct["open"]:
        st.caption(t("demo.no_open"))
        return
    st.caption(t("demo.open_caption"))
    for tr in list(acct["open"]):
        px = last_prices.get(tr["symbol"], tr["entry"])
        r = (px - tr["entry"]) / (tr["entry"] - tr["stop"]) + 0
        with st.container(border=True):
            c = st.columns([2, 2, 2, 2, 1])
            c[0].markdown(
                f"**{tr['symbol']}** × {da.fmt_shares(tr['shares'])}  \n{tr['entry_date']}"
            )
            c[1].markdown(t("demo.pos_entry", entry=tr["entry"], now=f"{px:.2f}"))
            c[2].markdown(t("demo.pos_levels", stop=tr["stop"], target=tr["target"]))
            c[3].markdown(
                t("demo.pos_pnl", pnl=money((px - tr["entry"]) * tr["shares"]), r=f"{r:+.2f}")
            )
            if c[4].button(t("demo.close"), key=f"close_{tr['id']}"):
                da.close_trade(acct, tr["id"], px, date.today().isoformat(), "manual")
                da.save(acct)
                st.rerun()
            if tr.get("note"):
                st.caption(t("demo.note", note=tr["note"]))


def _journal(acct, money):
    if not acct["closed"]:
        st.caption(t("demo.no_closed"))
        return
    df = pd.DataFrame(acct["closed"])
    per_usd = da.ACCOUNT_TYPES[acct["account_type"]][2]
    curve = (acct["starting_balance"] + df["pnl"].cumsum()) * per_usd
    fig = go.Figure(go.Scatter(x=list(range(1, len(df) + 1)), y=curve, mode="lines+markers"))
    unit = "USC" if per_usd != 1 else "$"
    fig.update_layout(
        height=260,
        margin=dict(t=10, b=10),
        xaxis_title=t("demo.axis_trade"),
        yaxis_title=f"{t('demo.axis_account')} ({unit})",
    )
    st.plotly_chart(fig, use_container_width=True)

    view = df.copy()
    view["pnl"] = view["pnl"].map(money)
    view["shares"] = view["shares"].map(da.fmt_shares)
    view["exit_reason"] = view["exit_reason"].map(lambda k: t(f"demo.reason.{k}"))
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
    view = view[cols].iloc[::-1].rename(columns={c: t(f"col.{c}") for c in cols})
    st.dataframe(view, hide_index=True, use_container_width=True)
    worst = df.nsmallest(1, "r_multiple").iloc[0]
    if worst["r_multiple"] < -1.05:
        st.warning(t("demo.worst", sym=worst["symbol"], r=f"{worst['r_multiple']:.2f}"))
