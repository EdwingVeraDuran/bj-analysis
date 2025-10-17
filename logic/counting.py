from __future__ import annotations
from models.card import Card

def hilo_value(card: Card) -> int:
    if card.rank in ["2", "3", "4", "5", "6"]:
        return +1
    if card.rank in ["7", "8", "9"]:
        return 0
    return -1

class Counter:
    def __init__(self):
        self.running = 0

    def observe(self, card: Card) -> None:
        self.running += hilo_value(card)

    def true_count(self, decks_reamining: float) -> float:
        if decks_reamining <= 0:
            return float(self.running)
        return self.running / decks_reamining
