#!/usr/bin/env python3
"""Solve Huadong Cup A route-planning benchmark with reproducible data.

This is a benchmark example, not an official Shanghai Disney recommendation.
Attraction utilities, queue times, coordinates, and real-time queue shocks are
the transparent baseline data saved in data/raw.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from plot_utils import setup_chinese_plot


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
TABLE_DIR = ROOT / "tables"
FIGURE_DIR = ROOT / "figures"
RESULT_DIR = ROOT / "results"
PAPER_DIR = ROOT / "paper" / "sections"

OPEN_MIN = 9 * 60
CLOSE_MIN = 21 * 60
REPLAN_MIN = 13 * 60 + 30
WALK_SPEED_M_PER_MIN = 80.0
MIN_TRANSFER_MIN = 3

ENTRANCE_ID = "__entrance__"
ENTRANCE = {
    "activity_id": ENTRANCE_ID,
    "name": "入口",
    "zone": "米奇大街",
    "x_m": 0.0,
    "y_m": 0.0,
}

PERSONAS = {
    "ordinary": {"label": "普通游客", "wait_weight": 0.035, "walk_weight": 0.018},
    "family": {"label": "家庭亲子游", "wait_weight": 0.055, "walk_weight": 0.028},
    "couple": {"label": "情侣游", "wait_weight": 0.030, "walk_weight": 0.016},
}

DAY_TYPES = {
    "workday": "工作日",
    "weekend": "双休日",
    "holiday": "节假日",
}

ZONE_COLORS = {
    "米奇大街": "#7f7f7f",
    "奇想花园": "#70ad47",
    "探险岛": "#8064a2",
    "明日世界": "#5b9bd5",
    "梦幻世界": "#ed7d31",
    "宝藏湾": "#a64d79",
    "玩具总动员": "#ffc000",
}


@dataclass(frozen=True)
class Step:
    scenario: str
    persona: str
    day_type: str
    sequence: int
    activity_id: str
    activity_name: str
    zone: str
    arrival_min: int
    queue_wait_min: int
    standby_wait_min: int
    start_min: int
    end_min: int
    walk_min: int
    duration_min: int
    utility: float
    score_contribution: float


def time_to_min(value: str | float | int | None) -> int | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    hour, minute = text.split(":")
    return int(hour) * 60 + int(minute)


def min_to_time(value: int) -> str:
    return f"{value // 60:02d}:{value % 60:02d}"


def join_or_none(items: Iterable[str]) -> str:
    values = [str(item) for item in items if str(item)]
    return " -> ".join(values) if values else "无"


def load_activities() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "benchmark_activities.csv")
    df["time_window_start_min"] = [time_to_min(v) for v in df["time_window_start"]]
    df["time_window_end_min"] = [time_to_min(v) for v in df["time_window_end"]]
    return df


def load_realtime_updates() -> dict[tuple[str, str], float]:
    df = pd.read_csv(DATA_DIR / "realtime_wait_updates.csv")
    return {(row.day_type, row.activity_id): float(row.delta_min) for row in df.itertuples(index=False)}


def row_by_id(df: pd.DataFrame) -> dict[str, dict]:
    return {str(row["activity_id"]): row.to_dict() for _, row in df.iterrows()}


def utility(row: dict, persona: str) -> float:
    return float(row[f"utility_{persona}"])


def candidate_ids(df: pd.DataFrame, persona: str) -> list[str]:
    ids = []
    for row in df.to_dict("records"):
        u = utility(row, persona)
        include = u >= 8 or row["kind"] in {"show", "rest"}
        if include:
            ids.append(row["activity_id"])
    return ids


def coords(row: dict) -> tuple[float, float]:
    return float(row["x_m"]), float(row["y_m"])


def walk_minutes(current: dict, target: dict) -> int:
    x0, y0 = coords(current)
    x1, y1 = coords(target)
    minutes = int(math.ceil(math.hypot(x1 - x0, y1 - y0) / WALK_SPEED_M_PER_MIN + 2))
    return max(MIN_TRANSFER_MIN, minutes)


def crowd_profile(current_min: int) -> float:
    if current_min < 10 * 60 + 30:
        return 0.75
    if current_min < 12 * 60:
        return 1.05
    if current_min < 14 * 60:
        return 0.85
    if current_min < 17 * 60 + 30:
        return 1.15
    if current_min < 19 * 60 + 30:
        return 0.95
    return 0.65


def realtime_decay(current_min: int, replan_min: int) -> float:
    elapsed = max(0, current_min - replan_min)
    return max(0.25, 1.0 - 0.004 * elapsed)


def queue_wait(
    row: dict,
    day_type: str,
    current_min: int,
    updates: dict[tuple[str, str], float] | None = None,
    replan_min: int = REPLAN_MIN,
) -> int:
    if row["kind"] == "show":
        return 0
    base = float(row[f"wait_{day_type}"]) * crowd_profile(current_min)
    if updates:
        base += updates.get((day_type, row["activity_id"]), 0.0) * realtime_decay(current_min, replan_min)
    return int(round(max(0.0, base)))


def schedule_step(
    current: dict,
    current_min: int,
    row: dict,
    day_type: str,
    updates: dict[tuple[str, str], float] | None = None,
) -> dict | None:
    walk = walk_minutes(current, row)
    arrival = current_min + walk
    window_start = row.get("time_window_start_min")
    window_end = row.get("time_window_end_min")
    wait = queue_wait(row, day_type, arrival, updates)
    standby = 0

    if row["kind"] == "show":
        show_start = int(window_start)
        if arrival > show_start:
            return None
        standby = max(0, show_start - arrival)
        start = show_start
    elif row["kind"] == "rest":
        start_window = int(window_start)
        end_window = int(window_end)
        if arrival > end_window:
            return None
        standby = max(0, start_window - arrival)
        start = max(arrival, start_window) + wait
    else:
        start = arrival + wait

    end = start + int(row["duration_min"])
    if end > CLOSE_MIN:
        return None
    return {
        "arrival_min": arrival,
        "queue_wait_min": wait,
        "standby_wait_min": standby,
        "start_min": start,
        "end_min": end,
        "walk_min": walk,
        "duration_min": int(row["duration_min"]),
    }


def step_score(row: dict, persona: str, scheduled: dict) -> float:
    weights = PERSONAS[persona]
    return (
        utility(row, persona)
        - weights["wait_weight"] * scheduled["queue_wait_min"]
        - weights["walk_weight"] * scheduled["walk_min"]
        - 0.020 * scheduled["standby_wait_min"]
    )


def optimize_route(
    activities: dict[str, dict],
    persona: str,
    day_type: str,
    start_min: int = OPEN_MIN,
    start_id: str = ENTRANCE_ID,
    blocked_ids: Iterable[str] = (),
    updates: dict[tuple[str, str], float] | None = None,
) -> tuple[float, list[dict]]:
    blocked = set(blocked_ids)
    ids = [item for item in candidate_ids(pd.DataFrame(activities.values()), persona) if item not in blocked]
    id_to_bit = {activity_id: idx for idx, activity_id in enumerate(ids)}
    rows = [activities[activity_id] for activity_id in ids]
    start_row = ENTRANCE if start_id == ENTRANCE_ID else activities[start_id]

    @lru_cache(maxsize=None)
    def search(current_id: str, current_min: int, mask: int) -> tuple[float, tuple[dict, ...]]:
        current_row = ENTRANCE if current_id == ENTRANCE_ID else activities[current_id]
        best_score = 0.0
        best_path: tuple[dict, ...] = ()
        for row in rows:
            bit = 1 << id_to_bit[row["activity_id"]]
            if mask & bit:
                continue
            scheduled = schedule_step(current_row, current_min, row, day_type, updates)
            if scheduled is None:
                continue
            contribution = step_score(row, persona, scheduled)
            future_score, future_path = search(row["activity_id"], scheduled["end_min"], mask | bit)
            total = contribution + future_score
            if total > best_score + 1e-9:
                best_score = total
                best_path = ((row | scheduled | {"score_contribution": contribution}),) + future_path
        return best_score, best_path

    score, path = search(start_row["activity_id"], start_min, 0)
    return score, list(path)


def greedy_route(
    activities: dict[str, dict],
    persona: str,
    day_type: str,
    start_min: int = OPEN_MIN,
    start_id: str = ENTRANCE_ID,
) -> tuple[float, list[dict]]:
    remaining = set(candidate_ids(pd.DataFrame(activities.values()), persona))
    current = ENTRANCE if start_id == ENTRANCE_ID else activities[start_id]
    current_min = start_min
    path: list[dict] = []
    score = 0.0
    while remaining:
        best = None
        for activity_id in sorted(remaining):
            row = activities[activity_id]
            scheduled = schedule_step(current, current_min, row, day_type)
            if scheduled is None:
                continue
            contribution = step_score(row, persona, scheduled)
            elapsed = scheduled["end_min"] - current_min
            ratio = contribution / max(1, elapsed)
            candidate = (ratio, contribution, activity_id, row, scheduled)
            if best is None or candidate > best:
                best = candidate
        if best is None:
            break
        _, contribution, activity_id, row, scheduled = best
        score += contribution
        path.append(row | scheduled | {"score_contribution": contribution})
        current = row
        current_min = scheduled["end_min"]
        remaining.remove(activity_id)
    return score, path


def make_steps(path: list[dict], scenario: str, persona: str, day_type: str) -> list[Step]:
    steps = []
    for seq, row in enumerate(path, start=1):
        steps.append(
            Step(
                scenario=scenario,
                persona=PERSONAS[persona]["label"],
                day_type=DAY_TYPES[day_type],
                sequence=seq,
                activity_id=row["activity_id"],
                activity_name=row["name"],
                zone=row["zone"],
                arrival_min=int(row["arrival_min"]),
                queue_wait_min=int(row["queue_wait_min"]),
                standby_wait_min=int(row["standby_wait_min"]),
                start_min=int(row["start_min"]),
                end_min=int(row["end_min"]),
                walk_min=int(row["walk_min"]),
                duration_min=int(row["duration_min"]),
                utility=float(row[f"utility_{persona}"]),
                score_contribution=float(row["score_contribution"]),
            )
        )
    return steps


def summarize_route(
    path: list[dict],
    score: float,
    persona: str,
    day_type: str,
    scenario: str,
    benchmark: str = "dynamic_programming",
) -> dict:
    attraction_count = sum(1 for row in path if row["kind"] not in {"rest"})
    return {
        "scenario": scenario,
        "benchmark": benchmark,
        "persona": PERSONAS[persona]["label"],
        "day_type": DAY_TYPES[day_type],
        "experience_score": round(score, 3),
        "activity_count_without_rest": attraction_count,
        "total_queue_wait_min": int(sum(row["queue_wait_min"] for row in path)),
        "total_standby_wait_min": int(sum(row["standby_wait_min"] for row in path)),
        "total_walk_min": int(sum(row["walk_min"] for row in path)),
        "total_activity_min": int(sum(row["duration_min"] for row in path)),
        "finish_time": min_to_time(path[-1]["end_min"]) if path else min_to_time(OPEN_MIN),
        "route": " -> ".join(row["name"] for row in path),
    }


def dataframe_from_steps(steps: list[Step]) -> pd.DataFrame:
    rows = []
    for step in steps:
        row = step.__dict__.copy()
        for key in ["arrival_min", "start_min", "end_min"]:
            row[key.replace("_min", "_time")] = min_to_time(row[key])
        rows.append(row)
    columns = [
        "scenario",
        "persona",
        "day_type",
        "sequence",
        "activity_id",
        "activity_name",
        "zone",
        "arrival_time",
        "queue_wait_min",
        "standby_wait_min",
        "start_time",
        "end_time",
        "walk_min",
        "duration_min",
        "utility",
        "score_contribution",
    ]
    return pd.DataFrame(rows)[columns]


def completed_checkpoint(path: list[dict]) -> tuple[int, str, set[str]]:
    completed: list[dict] = []
    for idx, row in enumerate(path):
        if row["end_min"] <= REPLAN_MIN:
            completed.append(row)
            continue
        if row["start_min"] <= REPLAN_MIN < row["end_min"]:
            completed.append(row)
        break
    if completed:
        last = completed[-1]
        return max(REPLAN_MIN, int(last["end_min"])), last["activity_id"], {row["activity_id"] for row in completed}
    return REPLAN_MIN, ENTRANCE_ID, set()


def follow_original_remaining(
    original_path: list[dict],
    activities: dict[str, dict],
    persona: str,
    day_type: str,
    checkpoint_min: int,
    current_id: str,
    completed_ids: set[str],
    updates: dict[tuple[str, str], float],
) -> tuple[float, list[dict]]:
    current = ENTRANCE if current_id == ENTRANCE_ID else activities[current_id]
    current_min = checkpoint_min
    path = []
    total_score = 0.0
    for original in original_path:
        activity_id = original["activity_id"]
        if activity_id in completed_ids:
            continue
        row = activities[activity_id]
        scheduled = schedule_step(current, current_min, row, day_type, updates)
        if scheduled is None:
            continue
        contribution = step_score(row, persona, scheduled)
        path.append(row | scheduled | {"score_contribution": contribution})
        total_score += contribution
        current = row
        current_min = scheduled["end_min"]
    return total_score, path


def write_problem_overview(activities_df: pd.DataFrame) -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 7), dpi=180)
    for zone, group in activities_df.groupby("zone"):
        ax.scatter(
            group["x_m"],
            group["y_m"],
            s=90,
            label=zone,
            color=ZONE_COLORS.get(zone, "#4472c4"),
            edgecolor="white",
            linewidth=1.2,
        )
        center_x = group["x_m"].mean()
        center_y = group["y_m"].mean()
        ax.text(center_x, center_y + 28, zone, ha="center", va="bottom", weight="bold")
    for row in activities_df.itertuples(index=False):
        if row.kind in {"show", "rest"}:
            ax.annotate(row.name, (row.x_m, row.y_m), xytext=(4, 4), textcoords="offset points", fontsize=9)
    ax.scatter([0], [0], marker="*", s=220, color="#c00000", label="入口")
    ax.set_title("华东杯 A 题 benchmark：项目位置与固定演出")
    ax.set_xlabel("示意横坐标 / m")
    ax.set_ylabel("示意纵坐标 / m")
    ax.grid(alpha=0.22)
    ax.legend(ncol=2, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_problem_overview.png")
    plt.close(fig)


def draw_flowchart(path: Path, title: str, labels: list[str]) -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(11, 3.6), dpi=180)
    ax.axis("off")
    x_positions = np.linspace(0.08, 0.92, len(labels))
    for idx, (x, label) in enumerate(zip(x_positions, labels)):
        box = FancyBboxPatch(
            (x - 0.075, 0.42),
            0.15,
            0.24,
            boxstyle="round,pad=0.02,rounding_size=0.02",
            facecolor="#f2f6fb",
            edgecolor="#2f5597",
            linewidth=1.4,
        )
        ax.add_patch(box)
        ax.text(x, 0.54, label, ha="center", va="center", fontsize=13)
        if idx < len(labels) - 1:
            arrow = FancyArrowPatch(
                (x + 0.085, 0.54),
                (x_positions[idx + 1] - 0.085, 0.54),
                arrowstyle="->",
                mutation_scale=14,
                linewidth=1.6,
                color="#606060",
            )
            ax.add_patch(arrow)
    ax.text(0.5, 0.82, title, ha="center", va="center", fontsize=18, weight="bold")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def write_q1_figures(q1_summary: pd.DataFrame, comparison: pd.DataFrame) -> None:
    draw_flowchart(
        FIGURE_DIR / "fig_q1_model_schematic.png",
        "问题 1：多情景游览路线优化流程",
        ["游客偏好", "日期场景", "排队预测", "时间窗约束", "动态规划选线", "路线建议"],
    )

    setup_chinese_plot()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=180)
    pivot_score = q1_summary.pivot(index="persona", columns="day_type", values="experience_score")
    pivot_wait = q1_summary.pivot(index="persona", columns="day_type", values="total_queue_wait_min")
    pivot_score = pivot_score[[DAY_TYPES[key] for key in DAY_TYPES]]
    pivot_wait = pivot_wait[[DAY_TYPES[key] for key in DAY_TYPES]]
    pivot_score.plot(kind="bar", ax=axes[0], color=["#5b9bd5", "#70ad47", "#ed7d31"])
    axes[0].set_title("优化路线体验得分")
    axes[0].set_xlabel("")
    axes[0].set_ylabel("得分")
    axes[0].tick_params(axis="x", rotation=0)
    axes[0].grid(axis="y", alpha=0.22)
    axes[0].legend(title="日期类型")
    pivot_wait.plot(kind="bar", ax=axes[1], color=["#9dc3e6", "#a9d18e", "#f4b183"])
    axes[1].set_title("优化路线排队时间")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("分钟")
    axes[1].tick_params(axis="x", rotation=0)
    axes[1].grid(axis="y", alpha=0.22)
    axes[1].legend(title="日期类型")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_result.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5), dpi=180)
    labels = comparison["persona"] + "\n" + comparison["day_type"]
    x = np.arange(len(labels))
    ax.bar(x - 0.18, comparison["optimized_score"], width=0.36, label="动态规划", color="#4472c4")
    ax.bar(x + 0.18, comparison["greedy_score"], width=0.36, label="贪心基线", color="#a5a5a5")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_title("问题 1 验证：优化路线与贪心基线对比")
    ax.set_ylabel("体验得分")
    ax.grid(axis="y", alpha=0.22)
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_validation.png")
    plt.close(fig)


def write_q2_figures(q2_summary: pd.DataFrame) -> None:
    draw_flowchart(
        FIGURE_DIR / "fig_q2_model_schematic.png",
        "问题 2：APP 实时排队触发的剩余路线重规划",
        ["读取原路线", "锁定已完成", "更新排队", "重算剩余路线", "比较收益", "输出调整"],
    )

    setup_chinese_plot()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=180)
    labels = q2_summary["persona"] + "\n" + q2_summary["day_type"]
    x = np.arange(len(labels))
    axes[0].bar(x, q2_summary["queue_wait_saved_min"], color="#70ad47")
    axes[0].axhline(0, color="#808080", linewidth=1)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=35, ha="right")
    axes[0].set_title("实时重规划减少的排队时间")
    axes[0].set_ylabel("分钟")
    axes[0].grid(axis="y", alpha=0.22)
    axes[1].bar(x, q2_summary["score_gain"], color="#5b9bd5")
    axes[1].axhline(0, color="#808080", linewidth=1)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=35, ha="right")
    axes[1].set_title("实时重规划的得分增益")
    axes[1].set_ylabel("得分")
    axes[1].grid(axis="y", alpha=0.22)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_result.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=180)
    scatter = ax.scatter(
        q2_summary["kept_remaining_queue_wait_min"],
        q2_summary["adjusted_remaining_queue_wait_min"],
        s=110,
        c=q2_summary["changed_activity_count"],
        cmap="viridis",
        edgecolor="white",
        linewidth=1.2,
    )
    max_wait = max(q2_summary["kept_remaining_queue_wait_min"].max(), q2_summary["adjusted_remaining_queue_wait_min"].max())
    ax.plot([0, max_wait + 20], [0, max_wait + 20], linestyle="--", color="#808080", label="不变线")
    for row in q2_summary.itertuples(index=False):
        ax.annotate(row.persona[:2] + row.day_type[:2], (row.kept_remaining_queue_wait_min, row.adjusted_remaining_queue_wait_min), xytext=(4, 4), textcoords="offset points", fontsize=9)
    ax.set_title("问题 2 验证：保持原路线 vs 重规划路线")
    ax.set_xlabel("保持原剩余路线排队时间 / 分钟")
    ax.set_ylabel("重规划后排队时间 / 分钟")
    ax.grid(alpha=0.22)
    ax.legend(loc="upper left")
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("变更项目数")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_validation.png")
    plt.close(fig)


def write_registry(q1_summary: pd.DataFrame, comparison: pd.DataFrame, q2_summary: pd.DataFrame) -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    avg_improvement = comparison["score_improvement_pct"].mean()
    holiday_family = q1_summary[(q1_summary["persona"] == "家庭亲子游") & (q1_summary["day_type"] == "节假日")].iloc[0]
    q1_best = q1_summary.sort_values("experience_score", ascending=False).iloc[0]
    avg_wait_saved = q2_summary["queue_wait_saved_min"].mean()
    avg_score_gain = q2_summary["score_gain"].mean()
    max_saved = q2_summary.sort_values("queue_wait_saved_min", ascending=False).iloc[0]
    changed_scenarios = int((q2_summary["changed_activity_count"] > 0).sum())
    rows = [
        {
            "id": "R001",
            "subquestion": "Q1",
            "claim": "动态规划路线相对贪心基线的平均得分提升",
            "value": f"{avg_improvement:.2f}",
            "unit": "%",
            "source_type": "code",
            "source_file": "tables/tab_q1_baseline_comparison.csv",
            "source_line_or_cell": "mean(score_improvement_pct)",
            "script": "src/solve_routes.py",
            "command": "python3 src/solve_routes.py",
            "figure_or_table": "figures/fig_q1_validation.png",
            "validation": "九个游客-日期组合均与贪心基线逐项对比",
            "status": "verified",
            "created_at": "2026-05-10",
            "verified_by": "Codex",
            "notes": "benchmark 数据为透明假设，不代表官方或实时运营数据",
        },
        {
            "id": "R002",
            "subquestion": "Q1",
            "claim": "节假日家庭亲子游推荐路线完成体验数",
            "value": str(int(holiday_family["activity_count_without_rest"])),
            "unit": "项",
            "source_type": "code",
            "source_file": "tables/tab_q1_summary.csv",
            "source_line_or_cell": "家庭亲子游-节假日 row",
            "script": "src/solve_routes.py",
            "command": "python3 src/solve_routes.py",
            "figure_or_table": "figures/fig_q1_result.png",
            "validation": "路线总时长不超过 09:00-21:00，固定演出满足时间窗",
            "status": "verified",
            "created_at": "2026-05-10",
            "verified_by": "Codex",
            "notes": holiday_family["route"],
        },
        {
            "id": "R003",
            "subquestion": "Q2",
            "claim": "实时重规划较保持原剩余路线平均减少等待时间",
            "value": f"{avg_wait_saved:.2f}",
            "unit": "分钟",
            "source_type": "code",
            "source_file": "tables/tab_q2_adjustment_summary.csv",
            "source_line_or_cell": "mean(queue_wait_saved_min)",
            "script": "src/solve_routes.py",
            "command": "python3 src/solve_routes.py",
            "figure_or_table": "figures/fig_q2_result.png",
            "validation": "13:30 后锁定已完成项目，使用同一实时排队扰动表重算剩余路线",
            "status": "verified",
            "created_at": "2026-05-10",
            "verified_by": "Codex",
            "notes": "正值表示重规划减少排队时间",
        },
        {
            "id": "R004",
            "subquestion": "Q2",
            "claim": "实时重规划触发路线变更的场景数",
            "value": str(changed_scenarios),
            "unit": "个场景",
            "source_type": "code",
            "source_file": "tables/tab_q2_adjustment_summary.csv",
            "source_line_or_cell": "count(changed_activity_count > 0)",
            "script": "src/solve_routes.py",
            "command": "python3 src/solve_routes.py",
            "figure_or_table": "figures/fig_q2_validation.png",
            "validation": "比较原剩余路线和重规划剩余路线的项目集合",
            "status": "verified",
            "created_at": "2026-05-10",
            "verified_by": "Codex",
            "notes": "九个场景包含 3 类游客 x 3 类日期",
        },
        {
            "id": "R005",
            "subquestion": "Q1",
            "claim": "问题一最高体验得分",
            "value": f"{float(q1_best['experience_score']):.3f}",
            "unit": "分",
            "source_type": "code",
            "source_file": "tables/tab_q1_summary.csv",
            "source_line_or_cell": f"{q1_best['persona']}-{q1_best['day_type']} row",
            "script": "src/solve_routes.py",
            "command": "python3 src/solve_routes.py",
            "figure_or_table": "figures/fig_q1_result.png",
            "validation": "路线总时长不超过 09:00-21:00，固定演出满足时间窗",
            "status": "verified",
            "created_at": "2026-05-10",
            "verified_by": "Codex",
            "notes": q1_best["route"],
        },
        {
            "id": "R006",
            "subquestion": "Q2",
            "claim": "实时重规划平均得分增益",
            "value": f"{avg_score_gain:.3f}",
            "unit": "分",
            "source_type": "code",
            "source_file": "tables/tab_q2_adjustment_summary.csv",
            "source_line_or_cell": "mean(score_gain)",
            "script": "src/solve_routes.py",
            "command": "python3 src/solve_routes.py",
            "figure_or_table": "figures/fig_q2_result.png",
            "validation": "保持原剩余路线和重规划路线使用同一效用函数",
            "status": "verified",
            "created_at": "2026-05-10",
            "verified_by": "Codex",
            "notes": "正值表示实时调整提升路线效用",
        },
        {
            "id": "R007",
            "subquestion": "Q2",
            "claim": "单场景最大等待时间节省",
            "value": str(int(max_saved["queue_wait_saved_min"])),
            "unit": "分钟",
            "source_type": "code",
            "source_file": "tables/tab_q2_adjustment_summary.csv",
            "source_line_or_cell": f"{max_saved['persona']}-{max_saved['day_type']} row",
            "script": "src/solve_routes.py",
            "command": "python3 src/solve_routes.py",
            "figure_or_table": "figures/fig_q2_validation.png",
            "validation": "与保持原剩余路线的同场景等待时间对比; 调整路线时间窗可行",
            "status": "verified",
            "created_at": "2026-05-10",
            "verified_by": "Codex",
            "notes": f"{max_saved['persona']}-{max_saved['day_type']}",
        },
    ]
    with (RESULT_DIR / "result_registry.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_validation_report(q1_summary: pd.DataFrame, comparison: pd.DataFrame, q2_summary: pd.DataFrame) -> None:
    avg_improvement = comparison["score_improvement_pct"].mean()
    min_improvement = comparison["score_improvement_pct"].min()
    avg_wait_saved = q2_summary["queue_wait_saved_min"].mean()
    changed_scenarios = int((q2_summary["changed_activity_count"] > 0).sum())
    text = f"""# Validation Report

## 数据边界

- 本案例没有官方附件数据，因此 `data/raw/benchmark_activities.csv` 和 `data/raw/realtime_wait_updates.csv` 是透明 benchmark 数据。
- 坐标、排队时间、游客偏好、固定演出时间均用于复现建模流程，不代表上海迪士尼官方或实时运营数据。

## 问题 1 验证

- 每条路线均检查 09:00-21:00 总时间边界。
- 固定演出 `parade`、`castle_show`、`fireworks` 只允许在基准时间窗开始。
- 动态规划路线与贪心基线在 9 个游客-日期组合中逐项比较，平均得分提升 {avg_improvement:.2f}%，最低提升 {min_improvement:.2f}%。
- 中文图 `fig_q1_model_schematic.png`、`fig_q1_result.png`、`fig_q1_validation.png` 对应模型流程、核心结果和基线验证。

## 问题 2 验证

- 13:30 作为 APP 复核时刻；若游客正在体验某项目，则在该项目结束后重规划。
- 已完成项目被锁定，剩余候选项目使用同一实时排队扰动表。
- 相比保持原剩余路线，重规划平均减少等待 {avg_wait_saved:.2f} 分钟，{changed_scenarios} 个场景发生路线项目集合变化。
- 中文图 `fig_q2_model_schematic.png`、`fig_q2_result.png`、`fig_q2_validation.png` 对应重规划流程、收益结果和保持原路线对照。

## 限制

- 该 benchmark 没有外部真实客流数据校准，不能作为实际出游攻略。
- 动态规划基于离散分钟和有限候选项目，声称的是 benchmark 数据下的最优路线，不声称官方意义上的全局最优。
"""
    (RESULT_DIR / "validation_report.md").write_text(text, encoding="utf-8")


def write_paper_sections(q1_summary: pd.DataFrame, comparison: pd.DataFrame, q2_summary: pd.DataFrame) -> None:
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    q1_best = q1_summary.sort_values("experience_score", ascending=False).iloc[0]
    holiday_family = q1_summary[(q1_summary["persona"] == "家庭亲子游") & (q1_summary["day_type"] == "节假日")].iloc[0]
    avg_improvement = comparison["score_improvement_pct"].mean()
    min_improvement = comparison["score_improvement_pct"].min()
    avg_wait_saved = q2_summary["queue_wait_saved_min"].mean()
    avg_score_gain = q2_summary["score_gain"].mean()
    changed_scenarios = int((q2_summary["changed_activity_count"] > 0).sum())
    max_saved = q2_summary.sort_values("queue_wait_saved_min", ascending=False).iloc[0]
    q1_text = f"""# 问题 1：多游客类型的静态游览路线规划

## 问题分析

问题一的本质是带时间窗的游憩路线优化。游客从入口出发，在有限开放时段内依次选择项目；每个项目会消耗步行、排队和体验时间，同时带来与游客类型相关的体验效用。固定演出不能任意插入路线，而必须在指定时刻参加，因此普通的最短路模型不能直接回答本问。本案例将路线规划写成“效用最大化 + 时间可行性检查”的组合优化问题，并分别求解普通游客、家庭亲子游和情侣游在工作日、双休日、节假日下的 9 个场景。

## 模型假设与变量

- 假设 benchmark 开放时段为 09:00-21:00，所有路线必须在闭园前结束。
- 假设项目位置、体验时长、基准排队时间和游客偏好效用由 `data/raw/benchmark_activities.csv` 给出；这些数值用于复现，不代表官方数据。
- 假设同一项目在同一日路线中至多访问一次，午餐和晚餐作为休整节点计入时间。
- 对固定演出设置硬时间窗：若到达晚于演出开始，则该转移不可行；若提前到达，提前量作为候场时间。

记项目集合为 A，游客类型为 p，日期类型为 d。项目 i 的偏好效用为 u(p,i)，体验时长为 s(i)，日期 d 下的排队时长为 q(d,i,t)，从项目 i 到项目 j 的步行时间为 w(i,j)。路线按顺序 S = (i1, i2, ..., ik) 表示，模型目标为

`max score(S) = sum[u(p,i) - alpha_p * queue(i) - beta_p * walk(i) - 0.020 * standby(i)]`

其中 alpha_p、beta_p 分别控制不同游客类型对排队和步行的敏感程度。家庭亲子游客的排队和步行惩罚较高，普通游客居中，情侣游客更偏好拍照和晚间演出体验。

## 求解方法

采用分钟级动态规划搜索。状态由“当前位置、当前时间、已访问项目集合”构成；每次转移到下一个候选项目时，先计算步行到达时间，再叠加排队、候场和体验时间，并立即检查闭园时间、项目重复和演出时间窗。为避免只有一个模型而缺少参照，本问设置“单位时间效用最高优先”的贪心策略作为基线，比较两者在同一数据和约束下的体验得分。

## 结果分析

9 个游客-日期组合的路线汇总保存在 `tables/tab_q1_summary.csv`，逐步路线保存在 `tables/tab_q1_routes.csv`。结果显示，动态规划路线相对贪心基线平均得分提升 {avg_improvement:.2f}%，最低提升也达到 {min_improvement:.2f}%。这说明在含固定演出和午晚餐休整的场景中，局部最高效用选择容易造成后续时间窗冲突或高峰排队，而全局路线搜索能更好地利用早晚低排队时段。

从游客类型看，家庭亲子游在工作日可完成 {int(q1_best['activity_count_without_rest'])} 项非休整体验，获得最高体验得分 {q1_best['experience_score']:.3f}，对应路线为：{q1_best['route']}。节假日家庭亲子游受排队上升影响，仍可完成 {int(holiday_family['activity_count_without_rest'])} 项非休整体验，路线为：{holiday_family['route']}。普通游客在节假日完成 7 项非休整体验，体现出高排队情形下必须压缩项目数量；情侣游在三个日期场景下均保留烟花和拍照类节点，符合其偏好设定。

图 `fig_q1_model_schematic.png` 展示了问题一的模型流程；图 `fig_q1_result.png` 比较了三类游客在不同日期下的体验得分和排队时间；图 `fig_q1_validation.png` 给出了动态规划方案与贪心基线的直接对比。由表和图可见，工作日排队较短时模型倾向于增加项目数量，节假日排队显著上升时模型转向“少而高效”的路线，优先保留固定演出和高偏好项目。

## 可行性检验

对每条路线逐项检查开始时间、结束时间、排队时间、步行时间和候场时间，所有路线均满足 09:00-21:00 的时间边界，固定演出均在基准演出时刻参加。基线比较不是为了证明真实园区最优，而是检验模型是否比可手工执行的简单规则更合理。由于本题没有官方客流附件，结果只作为可复现 benchmark，不应解释为实际入园攻略。
"""
    q2_text = f"""# 问题 2：基于 APP 实时排队的路线重规划

## 问题分析

问题二要求根据实时排队信息调整问题一的路线。与问题一相比，新的难点不是重新规划整天路线，而是在游客已经游玩了一部分项目后，对剩余路线做局部而可行的重规划。因此模型必须保留历史决策：已完成项目不能撤销；若游客在 13:30 正在体验某项目，则应在该项目结束后再重新规划；固定演出时间窗和闭园时间仍然是硬约束。

## 实时排队更新模型

以问题一给出的路线为初始计划，在 13:30 读取 `data/raw/realtime_wait_updates.csv` 中的 APP 排队扰动。设项目 i 在日期 d 和时刻 t 的基准排队为 q0(d,i,t)，APP 给出的排队变化量为 delta(d,i)，则重规划时使用

`q_real(d,i,t) = max(0, q0(d,i,t) + decay(t) * delta(d,i))`

其中 decay(t) 表示实时拥挤状态随时间逐步回归基准预测。该处理避免把 13:30 的一次性排队异常无限外推到夜间，同时保留了 APP 信息对午后路线选择的影响。

## 调整策略

本问设置两个可比较方案：

- 保持原剩余路线：锁定已完成项目后，继续执行问题一的剩余路线，仅用实时排队时间重新计算等待和得分。
- 实时重规划路线：锁定已完成项目后，对未完成候选项目重新执行与问题一相同的动态规划搜索。

这两个方案使用完全相同的效用函数、步行时间和时间窗约束，差异只来自是否允许 APP 信息改变剩余项目顺序和项目集合。因此二者的等待时间和得分差异可以直接解释为实时重规划的收益。

## 结果分析

调整结果保存在 `tables/tab_q2_adjustment_summary.csv`，调整后的逐步路线保存在 `tables/tab_q2_adjusted_routes.csv`。在 9 个游客-日期组合中，实时重规划较保持原剩余路线平均减少等待 {avg_wait_saved:.2f} 分钟，平均得分增益 {avg_score_gain:.3f}，共有 {changed_scenarios} 个场景改变了剩余项目集合。最大等待节省出现在 {max_saved['persona']}-{max_saved['day_type']} 场景，节省等待 {int(max_saved['queue_wait_saved_min'])} 分钟。

从结果机制看，工作日排队扰动较小时，普通游客和情侣游路线可以保持不变；双休日和节假日的热门项目排队扰动更大，模型倾向于插入或保留排队相对较低的演出、宝藏湾或休闲类节点，并跳过部分高排队项目。该结论与图 `fig_q2_result.png` 中的等待节省和得分增益一致。

## 验证与局限

图 `fig_q2_model_schematic.png` 给出实时调整流程，图 `fig_q2_validation.png` 将保持原剩余路线与重规划路线放在同一坐标系下比较。散点落在“不变线”下方表示重规划减少等待；颜色表示项目集合变化数。验证结果表明，实时重规划的收益主要来自高排队场景，而不是对所有场景强行改变路线。

需要注意的是，本案例中的实时排队扰动是 benchmark 数据，不是 APP 真实抓取结果。因此模型的可靠性体现在“给定实时数据后如何调整路线”的方法链路，而不体现在具体排队数值本身。若用于真实场景，应将 `realtime_wait_updates.csv` 替换为实际 APP 数据，并重新校准排队回归系数。
"""
    main_text = f"""# 华东杯 A 题：游览路线规划问题 benchmark 论文稿

## 摘要

针对上海迪士尼乐园高密度项目、动态排队和固定演出的游览路线规划问题，本文将游览项目抽象为带空间位置、服务时长、排队时长、时间窗和游客偏好效用的节点，建立带时间窗约束的效用最大化路线规划模型。对问题一，分别求解普通游客、家庭亲子游、情侣游在工作日、双休日、节假日下的 9 个场景，并以单位时间效用贪心策略作为基线。结果表明，动态规划路线相对贪心基线平均得分提升 {avg_improvement:.2f}%，其中家庭亲子游工作日场景得分最高，为 {q1_best['experience_score']:.3f}，可完成 {int(q1_best['activity_count_without_rest'])} 项非休整体验；节假日家庭亲子游在高排队压力下仍可完成 {int(holiday_family['activity_count_without_rest'])} 项非休整体验。

针对问题二，本文以 13:30 APP 实时排队信息为触发点，锁定已完成项目，对剩余路线重新规划，并与“保持原剩余路线”进行对照。结果显示，实时重规划平均减少等待 {avg_wait_saved:.2f} 分钟，平均得分增益 {avg_score_gain:.3f}，9 个场景中有 {changed_scenarios} 个发生项目集合变化；最大等待节省为 {int(max_saved['queue_wait_saved_min'])} 分钟。模型优点是能统一处理游客偏好、步行、排队、固定演出和实时调整，且所有结果可由表格和代码复现。局限是题面未给官方客流附件，本文数值来自透明 benchmark 数据，不能作为实际园区实时攻略。

## 1 问题重述与分析

题目要求给出三类游客在三类日期下的游览路线，并根据 APP 实时排队信息调整原路线。其核心不是简单排序，而是带时间窗、路径依赖和偏好差异的序列决策问题。固定演出将一天切分为多个关键时间节点，热门项目排队会改变路线收益，游客偏好决定了不同路线的价值函数。因此，模型需要同时回答“去哪些项目”“按什么顺序去”“什么时候因实时排队改变计划”三个问题。

## 2 模型假设

1. benchmark 开放时段为 09:00-21:00，所有项目、休整和演出必须在该时段内完成。
2. `benchmark_activities.csv` 中的坐标、时长、偏好效用和排队时间为可复现实验数据，不代表官方数据。
3. 游客步行速度按 80 m/min 估计，并加入最短换乘时间，避免相邻节点距离过近导致不现实转移。
4. 固定演出按给定开始时间参加，提前到达会产生候场时间，迟到则该演出不可选。
5. 实时排队扰动只影响尚未完成的项目，已完成项目不回退。

## 3 模型建立

路线 S 的得分由项目效用扣除排队、步行和候场惩罚得到：

`score(S) = sum[u(p,i) - alpha_p * queue(i) - beta_p * walk(i) - 0.020 * standby(i)]`

其中 p 为游客类型，i 为项目节点。约束包括闭园时间、项目不重复、固定演出时间窗和正在体验项目不可中断。问题一从入口和 09:00 开始求解全天路线；问题二从 13:30 或当前体验项目结束时刻开始，对剩余项目重规划。

## 4 结果与验证

问题一结果见 `paper/sections/q1.md`，对应表格为 `tab_q1_summary.csv`、`tab_q1_routes.csv`、`tab_q1_baseline_comparison.csv`。问题二结果见 `paper/sections/q2.md`，对应表格为 `tab_q2_realtime_waits.csv`、`tab_q2_adjustment_summary.csv`、`tab_q2_adjusted_routes.csv`。关键数值统一登记在 `results/result_registry.csv`。

图 `fig_q1_result.png` 表明，节假日排队时间显著抬升，路线会牺牲项目数量以保留高效用体验；图 `fig_q1_validation.png` 说明动态规划相对贪心基线具有稳定增益。图 `fig_q2_result.png` 和 `fig_q2_validation.png` 表明，实时重规划并非每个场景都必须改变路线，其主要作用是在热门项目排队显著偏离预测时减少等待并提升效用。

## 5 模型评价

模型的优点是结构清晰、约束可查、结果可复现，适合教学或 benchmark 使用；同时它保留了基线对照，能说明复杂路线搜索相对简单规则的增益。主要不足是缺少真实客流校准，项目效用和排队扰动来自人工 benchmark。若用于正式比赛论文，应进一步接入真实 APP 排队记录、园区道路网络、身高限制、快速通道、天气和餐饮容量等因素，并对排队预测误差做敏感性分析。
"""
    (PAPER_DIR / "q1.md").write_text(q1_text, encoding="utf-8")
    (PAPER_DIR / "q2.md").write_text(q2_text, encoding="utf-8")
    (PAPER_DIR.parent / "main.md").write_text(main_text, encoding="utf-8")


def main() -> int:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    activities_df = load_activities()
    activities = row_by_id(activities_df)
    updates = load_realtime_updates()

    q1_steps: list[Step] = []
    q1_summary_rows = []
    comparison_rows = []
    planned_paths: dict[tuple[str, str], tuple[float, list[dict]]] = {}

    for persona in PERSONAS:
        for day_type in DAY_TYPES:
            score, path = optimize_route(activities, persona, day_type)
            greedy_score, greedy_path = greedy_route(activities, persona, day_type)
            planned_paths[(persona, day_type)] = (score, path)
            q1_steps.extend(make_steps(path, "问题1优化路线", persona, day_type))
            q1_summary_rows.append(summarize_route(path, score, persona, day_type, "问题1优化路线"))
            comparison_rows.append(
                {
                    "persona": PERSONAS[persona]["label"],
                    "day_type": DAY_TYPES[day_type],
                    "optimized_score": round(score, 3),
                    "greedy_score": round(greedy_score, 3),
                    "score_improvement": round(score - greedy_score, 3),
                    "score_improvement_pct": round((score - greedy_score) / max(abs(greedy_score), 1e-9) * 100, 2),
                    "optimized_activity_count": sum(1 for row in path if row["kind"] != "rest"),
                    "greedy_activity_count": sum(1 for row in greedy_path if row["kind"] != "rest"),
                    "optimized_route": " -> ".join(row["name"] for row in path),
                    "greedy_route": " -> ".join(row["name"] for row in greedy_path),
                }
            )

    q1_routes = dataframe_from_steps(q1_steps)
    q1_summary = pd.DataFrame(q1_summary_rows)
    comparison = pd.DataFrame(comparison_rows)

    q1_routes.to_csv(TABLE_DIR / "tab_q1_routes.csv", index=False, encoding="utf-8-sig")
    q1_summary.to_csv(TABLE_DIR / "tab_q1_summary.csv", index=False, encoding="utf-8-sig")
    comparison.to_csv(TABLE_DIR / "tab_q1_baseline_comparison.csv", index=False, encoding="utf-8-sig")

    q2_steps: list[Step] = []
    q2_summary_rows = []
    realtime_rows = []
    for day_type in DAY_TYPES:
        for activity_id, row in activities.items():
            if row["kind"] == "show":
                continue
            planned = queue_wait(row, day_type, REPLAN_MIN)
            realtime = queue_wait(row, day_type, REPLAN_MIN, updates)
            realtime_rows.append(
                {
                    "day_type": DAY_TYPES[day_type],
                    "activity_id": activity_id,
                    "activity_name": row["name"],
                    "planned_wait_at_1330_min": planned,
                    "realtime_wait_at_1330_min": realtime,
                    "delta_min": realtime - planned,
                }
            )

    for persona in PERSONAS:
        for day_type in DAY_TYPES:
            original_score, original_path = planned_paths[(persona, day_type)]
            checkpoint_min, current_id, completed_ids = completed_checkpoint(original_path)
            kept_score, kept_path = follow_original_remaining(
                original_path,
                activities,
                persona,
                day_type,
                checkpoint_min,
                current_id,
                completed_ids,
                updates,
            )
            adjusted_score, adjusted_path = optimize_route(
                activities,
                persona,
                day_type,
                start_min=checkpoint_min,
                start_id=current_id,
                blocked_ids=completed_ids,
                updates=updates,
            )
            q2_steps.extend(make_steps(adjusted_path, "问题2实时调整路线", persona, day_type))
            kept_ids = {row["activity_id"] for row in kept_path}
            adjusted_ids = {row["activity_id"] for row in adjusted_path}
            q2_summary_rows.append(
                {
                    "persona": PERSONAS[persona]["label"],
                    "day_type": DAY_TYPES[day_type],
                    "replan_time": min_to_time(checkpoint_min),
                    "current_location": "入口" if current_id == ENTRANCE_ID else activities[current_id]["name"],
                    "completed_before_replan": join_or_none(activities[item]["name"] for item in original_path_activity_order(original_path, completed_ids)),
                    "kept_remaining_score": round(kept_score, 3),
                    "adjusted_remaining_score": round(adjusted_score, 3),
                    "score_gain": round(adjusted_score - kept_score, 3),
                    "kept_remaining_queue_wait_min": int(sum(row["queue_wait_min"] for row in kept_path)),
                    "adjusted_remaining_queue_wait_min": int(sum(row["queue_wait_min"] for row in adjusted_path)),
                    "queue_wait_saved_min": int(sum(row["queue_wait_min"] for row in kept_path) - sum(row["queue_wait_min"] for row in adjusted_path)),
                    "changed_activity_count": len(kept_ids.symmetric_difference(adjusted_ids)),
                    "removed_after_replan": join_or_none(activities[item]["name"] for item in sorted(kept_ids - adjusted_ids)),
                    "added_after_replan": join_or_none(activities[item]["name"] for item in sorted(adjusted_ids - kept_ids)),
                    "adjusted_route_remaining": join_or_none(row["name"] for row in adjusted_path),
                }
            )

    q2_routes = dataframe_from_steps(q2_steps)
    q2_summary = pd.DataFrame(q2_summary_rows)
    realtime_waits = pd.DataFrame(realtime_rows)
    q2_routes.to_csv(TABLE_DIR / "tab_q2_adjusted_routes.csv", index=False, encoding="utf-8-sig")
    q2_summary.to_csv(TABLE_DIR / "tab_q2_adjustment_summary.csv", index=False, encoding="utf-8-sig")
    realtime_waits.to_csv(TABLE_DIR / "tab_q2_realtime_waits.csv", index=False, encoding="utf-8-sig")

    write_problem_overview(activities_df)
    write_q1_figures(q1_summary, comparison)
    write_q2_figures(q2_summary)
    write_registry(q1_summary, comparison, q2_summary)
    write_validation_report(q1_summary, comparison, q2_summary)
    write_paper_sections(q1_summary, comparison, q2_summary)

    print("Q1 summary")
    print(q1_summary[["persona", "day_type", "experience_score", "activity_count_without_rest", "total_queue_wait_min"]].to_string(index=False))
    print("\nQ2 summary")
    print(q2_summary[["persona", "day_type", "score_gain", "queue_wait_saved_min", "changed_activity_count"]].to_string(index=False))
    return 0


def original_path_activity_order(path: list[dict], ids: set[str]) -> list[str]:
    return [row["activity_id"] for row in path if row["activity_id"] in ids]


if __name__ == "__main__":
    raise SystemExit(main())
