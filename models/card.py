from dataclasses import dataclass

RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
SUITS = ["♠","♥","♦","♣"]

@dataclass(frozen=True, slots=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        if self.rank not in RANKS:
            raise ValueError(f"Invalid rank: {self.rank}")
        if self.suit not in SUITS:
            raise ValueError(f"Invalid suit: {self.suit}")

    @property
    def is_ace(self) -> bool:
        return self.rank == "A"

    @property
    def value(self) -> int:
        if self.rank in ["J", "Q", "K", "10"]:
            return 10
        if self.rank == "A":
            return 11
        return int(self.rank)
