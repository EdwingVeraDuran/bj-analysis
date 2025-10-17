from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from statistics import fmean

import altair as alt
import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from utils.config import CONFIG


st.header("📊 Simulation Results")

base_csv_path = Path(CONFIG["csv_path"])
data_root = base_csv_path.parent if base_csv_path.suffix else base_csv_path
folders = sorted([p for p in data_root.iterdir() if p.is_dir()], reverse=True)

if not folders:
    st.info("No simulations found yet.")
else:
    default_idx = 0
    if "last_output_dir" in st.session_state:
        try:
            default_idx = next(i for i, p in enumerate(folders) if str(p) == st.session_state["last_output_dir"])
        except StopIteration:
            default_idx = 0

    selected_name = st.selectbox("Select a simulation batch", options=[p.name for p in folders], index=default_idx)
    selected_folder = next(p for p in folders if p.name == selected_name)

    params_file = selected_folder / "parameters.json"
    summary_file = selected_folder / "summary.csv"

    params = {}
    metadata = {}
    if params_file.exists():
        metadata = json.loads(params_file.read_text(encoding="utf-8"))
        params = metadata.get("parameters", {})
        st.subheader("Batch parameters")
        st.caption(f"Generated at `{metadata.get('generated_at', 'unknown')}`")
        param_display = [
            ("Decks", params.get("decks")),
            ("Starting balance", params.get("starting_balance")),
            ("Base bet", params.get("base_bet")),
            ("Penetration", params.get("penetration")),
            ("Blackjack payout", params.get("blackjack_payout")),
            ("Hands per run", params.get("hands_per_run")),
            ("Runs", metadata.get("runs")),
            ("Dealer hit soft 17", "Yes" if params.get("hit_soft_17") else "No"),
            ("RNG seed", params.get("rng_seed", "None")),
        ]
        for label, value in param_display:
            label_col, value_col = st.columns([0.4, 0.6])
            with label_col:
                st.markdown(f"**{label}**")
            with value_col:
                st.markdown(f"{value}")
        st.markdown("---")

    if not summary_file.exists():
        st.warning("Summary file not found.")
    else:
        with summary_file.open(newline="", encoding="utf-8") as fh:
            summary_rows = list(csv.DictReader(fh))

        if summary_rows:
            summary_df = pd.DataFrame(summary_rows)
            numeric_cols = [
                "hands",
                "profit",
                "roi_pct",
                "avg_bet",
                "stdev_delta",
                "errors",
                "wins",
                "losses",
                "pushes",
            ]
            for col in numeric_cols:
                if col in summary_df.columns:
                    summary_df[col] = pd.to_numeric(summary_df[col], errors="coerce")

            roi_values = summary_df["roi_pct"].dropna().tolist() if "roi_pct" in summary_df else []
            avg_roi = fmean(roi_values) if roi_values else 0.0

            total_hands = summary_df["hands"].sum() if "hands" in summary_df else 0
            total_wins = summary_df["wins"].sum() if "wins" in summary_df else 0
            win_rate = (total_wins / total_hands * 100) if total_hands else 0.0

            starting_balance = params.get("starting_balance")
            bankrupt_runs = 0
            if starting_balance is not None and "profit" in summary_df:
                bankrupt_runs = int(
                    (summary_df["profit"] + float(starting_balance)).le(0).sum()
                )

            col_roi, col_win, col_bank = st.columns(3)
            col_roi.metric("Average ROI", f"{avg_roi:.2f}%")
            col_win.metric("Win rate", f"{win_rate:.2f}%")
            if starting_balance is not None:
                col_bank.metric("Bankrupt runs", f"{bankrupt_runs} / {len(summary_df)}")
            else:
                col_bank.metric("Bankrupt runs", "N/A")

            if roi_values:
                st.markdown("#### ROI distribution")
                chart_df = pd.DataFrame({"ROI (%)": roi_values})
                histogram = (
                    alt.Chart(chart_df)
                    .mark_bar(opacity=0.75)
                    .encode(
                        alt.X("ROI (%)", bin=alt.Bin(maxbins=20), title="ROI (%)"),
                        alt.Y("count()", title="Simulations"),
                        tooltip=[alt.Tooltip("count()", title="Simulations")],
                    )
                    .properties(height=240)
                )
                st.altair_chart(histogram, use_container_width=True)

            st.subheader("Summary")
            st.dataframe(summary_df, width="stretch")
        else:
            st.info("Summary file is empty.")

    run_files = sorted(selected_folder.glob("sim_*.csv"))
    if run_files:
        run_options = [f.name for f in run_files]
        run_selected = st.selectbox("Run detail", options=run_options)
        detail_file = selected_folder / run_selected
        with detail_file.open(newline="", encoding="utf-8") as fh:
            run_reader = list(csv.DictReader(fh))
        st.subheader(f"Details: {run_selected}")
        st.dataframe(run_reader, width="stretch")
    else:
        st.info("No individual simulation files were found in this folder.")
