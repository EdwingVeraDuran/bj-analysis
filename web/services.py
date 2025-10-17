from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, List, Tuple

from main import (
    create_output_dir,
    format_run_timestamp,
    resolve_output_base,
    simulate_once,
    write_parameters,
)
from logic.stats import to_csv
from utils.config import CONFIG


def _build_args(params: Dict[str, Any]) -> SimpleNamespace:
    return SimpleNamespace(**params)


def run_simulations(
    *,
    decks: int,
    starting_balance: int,
    base_bet: int,
    blackjack_payout: float,
    hands_per_sim: int,
    runs: int,
    hit_soft_17: bool,
    penetration: float | None = None,
) -> Tuple[Path, List[Dict[str, Any]]]:
    if runs < 1:
        raise ValueError("runs must be >= 1")
    if base_bet > starting_balance:
        raise ValueError("base_bet cannot exceed starting_balance")

    penetration = penetration if penetration is not None else CONFIG["penetration"]

    base_csv_path = Path(CONFIG["csv_path"])
    output_root = resolve_output_base(base_csv_path)
    timestamp = format_run_timestamp()
    output_dir = create_output_dir(output_root, runs, timestamp)

    args = _build_args(
        {
            "decks": decks,
            "starting_balance": starting_balance,
            "base_bet": base_bet,
            "penetration": penetration,
            "hit_soft_17": hit_soft_17,
            "blackjack_payout": blackjack_payout,
            "simulations": hands_per_sim,
        }
    )

    metadata = {
        "generated_at": timestamp,
        "runs": runs,
        "parameters": {
            "decks": decks,
            "starting_balance": starting_balance,
            "base_bet": base_bet,
            "penetration": penetration,
            "hit_soft_17": hit_soft_17,
            "blackjack_payout": blackjack_payout,
            "hands_per_run": hands_per_sim,
            "rng_seed": None,
        },
    }
    write_parameters(output_dir, metadata)

    summary_rows: List[Dict[str, Any]] = []

    for run_idx in range(1, runs + 1):
        rows, summary = simulate_once(args, seed=None)
        run_path = output_dir / f"sim_{run_idx}.csv"
        to_csv(str(run_path), rows)

        summary_rows.append(
            {
                "run": run_idx,
                "hands": summary.hands,
                "profit": summary.profit,
                "roi_pct": round(summary.roi_pct, 2),
                "avg_bet": round(summary.avg_bet, 2),
                "stdev_delta": round(summary.stdev_delta, 2),
                "errors": summary.errors,
                "wins": summary.wins,
                "losses": summary.losses,
                "pushes": summary.pushes,
            }
        )

    summary_path = output_dir / "summary.csv"
    to_csv(str(summary_path), summary_rows)

    return output_dir, summary_rows
