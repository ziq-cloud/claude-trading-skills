import math
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import demo_account as da
from core import instruments as ins
from core import prices, training

from views.common import bars, instrument_picker, price_input
from views.lang import t
from views.state import level_info


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
    cent = acct_type == "cent"
    bal = st.select_slider(
        t("demo.balance"),
        choices,
        value=choices[len(choices) // 2],
        format_func=lambda v: f"{v:,} USC" if cent else f"${v:,}",
    )
    if st.button(t("demo.create"), type="primary"):
        da.save(da.new_account(bal, acct_type))
        st.rerun()


def render():
    level, info, _, acct = level_info()
    st.title("💼 " + t("nav.demo"))
    st.caption(
        t(
            "demo.caption",
            n=level,
            name=info["name"],
            pct=info["max_risk_pct"],
            lev=da.DEFAULT_LEVERAGE,
        )
    )
    if acct is None:
        _setup()
        return
    money = lambda usd: da.fmt_money(acct, usd)  # noqa: E731

    # ---- latest closes, auto stop/target exits, stop-out
    last_prices, all_bars = {}, {}
    for code in {tr["code"] for tr in acct["open"]}:
        try:
            all_bars[code], _ = bars(code)
            last_prices[code] = float(all_bars[code].close.iloc[-1])
        except prices.PriceDataError:
            pass
    events = da.check_exits(acct, all_bars)
    events += da.stop_out(acct, last_prices, date.today().isoformat())
    if events:
        da.save(acct)
        for e in events:
            st.toast(
                t(
                    "demo.toast",
                    sym=ins.get(e["code"]).name,
                    reason=t(f"demo.reason.{e['exit_reason']}"),
                    price=ins.fmt_price(ins.get(e["code"]), e["exit_price"]),
                    r=f"{e['r_multiple']:+.2f}",
                )
            )

    eq = da.equity(acct, last_prices)
    level_pct = da.margin_level(acct, last_prices)
    stats = training.trade_stats(acct["closed"])
    has = stats["trades"] > 0
    st.markdown(
        t(
            "demo.acct",
            type=t(f"demo.short.{acct['account_type']}"),
            start=money(acct["starting_balance"]),
        )
    )
    change = (eq / acct["starting_balance"] - 1) * 100
    m = st.columns(2)
    m[0].metric(t("demo.m_balance"), money(acct["balance"]))
    m[1].metric(t("demo.m_equity"), money(eq), f"{change:+.2f}%" if abs(change) >= 0.005 else None)
    m = st.columns(3)
    m[0].metric(t("demo.m_margin"), money(da.used_margin(acct)))
    m[1].metric(t("demo.m_free"), money(da.free_margin(acct, last_prices)))
    m[2].metric(t("demo.m_level"), "—" if level_pct is None else f"{level_pct:,.0f}%")
    m = st.columns(3)
    m[0].metric(t("demo.m_closed"), stats["trades"])
    m[1].metric(t("common.win_rate"), f"{stats['win_rate']:.0%}" if has else "—")
    m[2].metric(t("common.expectancy"), f"{stats['expectancy_r']:+.2f}R" if has else "—")

    tab_new, tab_open, tab_journal = st.tabs(
        [
            t("demo.tab_new"),
            t("demo.tab_open", n=len(acct["open"])),
            t("demo.tab_journal", n=len(acct["closed"])),
        ]
    )
    with tab_new:
        _new_trade(acct, level, info, last_prices, money)
    with tab_open:
        _open_positions(acct, last_prices, money)
    with tab_journal:
        _journal(acct, money)

    with st.expander(t("demo.reset_title")):
        st.warning(t("demo.reset_warn"))
        if st.button(t("demo.reset_btn")):
            da.ACCOUNT_FILE.unlink(missing_ok=True)
            st.rerun()


def _new_trade(acct, level, info, last_prices, money):
    code = instrument_picker("demo_code")
    inst = ins.get(code)
    try:
        df, _ = bars(code)
    except prices.PriceDataError:
        st.error(t("common.price_error"))
        return

    last = df.iloc[-1]
    entry = round(float(last.close), inst.digits)
    atr = float(last.atr_14)
    if math.isnan(last.sma_200):
        trend = t("demo.trend_no")
    elif last.close > last.sma_50 > last.sma_200:
        trend = t("demo.trend_up")
    elif last.close < last.sma_50 < last.sma_200:
        trend = t("demo.trend_down")
    else:
        trend = t("demo.trend_no")
    st.markdown(
        t(
            "demo.quote_line",
            sym=inst.name,
            close=ins.fmt_price(inst, entry),
            date=df.index[-1].date(),
            atr=f"{ins.pips(inst, atr, 0):,.0f} pips",
            rsi=f"{last.rsi_14:.0f}",
            trend=trend,
        )
    )

    view = df.tail(120)
    fig = go.Figure(
        go.Candlestick(
            x=view.index,
            open=view.open,
            high=view.high,
            low=view.low,
            close=view.close,
            name=inst.name,
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
    if inst.kind != "crypto":
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
    st.plotly_chart(fig, use_container_width=True)

    side = st.radio(
        t("replay.side"),
        ["buy", "sell"],
        horizontal=True,
        format_func=lambda s: t(f"common.{s}"),
        key="demo_side",
    )
    d = 1 if side == "buy" else -1
    prices_now = {**last_prices, code: entry}
    eq = da.equity(acct, prices_now)
    sc = da.scale(acct)

    c1, c2, c3 = st.columns(3)
    stop = price_input(c1, t("common.stop"), inst, entry - d * atr, f"ds_{code}_{side}")
    target = price_input(c2, t("common.target"), inst, entry + d * 2 * atr, f"dt_{code}_{side}")
    suggested = (
        ins.suggest_lot(
            inst, eq, da.free_margin(acct, prices_now), entry, stop, info["max_risk_pct"], sc
        )
        if (entry - stop) * d > 0
        else None
    )
    lots = c3.selectbox(
        t("common.lots"),
        ins.LOT_SIZES,
        index=ins.LOT_SIZES.index(suggested or ins.LOT_SIZES[0]),
        format_func=da.fmt_lots,
        key=f"dl_{code}_{side}_{stop}",
        help=t("demo.lots_help", pct=info["max_risk_pct"]),
    )
    if (entry - stop) * d > 0:
        risk = ins.risk_usd(inst, lots, entry, stop, sc)
        st.caption(
            t(
                "demo.preview",
                pips=f"{ins.pips(inst, entry, stop):,.0f}",
                risk=money(risk),
                pct=f"{risk / eq * 100:.2f}",
                margin=money(ins.margin_usd(inst, lots, entry, sc)),
            )
        )
        if suggested is None:
            st.warning(t("demo.no_lot", pct=info["max_risk_pct"]))

    side_label = t(f"common.{side}")
    with st.form("trade_form"):
        reason = st.text_input(t("demo.reason"))
        st.markdown(t("demo.checklist"))
        k1 = st.checkbox(t("demo.chk1"))
        k2 = st.checkbox(t("demo.chk2"))
        k3 = st.checkbox(t("demo.chk3")) if level >= 3 else True
        label = t(
            "demo.place",
            side=side_label,
            lots=da.fmt_lots(lots),
            sym=inst.name,
            price=ins.fmt_price(inst, entry),
        )
        if st.form_submit_button(label, type="primary"):
            if not reason.strip():
                st.error(t("demo.err_reason"))
            elif not (k1 and k2 and k3):
                st.error(t("demo.err_check"))
            else:
                try:
                    tr = da.open_trade(
                        acct,
                        code,
                        side,
                        lots,
                        entry,
                        stop,
                        target,
                        str(df.index[-1].date()),
                        info["max_risk_pct"],
                        note=reason.strip(),
                        last_prices=prices_now,
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
                            "demo.opened",
                            side=side_label,
                            lots=da.fmt_lots(lots),
                            sym=inst.name,
                            price=ins.fmt_price(inst, entry),
                            risk=money(tr["risk_usd"]),
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
        inst = ins.get(tr["code"])
        px = last_prices.get(tr["code"], tr["entry"])
        d = 1 if tr["side"] == "buy" else -1
        r = (px - tr["entry"]) * d / abs(tr["entry"] - tr["stop"]) + 0.0
        f = lambda v, i=inst: "—" if v is None else ins.fmt_price(i, v)  # noqa: E731
        with st.container(border=True):
            c = st.columns([2, 2, 2, 2, 1])
            arrow = "🟢" if d == 1 else "🔴"
            c[0].markdown(
                f"{arrow} **{inst.name}**  \n{t('common.' + tr['side'])} "
                f"{da.fmt_lots(tr['lots'])} · {tr['entry_date']}"
            )
            c[1].markdown(t("demo.pos_entry", entry=f(tr["entry"]), now=f(px)))
            c[2].markdown(t("demo.pos_levels", stop=f(tr["stop"]), target=f(tr["target"])))
            c[3].markdown(t("demo.pos_pnl", pnl=money(da.trade_pnl(acct, tr, px)), r=f"{r:+.2f}"))
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
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True)

    view = df.copy()
    fmt = lambda row, col: ins.fmt_price(ins.get(row["code"]), row[col])  # noqa: E731
    for col in ("entry", "exit_price", "stop"):
        view[col] = view.apply(lambda row, c=col: fmt(row, c), axis=1)
    view["instrument"] = view["code"].map(lambda c: ins.get(c).name)
    view["side"] = view["side"].map(lambda s: t(f"common.{s}"))
    view["lots"] = view["lots"].map(da.fmt_lots)
    view["pnl"] = view["pnl"].map(money)
    view["exit_reason"] = view["exit_reason"].map(lambda k: t(f"demo.reason.{k}"))
    cols = [
        "instrument",
        "side",
        "lots",
        "entry_date",
        "exit_date",
        "entry",
        "exit_price",
        "stop",
        "exit_reason",
        "pnl",
        "r_multiple",
        "note",
    ]
    view = view[cols].iloc[::-1].rename(columns={c: t(f"col.{c}") for c in cols})
    st.dataframe(view, hide_index=True, use_container_width=True)
    worst = df.nsmallest(1, "r_multiple").iloc[0]
    if worst["r_multiple"] < -1.05:
        st.warning(t("demo.worst", sym=ins.get(worst["code"]).name, r=f"{worst['r_multiple']:.2f}"))
