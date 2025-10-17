from __future__ import annotations

class Player:
    def __init__(self, starting_balance: int, base_bet: int) -> None:
        self.balance = starting_balance
        self.base_bet = base_bet

    def can_bet(self, amount: int) -> bool:
        return self.balance >= amount

    def place_bet(self, amount: int) -> int:
        if not self.can_bet(amount):
            raise ValueError("Insufficient funds to bet")
        self.balance -= amount
        return amount

    def settle(self, net: int) -> None:
        self.balance += net
