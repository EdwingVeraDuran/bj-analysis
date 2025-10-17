from __future__ import annotations
from bisect import bisect_right
from typing import Iterable

DEFAULT_TABLE = [
    (float("-inf"), 1),
    (1, 2),
    (3, 4),
    (5, 8),
]

def bet_multiplier(true_count: float, table: Iterable[tuple[float, int]] = DEFAULT_TABLE) -> int:
    thresholds = [t for t,_ in table]
    mults = [m for _,m in table]
    i = bisect_right(thresholds, true_count) - 1
    return mults[max(0, i)]
