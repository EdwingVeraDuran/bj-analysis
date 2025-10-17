from __future__ import annotations
from dataclasses import dataclass
from typing import List, Iterable
import math
import csv

@dataclass(slots=True)
class Summary:
    hands: int
    profit: int
    roi_pct: float
    avg_bet: float
    stdev_delta: float
    errors: int
    wins: int
    losses: int
    pushes: int

def to_csv(path: str, rows: Iterable[dict]) -> None:
    rows = list(rows)
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def summarize(hand_rows: List[dict]) -> Summary:
    hands = len(hand_rows)
    profit = sum(r["delta"] for r in hand_rows)
    avg_bet = sum(r["bet"] for r in hand_rows) / hands if hands else 0
    mean = profit / hands if hands else 0
    var = sum((r["delta"] - mean)**2 for r in hand_rows) / (hands-1 if hands > 1 else 1)
    stdev = math.sqrt(var)

    errors = sum(1 for r in hand_rows if r.get("bet_error", False))

    roi_pct = (profit / sum(r["bet"] for r in hand_rows) * 100) if hands and sum(r["bet"] for r in hand_rows) else 0

    wins = sum(1 for r in hand_rows if r["delta"] > 0)
    losses = sum(1 for r in hand_rows if r["delta"] < 0)
    pushes = sum(1 for r in hand_rows if r["delta"] == 0)

    return Summary(
        hands=hands,
        profit=profit,
        roi_pct=roi_pct,
        avg_bet=avg_bet,
        stdev_delta=stdev,
        errors=errors,
        wins=wins,
        losses=losses,
        pushes=pushes,
    )
