import pandas as pd
import streamlit as st
from core import sizing


def render():
    st.title("🧮 Position Sizer")
    st.caption("Wraps skills/position-sizer — the same calculation the Claude skill uses.")
    pre = st.session_state.get("sizer_prefill", {})
    if pre:
        st.success(
            f"Prefilled from Price Chart: {pre['symbol']} entry {pre['entry']}, ATR {pre['atr']}"
        )

    method = st.radio(
        "Method",
        ["Stop-loss (fixed %)", "ATR-based", "Kelly criterion"],
        index=1 if pre else 0,
        horizontal=True,
    )

    with st.form("sizer"):
        c1, c2, c3 = st.columns(3)
        account = c1.number_input("Account size ($)", min_value=1.0, value=100_000.0, step=1000.0)
        entry = stop = risk_pct = atr = win_rate = avg_win = avg_loss = None
        atr_mult = 2.0
        kelly_with_entry = False

        if method == "Stop-loss (fixed %)":
            entry = c2.number_input(
                "Entry price", min_value=0.01, value=float(pre.get("entry", 155.0))
            )
            stop = c3.number_input(
                "Stop price", min_value=0.01, value=round(float(pre.get("entry", 155.0)) * 0.95, 2)
            )
            risk_pct = c1.number_input("Risk per trade (%)", 0.05, 10.0, 1.0, 0.05)
        elif method == "ATR-based":
            entry = c2.number_input(
                "Entry price", min_value=0.01, value=float(pre.get("entry", 155.0))
            )
            atr = c3.number_input("ATR", min_value=0.01, value=float(pre.get("atr", 3.2)))
            atr_mult = c1.number_input("ATR multiplier", 0.5, 10.0, 2.0, 0.25)
            risk_pct = c2.number_input("Risk per trade (%)", 0.05, 10.0, 1.0, 0.05)
        else:
            win_rate = c2.number_input("Win rate (0–1)", 0.01, 0.99, 0.55, 0.01)
            avg_win = c3.number_input("Average win (R or $)", 0.01, value=2.5)
            avg_loss = c1.number_input("Average loss (R or $)", 0.01, value=1.0)
            kelly_with_entry = c2.checkbox("Convert to shares (needs entry & stop)")
            if kelly_with_entry:
                entry = c3.number_input(
                    "Entry price", min_value=0.01, value=float(pre.get("entry", 155.0))
                )
                stop = c1.number_input(
                    "Stop price",
                    min_value=0.01,
                    value=round(float(pre.get("entry", 155.0)) * 0.95, 2),
                )

        with st.expander("Portfolio constraints (optional)"):
            d1, d2, d3, d4 = st.columns(4)
            max_pos = d1.number_input("Max position (% of account)", 0.0, 100.0, 0.0)
            max_sector = d2.number_input("Max sector (%)", 0.0, 100.0, 0.0)
            sector = d3.text_input("Sector", "")
            cur_sector = d4.number_input("Current sector exposure (%)", 0.0, 100.0, 0.0)
            fractional = st.checkbox("Allow fractional shares")

        submitted = st.form_submit_button("Calculate", type="primary")

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
        st.error(f"Invalid input: {exc}")
        return

    if result["mode"] == "budget":
        k = result["calculations"]["kelly"]
        a, b = st.columns(2)
        a.metric(
            "Risk budget (half Kelly)",
            f"${result['recommended_risk_budget']:,.2f}",
            f"{result['recommended_risk_budget_pct']}% of account",
            delta_color="off",
        )
        b.metric("Full Kelly", f"{k.get('full_kelly_pct', 0)}%")
        st.caption(result.get("note", ""))
    else:
        a, b, c, d = st.columns(4)
        a.metric("Shares", f"{result['final_recommended_shares']:,}")
        b.metric(
            "Position value",
            f"${result['final_position_value']:,.2f}",
            f"{result['final_position_value'] / account * 100:.1f}% of account",
            delta_color="off",
        )
        if result.get("final_risk_dollars") is not None:
            c.metric("Risk ($)", f"${result['final_risk_dollars']:,.2f}")
            d.metric("Risk (% of account)", f"{result['final_risk_pct']}%")
        stop_used = result["parameters"].get("stop_price")
        if stop_used:
            st.write(f"**Stop:** {stop_used}")
        if result.get("binding_constraint"):
            st.warning(f"Limited by constraint: **{result['binding_constraint']}**")
        if result.get("constraints_applied"):
            st.dataframe(pd.DataFrame(result["constraints_applied"]), hide_index=True)
        if result.get("risk_note"):
            st.info(result["risk_note"])

    md = sizing.markdown_report(result)
    with st.expander("Full report"):
        st.markdown(md)
    st.download_button("Download report (.md)", md, file_name="position_sizer_report.md")
