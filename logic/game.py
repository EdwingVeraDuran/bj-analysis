from __future__ import annotations
from dataclasses import dataclass
from models.player import Player
from models.dealer import Dealer
from models.hand import Hand
from models.deck import Shoe
from models.card import Card
from logic.counting import Counter
from logic.strategy import bet_multiplier, DEFAULT_TABLE

@dataclass(slots=True)
class HandResult:
    bet: int
    delta: int
    running_count: int
    true_count: float
    player_total: int
    dealer_total: int
    is_player_bj: bool
    is_dealer_bj: bool
    player_cards: tuple[str, ...]
    dealer_cards: tuple[str, ...]

_SUIT_LABELS = {
    "\u2660": "S",
    "\u2665": "H",
    "\u2666": "D",
    "\u2663": "C",
}

def _format_cards(hand: Hand) -> tuple[str, ...]:
    return tuple(f"{c.rank}{_SUIT_LABELS.get(c.suit, c.suit)}" for c in hand.cards)

def settle_hand(player_bet: int, player_bj: bool, dealer_bj: bool, player_total: int, dealer_total: int, blackjack_payout: float = 1.5) -> int:
    if player_bj and not dealer_bj:
        return int(round(player_bet * blackjack_payout))
    if dealer_bj and not player_bj:
        return -player_bet
    if player_total > 21:
        return -player_bet
    if dealer_total > 21:
        return player_bet
    if player_total > dealer_total:
        return player_bet
    if player_total < dealer_total:
        return -player_bet
    return 0

def basic_player_policy(player: Hand, dealer_up: Card) -> str:
    if player.total <= 11:
        return "HIT"
    if dealer_up.rank in ["7", "8", "9", "10", "J", "Q", "K", "A"] and player.total < 17:
        return "HIT"
    if player.total < 12:
        return "HIT"
    return "STAND"

def play_one_hand(player: Player, dealer: Dealer, shoe: Shoe, counter: Counter, base_bet: int, table=DEFAULT_TABLE, blackjack_payout: float = 1.5) -> HandResult:
    if shoe.needs_shuffle():
        shoe.shuffle()
        counter.running = 0

    tc = counter.true_count(shoe.decks_remaining)
    mult = bet_multiplier(tc, table)
    bet = max(base_bet * mult, base_bet)
    if not player.can_bet(bet):
        bet = player.balance if player.balance > 0 else 0
        if bet == 0:
            return HandResult(0, 0, counter.running, tc, 0, 0, False, False, tuple(), tuple())

    player.place_bet(bet)

    p = Hand()
    d = Dealer(hit_soft_17=dealer.hit_soft_17)
    d.hand.add(shoe.deal(1)[0]); p.add(shoe.deal(1)[0])
    d.hand.add(shoe.deal(1)[0]); p.add(shoe.deal(1)[0])

    for c in p.cards + d.hand.cards:
        counter.observe(c)

    while True:
        action = basic_player_policy(p, dealer_up=d.hand.cards[1])
        if action == "HIT":
            c = shoe.deal(1)[0]
            p.add(c)
            counter.observe(c)
            if p.total >= 21:
                break
        else:
            break

    while True:
        total = d.hand.total
        soft = d.hand.is_soft
        if total < 17 or (total == 17 and soft and d.hit_soft_17):
            c = shoe.deal(1)[0]
            d.hand.add(c)
            counter.observe(c)
        else:
            break

    delta = settle_hand(
        player_bet=bet,
        player_bj=p.is_blackjack,
        dealer_bj=d.hand.is_blackjack,
        player_total=p.total,
        dealer_total=d.hand.total,
        blackjack_payout=blackjack_payout,
    )

    player.settle(bet + delta)

    return HandResult(
        bet=bet,
        delta=delta,
        running_count=counter.running,
        true_count=counter.true_count(shoe.decks_remaining),
        player_total=p.total,
        dealer_total=d.hand.total,
        is_player_bj=p.is_blackjack,
        is_dealer_bj=d.hand.is_blackjack,
        player_cards=_format_cards(p),
        dealer_cards=_format_cards(d.hand),
    )

