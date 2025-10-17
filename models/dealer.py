from __future__ import annotations
from models.hand import Hand
from models.deck import Shoe

class Dealer:
    def __init__(self, hit_soft_17: bool = False):
        self.hand = Hand()
        self.hit_soft_17 = hit_soft_17

    def play(self, shoe: Shoe) -> None:
        while True:
            total = self.hand.total
            soft = self.hand.is_soft
            if total < 17:
                self.hand.add(shoe.deal(1)[0])
            elif total == 17 and soft and self.hit_soft_17:
                self.hand.add(shoe.deal(1)[0])
            else:
                break
