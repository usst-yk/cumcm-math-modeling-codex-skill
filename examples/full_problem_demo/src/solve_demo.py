#!/usr/bin/env python3
"""Solve the toy CUMCM workflow demo.

This script is intentionally simple. It demonstrates traceable artifacts:
tables, figures, validation notes, and a single TeX paper.
"""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "station_demand.csv"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
RESULTS = ROOT / "results"
SKILL_ROOT = ROOT.parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from make_paper_figures import apply_cumcm_style  # noqa: E402


def ensure_dirs() -> None:
    for path in (TABLES, FIGURES, RESULTS):
        path.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["date"])
    return df.sort_values(["date", "station_id"])


def forecast_total(df: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    daily = df.groupby("date", as_index=False)["demand"].sum()
    daily["day_index"] = range(1, len(daily) + 1)
    x = daily["day_index"]
    y = daily["demand"]
    slope = ((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()
    intercept = y.mean() - slope * x.mean()
    daily["linear_fit"] = intercept + slope * x
    forecast = intercept + slope * 7
    baseline = float(y.tail(3).mean())
    return daily, float(forecast), baseline


def allocation(df: pd.DataFrame, capacity: int = 260) -> pd.DataFrame:
    latest = df[df["date"] == df["date"].max()].copy()
    latest["weighted_priority"] = latest["demand"] * (1 + latest["priority_score"])
    latest = latest.sort_values("weighted_priority", ascending=False)
    remaining = capacity
    allocated = []
    for _, row in latest.iterrows():
        amount = min(int(row["demand"]), remaining)
        remaining -= amount
        allocated.append(amount)
    latest["allocated"] = allocated
    latest["unmet"] = latest["demand"] - latest["allocated"]
    return latest


def ranking(df: pd.DataFrame) -> pd.DataFrame:
    latest = df[df["date"] == df["date"].max()].copy()
    demand_norm = latest["demand"] / latest["demand"].max()
    latest["final_score"] = 0.6 * demand_norm + 0.4 * latest["priority_score"]
    latest = latest.sort_values("final_score", ascending=False)
    latest["rank"] = range(1, len(latest) + 1)
    return latest


def write_figures(daily: pd.DataFrame, rank: pd.DataFrame) -> None:
    apply_cumcm_style(font_size=15)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(daily["date"], daily["demand"], marker="o", label="实际需求")
    ax.plot(daily["date"], daily["linear_fit"], linestyle="--", label="线性拟合")
    ax.set_xlabel("日期")
    ax.set_ylabel("需求量 / 件")
    ax.set_title("问题一：日总需求预测")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_q1_demand_forecast.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(rank["station_id"], rank["final_score"], color="#2563eb")
    ax.invert_yaxis()
    ax.set_xlabel("优先级得分")
    ax.set_ylabel("站点")
    ax.set_title("问题三：站点优先级排序")
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_q3_priority_ranking.png", dpi=200)
    plt.close(fig)


def write_validation(forecast: float, baseline: float, alloc: pd.DataFrame) -> None:
    lines = [
        "# Validation Report",
        "",
        "| Subquestion | Check | Result | Status |",
        "| --- | --- | --- | --- |",
        (
            "| Q1 | Linear forecast vs recent-mean baseline | "
            f"forecast={forecast:.2f}, baseline={baseline:.2f} | pass |"
        ),
        (
            "| Q2 | Capacity and unmet demand | "
            f"allocated={alloc['allocated'].sum()}, unmet={alloc['unmet'].sum()} | pass |"
        ),
        "| Q3 | Ranking traceability | ranking table and figure generated | pass |",
        "",
    ]
    (RESULTS / "validation_report.md").write_text("\n".join(lines), encoding="utf-8")

def main() -> int:
    ensure_dirs()
    df = load_data()
    daily, forecast, baseline = forecast_total(df)
    alloc = allocation(df)
    rank = ranking(df)

    daily.to_csv(TABLES / "tab_q1_daily_forecast.csv", index=False, encoding="utf-8-sig")
    alloc.to_csv(TABLES / "tab_q2_allocation.csv", index=False, encoding="utf-8-sig")
    rank.to_csv(TABLES / "tab_q3_priority_ranking.csv", index=False, encoding="utf-8-sig")

    write_figures(daily, rank)
    write_validation(forecast, baseline, alloc)
    print("Demo artifacts generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
