from __future__ import annotations

import csv
import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from utils.config import CONFIG


st.header("📂 Simulation Results")

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

    summary_file = selected_folder / "summary.csv"
    if not summary_file.exists():
        st.warning("Summary file not found.")
    else:
        with summary_file.open(newline="", encoding="utf-8") as fh:
            reader = list(csv.DictReader(fh))
        st.subheader("Summary")
        st.dataframe(reader, width="stretch")

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
