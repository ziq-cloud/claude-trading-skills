import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from core import breadth
from core.paths import REPORTS_DIR

OUT_DIR = REPORTS_DIR / "webapp" / "market_breadth"


def _source_args() -> list[str]:
    """Optional CSV mirror via BREADTH_DETAIL_URL / BREADTH_SUMMARY_URL env vars."""
    args = []
    if os.environ.get("BREADTH_DETAIL_URL"):
        args += ["--detail-url", os.environ["BREADTH_DETAIL_URL"]]
    if os.environ.get("BREADTH_SUMMARY_URL"):
        args += ["--summary-url", os.environ["BREADTH_SUMMARY_URL"]]
    return args


def _gauge(score: float, zone: str):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": zone},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#222"},
                "steps": [
                    {"range": [0, 20], "color": "#e74c3c"},
                    {"range": [20, 40], "color": "#f39c12"},
                    {"range": [40, 60], "color": "#f7dc6f"},
                    {"range": [60, 80], "color": "#82e0aa"},
                    {"range": [80, 100], "color": "#27ae60"},
                ],
            },
        )
    )
    fig.update_layout(height=280, margin=dict(t=40, b=10, l=40, r=40))
    return fig


def render():
    st.title("🌡️ Market Breadth")
    st.caption("Runs skills/market-breadth-analyzer on TraderMonty's public CSV — no API key.")

    col1, col2 = st.columns([1, 3])
    run = col1.button("Run analysis", type="primary")
    analysis = None
    if run:
        with st.spinner("Fetching breadth data and scoring…"):
            try:
                analysis = breadth.run_analyzer(OUT_DIR, _source_args())
            except (breadth.BreadthError, OSError) as exc:
                st.error(f"Analyzer failed: {exc}")
                return
    elif OUT_DIR.exists():
        try:
            analysis = breadth.load_latest_report(OUT_DIR)
            col2.caption("Showing the latest saved report. Click **Run analysis** to refresh.")
        except breadth.BreadthError:
            pass

    if not analysis:
        st.info("No report yet — click **Run analysis**.")
        return

    comp = analysis.get("composite", {})
    meta = analysis.get("metadata", {})
    fresh = meta.get("data_freshness", {})
    if fresh.get("warning"):
        st.warning(fresh["warning"])

    left, right = st.columns([1, 1])
    left.plotly_chart(
        _gauge(comp.get("composite_score", 0), comp.get("zone", "")), use_container_width=True
    )
    with right:
        st.metric("Equity exposure guidance", comp.get("exposure_guidance", "—"))
        sh, wk = comp.get("strongest_health", {}), comp.get("weakest_health", {})
        st.write(f"**Strongest:** {sh.get('label', '—')} ({sh.get('score', '—')})")
        st.write(f"**Weakest:** {wk.get('label', '—')} ({wk.get('score', '—')})")
        st.caption(
            f"Latest data: {fresh.get('latest_date', '—')} · generated "
            f"{meta.get('generated_at', '—')}"
        )

    rows = breadth.component_rows(analysis)
    if rows:
        st.subheader("Components")
        st.dataframe(
            pd.DataFrame(rows),
            hide_index=True,
            use_container_width=True,
            column_config={
                "score": st.column_config.ProgressColumn(
                    "score", min_value=0, max_value=100, format="%d"
                )
            },
        )

    levels = analysis.get("key_levels") or {}
    if levels:
        st.subheader("Key levels to watch")
        st.dataframe(
            pd.DataFrame([{"level": k, **v} for k, v in levels.items()]),
            hide_index=True,
            use_container_width=True,
        )
    st.caption(f"Reports saved to {os.path.relpath(OUT_DIR)}")
