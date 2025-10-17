from __future__ import annotations
import argparse, random
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
    p.add_argument(
        "--rng-seed",
        type=int,
        default=CONFIG["rng_seed"],
        help="Semilla para reproducibilidad; omitir para aleatoriedad"
    )
    return p.parse_args()

def main():
    args = build_args()
    rng = random.Random(args.rng_seed)
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
        # Marcar errores de apuesta (definición provisional)
        bet_error = int((res.true_count <= 0 and res.bet > args.base_bet) or (res.true_count >= 3 and res.bet < args.base_bet*4))
        rows.append({
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
        })

    to_csv(args.csv_path, rows)
    summary = summarize(rows)
    print_summary(summary)

if __name__ == "__main__":
    main()
