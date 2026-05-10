#!/usr/bin/env python3
"""Minimal single-question example: linear trend forecast."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "tables"


def main() -> int:
    days = [1, 2, 3, 4, 5]
    demand = [80, 86, 90, 95, 99]
    slope = (demand[-1] - demand[0]) / (days[-1] - days[0])
    forecast = demand[-1] + slope
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {
                "method": "linear_trend_baseline",
                "day": 6,
                "forecast_demand": round(forecast, 2),
                "unit": "件",
            }
        ]
    ).to_csv(TABLE_DIR / "tab_q1_result.csv", index=False)
    print(f"day_6_forecast={forecast:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

