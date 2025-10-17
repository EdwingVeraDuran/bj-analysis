from __future__ import annotations
import random
from collections import deque
from typing import Deque, Iterable
from models.card import Card, RANKS, SUITS

class Shoe:
    def __init__(self, num_decks: int = 6, rng: random.Random | None = None, penetration: float = 0.75):
        if num_decks < 1:
            raise ValueError("num_decks have to be >= 1")
        if not (0.5 <= penetration <= 0.95):
            raise ValueError("penetration have to be in between 0.5 and 0.95")
        self.num_decks = num_decks
        self.penetration = penetration
        self.rng = rng or random.Random()
        self._cards: Deque[Card] = deque()
        self._discard_tray: list[Card] = []
        self.shuffle()

    def _generate_decks(self) -> list[Card]:
        return [Card(rank, suit) for _ in range(self.num_decks) for suit in SUITS for rank in RANKS]

    def shuffle(self) -> None:
        cards = self._generate_decks()
        self.rng.shuffle(cards)
        self._cards = deque(cards)
        self._discard_tray.clear()

    @property
    def cards_remaining(self) -> int:
        return len(self._cards)

    @property
    def decks_remaining(self) -> float:
        return self.cards_remaining / 52.0

    def needs_shuffle(self) -> bool:
        consumed = self.num_decks*52 - self.cards_remaining
        return consumed >= (self.num_decks*52 * self.penetration)

    def deal(self, n: int = 1) -> list[Card]:
        if n < 1:
            raise ValueError("n have to be >= 1")
        dealt = []
        for _ in range(n):
            if not self._cards:
                self.shuffle()
            c = self._cards.popleft()
            dealt.append(c)
        return dealt

    def discard(self, cards: Iterable[Card]) -> None:
        self._discard_tray.extend(cards)
