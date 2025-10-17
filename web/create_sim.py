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

st.markdown("---")
st.subheader("Parameter guide")
st.caption("Tune the knobs below to design the blackjack world you want to simulate.")
parameter_cards = [
    ("🎴", "# Decks", "How many decks are loaded into the shoe. More decks dilute counting edges and trigger shuffles less often."),
    ("💰", "Starting balance", "Initial bankroll for the player. Make sure it comfortably covers the bet spread you plan to test."),
    ("🎯", "Base bet", "Smallest wager the player makes. True-count multipliers scale from this stake, so raising it increases overall exposure."),
    ("✨", "Blackjack payout", "Payout when the player hits blackjack. Most casinos offer 3:2 (1.5); anything smaller hurts profitability."),
    ("🪄", "Penetration", "Share of the shoe dealt before a shuffle. Deeper penetration lets the count gain more predictive power."),
    ("🃏", "Hands per simulation", "Number of hands played per run. Longer runs smooth variance and give clearer averages."),
    ("📊", "Number of simulations", "How many independent runs to perform so you can compare distributions and aggregate results."),
    ("🤖", "Dealer hit soft 17", "Whether the dealer draws on soft 17. When enabled the house edge rises, altering optimal play."),
]

for icon, title, description in parameter_cards:
    icon_col, text_col = st.columns([0.12, 0.88])
    with icon_col:
        st.markdown(f"<div style='font-size:2rem; line-height:1;'>{icon}</div>", unsafe_allow_html=True)
    with text_col:
        st.markdown(f"**{title}**<br/><span style='color:#6c757d;'>{description}</span>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:0.3rem 0; opacity:0.15;'/>", unsafe_allow_html=True)
