#!/usr/bin/env python3
"""Solve CUMCM 2025 A Q1 with a reproducible geometric-kinematic model.

This demo uses the target-axis midpoint as the representative line-of-sight
point. It is intended as a traceable skill example, not an official answer.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import setup_chinese_plot


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "tables"
FIGURE_DIR = ROOT / "figures"

G = 9.8
MISSILE_SPEED = 300.0
UAV_SPEED = 120.0
SMOKE_SINK_SPEED = 3.0
SMOKE_RADIUS = 10.0
SMOKE_EFFECTIVE_SECONDS = 20.0
RELEASE_TIME = 1.5
FUSE_DELAY = 3.6
DETONATION_TIME = RELEASE_TIME + FUSE_DELAY

MISSILE_M1_0 = np.array([20000.0, 0.0, 2000.0])
DECOY = np.array([0.0, 0.0, 0.0])
TRUE_TARGET_AXIS_MIDPOINT = np.array([0.0, 200.0, 5.0])
FY1_0 = np.array([17800.0, 0.0, 1800.0])
FY1_DIRECTION = np.array([-1.0, 0.0, 0.0])


def unit(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        raise ValueError("zero vector cannot be normalized")
    return vector / norm


MISSILE_DIRECTION = unit(DECOY - MISSILE_M1_0)


def missile_position(t: float) -> np.ndarray:
    return MISSILE_M1_0 + MISSILE_SPEED * t * MISSILE_DIRECTION


def uav_position(t: float) -> np.ndarray:
    return FY1_0 + UAV_SPEED * t * FY1_DIRECTION


def bomb_position_after_release(t: float) -> np.ndarray:
    tau = t - RELEASE_TIME
    if tau < 0:
        raise ValueError("bomb has not been released")
    release_point = uav_position(RELEASE_TIME)
    velocity = UAV_SPEED * FY1_DIRECTION
    gravity = np.array([0.0, 0.0, -0.5 * G * tau * tau])
    return release_point + velocity * tau + gravity


DETONATION_POINT = bomb_position_after_release(DETONATION_TIME)


def smoke_center(t: float) -> np.ndarray:
    if t < DETONATION_TIME:
        raise ValueError("smoke has not detonated")
    return DETONATION_POINT + np.array([0.0, 0.0, -SMOKE_SINK_SPEED * (t - DETONATION_TIME)])


def distance_to_segment(point: np.ndarray, start: np.ndarray, end: np.ndarray) -> tuple[float, float]:
    segment = end - start
    length_sq = float(np.dot(segment, segment))
    if length_sq == 0:
        return float(np.linalg.norm(point - start)), 0.0
    projection = float(np.dot(point - start, segment) / length_sq)
    projection_clamped = min(1.0, max(0.0, projection))
    nearest = start + projection_clamped * segment
    return float(np.linalg.norm(point - nearest)), projection


def distance_margin(t: float) -> tuple[float, float, float]:
    distance, projection = distance_to_segment(
        smoke_center(t),
        missile_position(t),
        TRUE_TARGET_AXIS_MIDPOINT,
    )
    return distance - SMOKE_RADIUS, distance, projection


def is_effective(t: float) -> bool:
    if t < DETONATION_TIME or t > DETONATION_TIME + SMOKE_EFFECTIVE_SECONDS:
        return False
    margin, _, projection = distance_margin(t)
    return margin <= 0 and 0 <= projection <= 1


def refine_crossing(left: float, right: float) -> float:
    left_effective = is_effective(left)
    for _ in range(80):
        mid = (left + right) / 2
        if is_effective(mid) == left_effective:
            left = mid
        else:
            right = mid
    return (left + right) / 2


def find_intervals(dt: float = 0.01) -> list[tuple[float, float]]:
    start = DETONATION_TIME
    end = DETONATION_TIME + SMOKE_EFFECTIVE_SECONDS
    times = np.arange(start, end + dt, dt)
    states = [is_effective(float(t)) for t in times]

    intervals: list[tuple[float, float]] = []
    current_start: float | None = None
    for idx, state in enumerate(states):
        t = float(times[idx])
        if state and current_start is None:
            if idx == 0:
                current_start = t
            else:
                current_start = refine_crossing(float(times[idx - 1]), t)
        if not state and current_start is not None:
            intervals.append((current_start, refine_crossing(float(times[idx - 1]), t)))
            current_start = None
    if current_start is not None:
        intervals.append((current_start, end))
    return intervals


def min_distance_in_interval(start: float, end: float) -> float:
    times = np.linspace(start, end, 2001)
    distances = [distance_margin(float(t))[1] for t in times]
    return float(min(distances))


def write_tables(intervals: list[tuple[float, float]]) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    key_points = [
        ("release_point", RELEASE_TIME, *uav_position(RELEASE_TIME)),
        ("detonation_point", DETONATION_TIME, *DETONATION_POINT),
    ]
    with (TABLE_DIR / "tab_q1_key_points.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["point", "time_s", "x_m", "y_m", "z_m"])
        for row in key_points:
            writer.writerow([row[0], f"{row[1]:.6f}", f"{row[2]:.6f}", f"{row[3]:.6f}", f"{row[4]:.6f}"])

    with (TABLE_DIR / "tab_q1_intervals.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "method",
                "target_point",
                "start_s",
                "end_s",
                "duration_s",
                "min_distance_m",
                "threshold_m",
            ]
        )
        for start, end in intervals:
            writer.writerow(
                [
                    "target-axis midpoint line-of-sight",
                    "(0, 200, 5)",
                    f"{start:.6f}",
                    f"{end:.6f}",
                    f"{end - start:.6f}",
                    f"{min_distance_in_interval(start, end):.6f}",
                    f"{SMOKE_RADIUS:.6f}",
                ]
            )


def write_model_flow(intervals: list[tuple[float, float]]) -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    start, end = intervals[0]

    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=180)
    ax.axis("off")
    y = 0.55
    events = [
        (0.0, "发现目标\n受领任务"),
        (RELEASE_TIME, "投放烟幕弹\n1.5 s"),
        (DETONATION_TIME, "烟幕弹起爆\n5.1 s"),
        (start, "有效遮蔽开始"),
        (end, "有效遮蔽结束"),
    ]
    x_min, x_max = -1.0, end + 1.2

    ax.annotate(
        "",
        xy=(x_max, y),
        xytext=(x_min, y),
        arrowprops={"arrowstyle": "->", "linewidth": 2.2, "color": "#1f4e79"},
    )
    ax.plot([start, end], [y, y], color="#70ad47", linewidth=12, alpha=0.35, solid_capstyle="round")
    ax.text((start + end) / 2, y + 0.18, "有效遮蔽区间", ha="center", va="bottom", color="#548235", weight="bold")

    for idx, (time, label) in enumerate(events):
        ax.scatter([time], [y], s=70, color="#c00000" if idx >= 3 else "#2f5597", zorder=3)
        offset = 0.28 if idx % 2 == 0 else -0.33
        va = "bottom" if offset > 0 else "top"
        ax.plot([time, time], [y, y + offset * 0.74], color="#808080", linewidth=1.0)
        ax.text(time, y + offset, label, ha="center", va=va, fontsize=14)

    ax.text(
        0.02,
        0.08,
        "判定逻辑：烟幕云团中心到 M1-真目标轴中点视线线段的距离不超过 10 m，且垂足在线段内部。",
        transform=ax.transAxes,
        fontsize=14,
        ha="left",
        va="center",
        bbox={"boxstyle": "round,pad=0.45", "facecolor": "#f2f7fb", "edgecolor": "#9dc3e6"},
    )
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.12, 1.14)
    ax.set_title("问题一：给定投放方案的时序与遮蔽判定示意")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_model_flow.png", bbox_inches="tight")
    plt.close(fig)


def write_figure(intervals: list[tuple[float, float]]) -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    times = np.linspace(DETONATION_TIME, DETONATION_TIME + SMOKE_EFFECTIVE_SECONDS, 1200)
    distances = np.array([distance_margin(float(t))[1] for t in times])
    missile_points = np.array([missile_position(float(t)) for t in times])
    smoke_points = np.array([smoke_center(float(t)) for t in times])

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), dpi=180)

    axes[0].plot(times, distances, color="#2f5597", linewidth=1.8, label="到代表视线的距离")
    axes[0].axhline(SMOKE_RADIUS, color="#c00000", linestyle="--", linewidth=1.2, label="有效半径 10 m")
    for start, end in intervals:
        axes[0].axvspan(start, end, color="#92d050", alpha=0.25)
    axes[0].set_xlabel("时间 / s")
    axes[0].set_ylabel("距离 / m")
    axes[0].set_title("问题一：有效遮蔽区间")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.25)

    axes[1].plot(missile_points[:, 0], missile_points[:, 2], color="#7030a0", linewidth=1.5, label="M1 轨迹")
    axes[1].plot(smoke_points[:, 0], smoke_points[:, 2], color="#548235", linewidth=1.5, label="烟幕云团中心")
    axes[1].scatter([TRUE_TARGET_AXIS_MIDPOINT[0]], [TRUE_TARGET_AXIS_MIDPOINT[2]], color="#c00000", s=28, label="真目标轴中点")
    axes[1].scatter([DETONATION_POINT[0]], [DETONATION_POINT[2]], color="#548235", s=28, marker="x", label="起爆点")
    axes[1].set_xlabel("x 坐标 / m")
    axes[1].set_ylabel("z 坐标 / m")
    axes[1].set_title("侧视几何关系")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_distance_geometry.png", bbox_inches="tight")
    plt.close(fig)


def write_validation_figure(intervals: list[tuple[float, float]]) -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    times = np.linspace(DETONATION_TIME, DETONATION_TIME + SMOKE_EFFECTIVE_SECONDS, 1200)
    margins = []
    projections = []
    for t in times:
        margin, _, projection = distance_margin(float(t))
        margins.append(margin)
        projections.append(projection)
    margins_arr = np.array(margins)
    projections_arr = np.array(projections)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6.2), dpi=180, sharex=True)

    axes[0].plot(times, margins_arr, color="#2f5597", linewidth=1.8, label="距离裕度")
    axes[0].axhline(0, color="#c00000", linestyle="--", linewidth=1.3, label="有效边界")
    for start, end in intervals:
        axes[0].axvspan(start, end, color="#92d050", alpha=0.25)
    axes[0].set_ylabel("距离裕度 / m")
    axes[0].set_title("问题一：遮蔽判据验证")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.25)

    axes[1].plot(times, projections_arr, color="#548235", linewidth=1.8, label="垂足位置参数")
    axes[1].axhspan(0, 1, color="#d9ead3", alpha=0.45, label="线段内部")
    for start, end in intervals:
        axes[1].axvspan(start, end, color="#92d050", alpha=0.18)
    axes[1].set_xlabel("时间 / s")
    axes[1].set_ylabel("投影参数")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_validation_margin.png", bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    intervals = find_intervals()
    write_tables(intervals)
    write_model_flow(intervals)
    write_figure(intervals)
    write_validation_figure(intervals)

    total_duration = sum(end - start for start, end in intervals)
    print(f"release_point={uav_position(RELEASE_TIME)}")
    print(f"detonation_point={DETONATION_POINT}")
    print(f"intervals={intervals}")
    print(f"total_effective_duration_s={total_duration:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
