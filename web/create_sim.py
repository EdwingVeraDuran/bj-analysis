from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from utils.config import CONFIG
from web.services import run_simulations


st.header("♠ Create Simulation")

with st.form("create"):
    decks_num = st.number_input("# Decks", min_value=1, max_value=12, value=CONFIG["decks"])
    starting_balance = st.number_input("Starting balance", min_value=1, step=1, value=CONFIG["starting_balance"])
    base_bet = st.number_input(
        "Base bet",
        min_value=1,
        step=1,
        value=min(CONFIG["base_bet"], starting_balance),
        max_value=starting_balance,
    )
    bj_payout = st.number_input("Blackjack payout", min_value=1.0, value=float(CONFIG["blackjack_payout"]))
    penetration = st.slider(
        "Penetration",
        min_value=0.5,
        max_value=0.95,
        value=float(CONFIG["penetration"]),
        step=0.01,
    )
    hands_to_sim = st.number_input("Hands per simulation", min_value=1, step=1, value=CONFIG["simulations"])
    num_simulations = st.number_input("Number of simulations", min_value=1, step=1, value=1)
    dealer_hit_soft_17 = st.toggle("Dealer hit soft 17", value=CONFIG["hit_soft_17"])

    submitted = st.form_submit_button("Run simulations")

    if submitted:
        try:
            output_dir, summary_rows = run_simulations(
                decks=int(decks_num),
                starting_balance=int(starting_balance),
                base_bet=int(base_bet),
                blackjack_payout=float(bj_payout),
                hands_per_sim=int(hands_to_sim),
                runs=int(num_simulations),
                hit_soft_17=bool(dealer_hit_soft_17),
                penetration=float(penetration),
            )
        except ValueError as exc:
            st.error(str(exc))
        else:
            st.success(f"Simulations stored in `{output_dir}`")
            st.session_state.setdefault("recent_runs", [])
            st.session_state["recent_runs"].append(str(output_dir))
            st.session_state["recent_runs"] = st.session_state["recent_runs"][-10:]
            st.session_state["last_summary"] = summary_rows
            st.session_state["last_output_dir"] = str(output_dir)

            st.subheader("Summary")
            st.dataframe(summary_rows, width="stretch")
            st.caption(f"Summary CSV saved at `{output_dir / 'summary.csv'}`")
