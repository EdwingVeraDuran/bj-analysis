from __future__ import annotations

import argparse
import json
import random
from datetime import datetime
from pathlib import Path

from models.player import Player
from models.dealer import Dealer
from models.deck import Shoe
from logic.counting import Counter
from logic.game import play_one_hand
from logic.stats import to_csv, summarize
from utils.config import CONFIG
from utils.display import print_summary


def build_args():
    p = argparse.ArgumentParser(description="Blackjack Hi-Lo Simulator")
    p.add_argument("--decks", type=int, default=CONFIG["decks"])
    p.add_argument("--starting-balance", type=int, default=CONFIG["starting_balance"])
    p.add_argument("--base-bet", type=int, default=CONFIG["base_bet"])
    p.add_argument("--penetration", type=float, default=CONFIG["penetration"])
    p.add_argument("--hit-soft-17", action="store_true" if CONFIG["hit_soft_17"] else "store_false")
    p.add_argument("--blackjack-payout", type=float, default=CONFIG["blackjack_payout"])
    p.add_argument("--simulations", type=int, default=CONFIG["simulations"])
    p.add_argument("--csv-path", type=str, default=CONFIG["csv_path"])
    p.add_argument("--runs", type=int, default=1, help="Cantidad de simulaciones independientes a ejecutar")
    p.add_argument(
        "--rng-seed",
        type=int,
        default=CONFIG["rng_seed"],
        help="Semilla para reproducibilidad; omitir para aleatoriedad",
    )
    args = p.parse_args()
    if args.runs < 1:
        p.error("--runs debe ser >= 1")
    return args


def format_run_timestamp() -> str:
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.%f")
    return ts[:-3]


def resolve_output_base(csv_path: Path) -> Path:
    return csv_path.parent if csv_path.suffix else csv_path


def create_output_dir(base_path: Path, runs: int, timestamp: str) -> Path:
    directory = base_path / f"{timestamp}_runs{runs}"
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def write_parameters(directory: Path, metadata: dict) -> None:
    metadata_path = directory / "parameters.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def simulate_once(args, seed: int | None):
    rng = random.Random(seed) if seed is not None else random.Random()
    shoe = Shoe(num_decks=args.decks, rng=rng, penetration=args.penetration)
    player = Player(starting_balance=args.starting_balance, base_bet=args.base_bet)
    dealer = Dealer(hit_soft_17=args.hit_soft_17)
    counter = Counter()

    rows = []
    for i in range(1, args.simulations + 1):
        res = play_one_hand(
            player=player,
            dealer=dealer,
            shoe=shoe,
            counter=counter,
            base_bet=args.base_bet,
            blackjack_payout=args.blackjack_payout,
        )
        # Marcar errores de apuesta (definicion provisional)
        bet_error = int(
            (res.true_count <= 0 and res.bet > args.base_bet)
            or (res.true_count >= 3 and res.bet < args.base_bet * 4)
        )
        rows.append(
            {
                "hand": i,
                "bet": res.bet,
                "delta": res.delta,
                "running_count": res.running_count,
                "true_count": round(res.true_count, 2),
                "player_total": res.player_total,
                "dealer_total": res.dealer_total,
                "is_player_bj": int(res.is_player_bj),
                "is_dealer_bj": int(res.is_dealer_bj),
                "bet_error": bet_error,
                "result": "win" if res.delta > 0 else "loss" if res.delta < 0 else "push",
                "player_cards": " ".join(res.player_cards) if res.player_cards else "-",
                "dealer_cards": " ".join(res.dealer_cards) if res.dealer_cards else "-",
            }
        )

    summary = summarize(rows)
    return rows, summary


def main():
    args = build_args()

    base_csv_path = Path(args.csv_path)
    output_base = resolve_output_base(base_csv_path)
    timestamp = format_run_timestamp()
    output_dir = create_output_dir(output_base, args.runs, timestamp)

    metadata = {
        "generated_at": timestamp,
        "runs": args.runs,
        "parameters": {
            "decks": args.decks,
            "starting_balance": args.starting_balance,
            "base_bet": args.base_bet,
            "penetration": args.penetration,
            "hit_soft_17": args.hit_soft_17,
            "blackjack_payout": args.blackjack_payout,
            "hands_per_run": args.simulations,
            "rng_seed": args.rng_seed,
        },
    }
    write_parameters(output_dir, metadata)

    summary_rows = []

    for run_idx in range(1, args.runs + 1):
        seed = args.rng_seed + run_idx - 1 if args.rng_seed is not None else None
        rows, summary = simulate_once(args, seed)
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

        print(f"=== Simulacion {run_idx} ===")
        print_summary(summary)

    summary_path = output_dir / "summary.csv"
    to_csv(str(summary_path), summary_rows)
    print(f"Archivos guardados en {output_dir}")


if __name__ == "__main__":
    main()
