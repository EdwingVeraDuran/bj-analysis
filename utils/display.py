from __future__ import annotations
from logic.stats import Summary

def print_summary(s: Summary) -> None:
    print("=== Resumen ===")
    print(f"Manos: {s.hands}")
    print(f"Ganancia neta: {s.profit}")
    print(f"ROI: {s.roi_pct:.2f}%")
    print(f"Apuesta Prom.: {s.avg_bet:.2f}%")
    print(f"stDev delta: {s.stdev_delta:.2f}")
    print(f"Errores: {s.errors}")
    print(f"Ganadas: {s.wins}")
    print(f"Perdidas: {s.losses}")
    print(f"Empates: {s.pushes}")
