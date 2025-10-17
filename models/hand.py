from __future__ import annotations
from typing import List
from models.card import Card

class Hand:
    def __init__(self) -> None:
        self.cards: List[Card] = []

    def add(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def values(self) -> tuple[int, int]:
        # (min_total, max_total) Taking into account Ases
        total = sum(11 if c.is_ace else c.value for c in self.cards)
        aces = sum(1 for c in self.cards if c.is_ace)
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return (total, total)

    @property
    def total(self) -> int:
        return self.values[1]

    @property
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.total == 21

    @property
    def is_bust(self) -> bool:
        return self.total > 21

    @property
    def is_soft(self) -> bool:
        hard_total = sum(c.value if not c.is_ace else 1 for c in self.cards)
        return any(c.is_ace for c in self.cards) and (hard_total + 10) == self.total and self.total <= 21


