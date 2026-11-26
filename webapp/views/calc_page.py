import pandas as pd
import streamlit as st
from core import demo_account as da
from core import instruments as ins
from core import prices

from views.common import bars, instrument_picker, price_input
from views.lang import t


def render():
    st.title("🧮 " + t("nav.calc"))
    st.caption(t("calc.caption"))
    c1, c2 = st.columns(2)
    code = instrument_picker("calc_code", c1)
    inst = ins.get(code)
    acct_type = c2.radio(
        t("calc.account_type"),
        list(da.ACCOUNT_TYPES),
        horizontal=True,
        format_func=lambda k: t(f"demo.short.{k}"),
    )
    sc = da.ACCOUNT_TYPES[acct_type][4]

    pre = st.session_state.get("calc_prefill", {})
    if pre.get("code") == code:
        entry0, atr0 = pre["entry"], pre["atr"]
    else:
        try:
            df, _ = bars(code)
            entry0, atr0 = float(df.close.iloc[-1]), float(df.atr_14.iloc[-1])
        except prices.PriceDataError:
            st.warning(t("common.price_error"))
            entry0, atr0 = 1.0, 0.01

    c1, c2, c3, c4 = st.columns(4)
    per_usd = da.ACCOUNT_TYPES[acct_type][2]
    unit = "USC" if per_usd != 1 else "USD"
    balance = (
        c1.number_input(
            f"{t('calc.balance')} ({unit})",
            min_value=1.0,
            value=1_000.0 * per_usd,
            step=100.0 * per_usd,
            key=f"calc_bal_{acct_type}",
        )
        / per_usd
    )
    risk_pct = c2.number_input(t("calc.risk"), 0.1, 10.0, 1.0, 0.1)
    entry = price_input(c3, t("calc.entry"), inst, entry0, f"calc_entry_{code}")
    stop = price_input(c4, t("calc.stop"), inst, entry0 - atr0, f"calc_stop_{code}")
    if stop == entry:
        st.error(t("demo.err.stop"))
        return

    lev = inst.leverage
    stop_pips = ins.pips(inst, entry, stop)
    pip_val = ins.pip_value_usd(inst, 0.01, entry, sc)
    exact = (balance * risk_pct / 100) / ins.risk_usd(inst, 1.0, entry, stop, sc)
    lot = ins.suggest_lot(inst, balance, balance, entry, stop, risk_pct, sc)
    acct = {"account_type": acct_type}
    money = lambda usd: da.fmt_money(acct, usd)  # noqa: E731

    m = st.columns(3)
    m[0].metric(t("calc.stop_pips"), f"{stop_pips:,.1f} pips")
    m[1].metric(t("calc.pip_value"), money(pip_val))
    m[2].metric(t("calc.exact"), f"{exact:.3f}")
    m = st.columns(3)
    if lot is None:
        st.error(t("calc.none"))
    else:
        m[0].metric(t("calc.fixed"), da.fmt_lots(lot))
        m[1].metric(t("calc.risk_at"), money(ins.risk_usd(inst, lot, entry, stop, sc)))
        m[2].metric(t("calc.margin", lev=lev), money(ins.margin_usd(inst, lot, entry, sc)))

    st.subheader(t("calc.table"))
    rows = []
    for size in ins.LOT_SIZES:
        risk = ins.risk_usd(inst, size, entry, stop, sc)
        margin = ins.margin_usd(inst, size, entry, sc)
        ok = risk <= balance * risk_pct / 100 + 1e-9 and margin <= balance
        rows.append(
            {
                t("common.lots"): da.fmt_lots(size),
                t("calc.col_risk"): money(risk),
                t("calc.col_risk_pct"): f"{risk / balance * 100:.2f}%",
                t("calc.col_margin"): money(margin),
                t("calc.col_ok"): "✅" if ok else "❌",
            }
        )
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
