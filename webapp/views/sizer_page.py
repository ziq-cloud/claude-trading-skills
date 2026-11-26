import pandas as pd
import streamlit as st
from core import sizing

from views.lang import t

METHODS = ["stop", "atr", "kelly"]


def render():
    st.title("🧮 " + t("nav.sizer"))
    st.caption(t("sizer.caption"))
    pre = st.session_state.get("sizer_prefill", {})
    if pre:
        st.success(t("sizer.prefilled", sym=pre["symbol"], entry=pre["entry"], atr=pre["atr"]))
    method = st.radio(
        t("sizer.method"),
        METHODS,
        index=1 if pre else 0,
        horizontal=True,
        format_func=lambda m: t(f"sizer.m_{m}"),
    )
    pe = float(pre.get("entry", 155.0))

    with st.form("sizer_form"):
        c1, c2, c3 = st.columns(3)
        account = c1.number_input(t("sizer.account"), min_value=1.0, value=1_000.0, step=100.0)
        entry = stop = risk_pct = atr = win_rate = avg_win = avg_loss = None
        atr_mult = 2.0
        if method == "stop":
            entry = c2.number_input(t("sizer.entry"), min_value=0.01, value=pe)
            stop = c3.number_input(t("sizer.stop"), min_value=0.01, value=round(pe * 0.95, 2))
            risk_pct = c1.number_input(t("sizer.risk_pct"), 0.05, 10.0, 1.0, 0.05)
        elif method == "atr":
            entry = c2.number_input(t("sizer.entry"), min_value=0.01, value=pe)
            atr = c3.number_input("ATR", min_value=0.01, value=float(pre.get("atr", 3.2)))
            atr_mult = c1.number_input(t("sizer.atr_mult"), 0.5, 10.0, 2.0, 0.25)
            risk_pct = c2.number_input(t("sizer.risk_pct"), 0.05, 10.0, 1.0, 0.05)
        else:
            win_rate = c2.number_input(t("sizer.win_rate"), 0.01, 0.99, 0.55, 0.01)
            avg_win = c3.number_input(t("sizer.avg_win"), 0.01, value=2.5)
            avg_loss = c1.number_input(t("sizer.avg_loss"), 0.01, value=1.0)
            if c2.checkbox(t("sizer.kelly_convert")):
                entry = c3.number_input(t("sizer.entry"), min_value=0.01, value=pe)
                stop = c1.number_input(t("sizer.stop"), min_value=0.01, value=round(pe * 0.95, 2))

        with st.expander(t("sizer.constraints")):
            d1, d2, d3, d4 = st.columns(4)
            max_pos = d1.number_input(t("sizer.max_pos"), 0.0, 100.0, 0.0)
            max_sector = d2.number_input(t("sizer.max_sector"), 0.0, 100.0, 0.0)
            sector = d3.text_input(t("sizer.sector"), "")
            cur_sector = d4.number_input(t("sizer.cur_sector"), 0.0, 100.0, 0.0)
        fractional = st.checkbox(t("sizer.fractional"), value=True)
        submitted = st.form_submit_button(t("sizer.calculate"), type="primary")

    if not submitted:
        return
    try:
        result = sizing.size_position(
            account_size=account,
            entry=entry,
            stop=stop,
            risk_pct=risk_pct,
            atr=atr,
            atr_multiplier=atr_mult,
            win_rate=win_rate,
            avg_win=avg_win,
            avg_loss=avg_loss,
            max_position_pct=max_pos or None,
            max_sector_pct=max_sector or None,
            sector=sector or None,
            current_sector_exposure=cur_sector,
            fractional_shares=fractional,
        )
    except (ValueError, ZeroDivisionError) as exc:
        st.error(t("sizer.invalid", err=exc))
        return

    if result["mode"] == "budget":
        k = result["calculations"]["kelly"]
        a, b = st.columns(2)
        a.metric(
            t("sizer.budget"),
            f"${result['recommended_risk_budget']:,.2f}",
            t("sizer.pct_acct", pct=result["recommended_risk_budget_pct"]),
            delta_color="off",
        )
        b.metric(t("sizer.full_kelly"), f"{k.get('full_kelly_pct', 0)}%")
    else:
        a, b, c, d = st.columns(4)
        a.metric(t("demo.shares"), f"{result['final_recommended_shares']:,}")
        b.metric(
            t("sizer.pos_value"),
            f"${result['final_position_value']:,.2f}",
            t("sizer.pct_acct", pct=f"{result['final_position_value'] / account * 100:.1f}"),
            delta_color="off",
        )
        if result.get("final_risk_dollars") is not None:
            c.metric(t("sizer.risk_usd"), f"${result['final_risk_dollars']:,.2f}")
            d.metric(t("sizer.risk_acct"), f"{result['final_risk_pct']}%")
        if result["parameters"].get("stop_price"):
            st.write(t("sizer.stop_used", stop=result["parameters"]["stop_price"]))
        if result.get("binding_constraint"):
            st.warning(t("sizer.binding", name=result["binding_constraint"]))
        if result.get("constraints_applied"):
            st.dataframe(pd.DataFrame(result["constraints_applied"]), hide_index=True)

    md = sizing.markdown_report(result)
    with st.expander(t("sizer.report")):
        st.markdown(md)
    st.download_button(t("sizer.download"), md, file_name="position_sizer_report.md")
