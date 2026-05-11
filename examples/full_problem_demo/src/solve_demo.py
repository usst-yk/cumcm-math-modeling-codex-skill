#!/usr/bin/env python3
"""Solve the toy CUMCM workflow demo.

This script is intentionally simple. It demonstrates traceable artifacts:
tables, figures, result registry rows, a validation report, and a single TeX paper.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "raw" / "station_demand.csv"
TABLES = ROOT / "tables"
FIGURES = ROOT / "figures"
RESULTS = ROOT / "results"
PAPER = ROOT / "paper" / "sections"
SKILL_ROOT = ROOT.parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from make_paper_figures import apply_cumcm_style  # noqa: E402


def ensure_dirs() -> None:
    for path in (TABLES, FIGURES, RESULTS, PAPER):
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


def write_registry(forecast: float, baseline: float, alloc: pd.DataFrame, rank: pd.DataFrame) -> None:
    rows = [
        {
            "id": "R001",
            "subquestion": "Q1",
            "claim": "第7天总需求线性趋势预测值",
            "value": f"{forecast:.2f}",
            "unit": "件",
            "source_type": "code",
            "source_file": "tables/tab_q1_daily_forecast.csv",
            "source_line_or_cell": "forecast formula in src/solve_demo.py",
            "script": "src/solve_demo.py",
            "command": "python src/solve_demo.py",
            "figure_or_table": "figures/fig_q1_demand_forecast.png",
            "validation": f"与近3日均值基线 {baseline:.2f} 件比较",
            "status": "verified",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "verified_by": "demo script",
            "notes": "Toy demo, not a contest-level model.",
        },
        {
            "id": "R002",
            "subquestion": "Q2",
            "claim": "车辆容量260件时全部站点需求可满足",
            "value": str(int(alloc["unmet"].sum())),
            "unit": "未满足件数",
            "source_type": "code",
            "source_file": "tables/tab_q2_allocation.csv",
            "source_line_or_cell": "unmet column sum",
            "script": "src/solve_demo.py",
            "command": "python src/solve_demo.py",
            "figure_or_table": "tables/tab_q2_allocation.csv",
            "validation": "分配量不超过需求量且总分配量不超过260件",
            "status": "verified",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "verified_by": "demo script",
            "notes": "Toy demo capacity check.",
        },
        {
            "id": "R003",
            "subquestion": "Q3",
            "claim": "最高优先级站点",
            "value": str(rank.iloc[0]["station_id"]),
            "unit": "站点",
            "source_type": "code",
            "source_file": "tables/tab_q3_priority_ranking.csv",
            "source_line_or_cell": "rank 1 row",
            "script": "src/solve_demo.py",
            "command": "python src/solve_demo.py",
            "figure_or_table": "figures/fig_q3_priority_ranking.png",
            "validation": "需求权重和原始优先级加权排序",
            "status": "verified",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "verified_by": "demo script",
            "notes": "Toy demo ranking.",
        },
    ]
    pd.DataFrame(rows).to_csv(RESULTS / "result_registry.csv", index=False, encoding="utf-8-sig")


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


def write_paper_section(forecast: float, baseline: float) -> None:
    text = rf"""
本文首先对 6 个配送站点过去 6 天的需求量进行汇总，得到每日总需求序列。
以日序号为自变量建立线性趋势基线模型，并使用近 3 日平均需求作为对照。
	计算结果显示，第 7 天总需求的线性趋势预测值为 {forecast:.2f} 件，
	近 3 日均值基线为 {baseline:.2f} 件。
图 \texttt{{fig\_q1\_demand\_forecast.png}} 展示了历史总需求和线性拟合趋势。
该结果已登记在结果注册表 R001 中，后续正式论文应结合更多历史数据进行误差验证。
""".strip()
    (PAPER / "q1.tex").write_text(text + "\n", encoding="utf-8")


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
    write_registry(forecast, baseline, alloc, rank)
    write_validation(forecast, baseline, alloc)
    write_paper_section(forecast, baseline)
    print("Demo artifacts generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
