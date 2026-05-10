#!/usr/bin/env python3
"""Solve CUMCM 2025 A Q2 with deterministic search.

This demo maximizes the effective shielding time for one FY1 smoke bomb under
the same target-axis midpoint line-of-sight criterion used in Q1. It is a
traceable example, not an official answer.
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
SMOKE_SINK_SPEED = 3.0
SMOKE_RADIUS = 10.0
SMOKE_EFFECTIVE_SECONDS = 20.0
MIN_UAV_SPEED = 70.0
MAX_UAV_SPEED = 140.0

MISSILE_M1_0 = np.array([20000.0, 0.0, 2000.0])
DECOY = np.array([0.0, 0.0, 0.0])
TRUE_TARGET_AXIS_MIDPOINT = np.array([0.0, 200.0, 5.0])
FY1_0 = np.array([17800.0, 0.0, 1800.0])
MISSILE_DIRECTION = (DECOY - MISSILE_M1_0) / np.linalg.norm(DECOY - MISSILE_M1_0)
MISSILE_IMPACT_TIME = float(np.linalg.norm(DECOY - MISSILE_M1_0) / MISSILE_SPEED)


def missile_position(t: np.ndarray | float) -> np.ndarray:
    t_arr = np.asarray(t, dtype=float)
    return MISSILE_M1_0 + MISSILE_SPEED * t_arr[..., None] * MISSILE_DIRECTION


def decision_geometry(decision: np.ndarray) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    speed, heading, release_time, fuse_delay = decision
    direction = np.array([np.cos(heading), np.sin(heading), 0.0])
    detonation_time = release_time + fuse_delay
    release_point = FY1_0 + speed * release_time * direction
    detonation_point = (
        FY1_0
        + speed * detonation_time * direction
        + np.array([0.0, 0.0, -0.5 * G * fuse_delay * fuse_delay])
    )
    return detonation_time, direction, release_point, detonation_point


def distance_to_segment(points: np.ndarray, starts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    segment = TRUE_TARGET_AXIS_MIDPOINT - starts
    length_sq = np.sum(segment * segment, axis=-1)
    projection = np.sum((points - starts) * segment, axis=-1) / length_sq
    nearest = starts + np.clip(projection, 0.0, 1.0)[..., None] * segment
    distance = np.linalg.norm(points - nearest, axis=-1)
    return distance, projection


def score_batch(decisions: np.ndarray, dt: float) -> np.ndarray:
    rel_times = np.arange(0.0, SMOKE_EFFECTIVE_SECONDS + dt, dt)
    speed = decisions[:, 0]
    heading = decisions[:, 1]
    release_time = decisions[:, 2]
    fuse_delay = decisions[:, 3]
    detonation_time = release_time + fuse_delay
    direction = np.column_stack([np.cos(heading), np.sin(heading), np.zeros_like(heading)])
    detonation_point = (
        FY1_0
        + speed[:, None] * detonation_time[:, None] * direction
        + np.column_stack([np.zeros_like(fuse_delay), np.zeros_like(fuse_delay), -0.5 * G * fuse_delay * fuse_delay])
    )

    valid = (
        (speed >= MIN_UAV_SPEED)
        & (speed <= MAX_UAV_SPEED)
        & (release_time >= 0)
        & (fuse_delay > 0)
        & (detonation_time < MISSILE_IMPACT_TIME)
        & (detonation_point[:, 2] > 0)
    )

    times = detonation_time[:, None] + rel_times[None, :]
    smoke_points = detonation_point[:, None, :] + np.stack(
        [
            np.zeros_like(times),
            np.zeros_like(times),
            -SMOKE_SINK_SPEED * rel_times[None, :].repeat(len(decisions), axis=0),
        ],
        axis=-1,
    )
    missile_points = missile_position(times)
    distance, projection = distance_to_segment(smoke_points, missile_points)
    effective = (
        valid[:, None]
        & (times <= MISSILE_IMPACT_TIME)
        & (distance <= SMOKE_RADIUS)
        & (projection >= 0)
        & (projection <= 1)
    )
    return effective.sum(axis=1) * dt


def generate_candidates(rng: np.random.Generator, n: int) -> np.ndarray:
    candidates = np.empty((n, 4), dtype=float)
    candidates[:, 0] = rng.uniform(MIN_UAV_SPEED, MAX_UAV_SPEED, n)
    candidates[:, 1] = rng.uniform(np.pi - 0.5, np.pi + 0.5, n)
    candidates[:, 2] = rng.uniform(0.0, 8.0, n)
    candidates[:, 3] = rng.uniform(0.3, 9.0, n)
    return candidates


def local_candidates(rng: np.random.Generator, center: np.ndarray, scale: np.ndarray, n: int) -> np.ndarray:
    candidates = rng.normal(center, scale, size=(n, 4))
    candidates[:, 0] = np.clip(candidates[:, 0], MIN_UAV_SPEED, MAX_UAV_SPEED)
    candidates[:, 1] = np.clip(candidates[:, 1], np.pi - 0.7, np.pi + 0.7)
    candidates[:, 2] = np.clip(candidates[:, 2], 0.0, 12.0)
    candidates[:, 3] = np.clip(candidates[:, 3], 0.1, 12.0)
    return candidates


def search_best() -> tuple[np.ndarray, float]:
    rng = np.random.default_rng(20260510)
    best_decision = np.array([120.0, np.pi, 1.5, 3.6], dtype=float)
    best_score = score_batch(best_decision[None, :], dt=0.1)[0]

    # A broad deterministic search gives the local stage a problem-specific basin.
    for _ in range(6):
        candidates = generate_candidates(rng, 6000)
        scores = score_batch(candidates, dt=0.1)
        idx = int(np.argmax(scores))
        if scores[idx] > best_score:
            best_score = float(scores[idx])
            best_decision = candidates[idx].copy()

    scale = np.array([12.0, 0.18, 2.0, 1.5])
    for _ in range(8):
        candidates = local_candidates(rng, best_decision, scale, 6000)
        scores = score_batch(candidates, dt=0.04)
        idx = int(np.argmax(scores))
        if scores[idx] >= best_score:
            best_score = float(scores[idx])
            best_decision = candidates[idx].copy()
        scale *= np.array([0.55, 0.55, 0.55, 0.55])

    # Final tiny search around the best point, including the release-at-once boundary.
    best_decision[2] = max(0.0, best_decision[2])
    scale = np.array([0.6, 0.01, 0.05, 0.08])
    for _ in range(5):
        candidates = local_candidates(rng, best_decision, scale, 8000)
        candidates[:1000, 2] = 0.0
        scores = score_batch(candidates, dt=0.02)
        idx = int(np.argmax(scores))
        if scores[idx] >= best_score:
            best_score = float(scores[idx])
            best_decision = candidates[idx].copy()
        scale *= np.array([0.55, 0.55, 0.55, 0.55])

    return best_decision, best_score


def is_effective(decision: np.ndarray, t: float) -> bool:
    detonation_time, _, _, detonation_point = decision_geometry(decision)
    if t < detonation_time or t > detonation_time + SMOKE_EFFECTIVE_SECONDS or t > MISSILE_IMPACT_TIME:
        return False
    if detonation_point[2] <= 0:
        return False
    smoke_point = detonation_point + np.array([0.0, 0.0, -SMOKE_SINK_SPEED * (t - detonation_time)])
    distance, projection = distance_to_segment(smoke_point[None, :], missile_position(np.array([t])))
    return bool(distance[0] <= SMOKE_RADIUS and 0 <= projection[0] <= 1)


def refine_crossing(decision: np.ndarray, left: float, right: float) -> float:
    left_effective = is_effective(decision, left)
    for _ in range(80):
        mid = (left + right) / 2
        if is_effective(decision, mid) == left_effective:
            left = mid
        else:
            right = mid
    return (left + right) / 2


def find_intervals(decision: np.ndarray, dt: float = 0.005) -> list[tuple[float, float]]:
    detonation_time, _, _, _ = decision_geometry(decision)
    end = min(detonation_time + SMOKE_EFFECTIVE_SECONDS, MISSILE_IMPACT_TIME)
    times = np.arange(detonation_time, end + dt, dt)
    states = [is_effective(decision, float(t)) for t in times]

    intervals: list[tuple[float, float]] = []
    current_start: float | None = None
    for idx, state in enumerate(states):
        t = float(times[idx])
        if state and current_start is None:
            current_start = t if idx == 0 else refine_crossing(decision, float(times[idx - 1]), t)
        if not state and current_start is not None:
            intervals.append((current_start, refine_crossing(decision, float(times[idx - 1]), t)))
            current_start = None
    if current_start is not None:
        intervals.append((current_start, end))
    return intervals


def min_distance_in_interval(decision: np.ndarray, start: float, end: float) -> float:
    times = np.linspace(start, end, 2001)
    detonation_time, _, _, detonation_point = decision_geometry(decision)
    smoke_points = detonation_point + np.column_stack(
        [np.zeros_like(times), np.zeros_like(times), -SMOKE_SINK_SPEED * (times - detonation_time)]
    )
    distance, _ = distance_to_segment(smoke_points, missile_position(times))
    return float(np.min(distance))


def write_tables(decision: np.ndarray, intervals: list[tuple[float, float]]) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    speed, heading, release_time, fuse_delay = decision
    detonation_time, direction, release_point, detonation_point = decision_geometry(decision)
    heading_deg = (np.degrees(heading) + 360.0) % 360.0
    total_duration = sum(end - start for start, end in intervals)

    with (TABLE_DIR / "tab_q2_strategy.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "uav",
                "speed_m_s",
                "heading_rad",
                "heading_deg_from_positive_x",
                "direction_x",
                "direction_y",
                "release_time_s",
                "fuse_delay_s",
                "detonation_time_s",
                "release_x_m",
                "release_y_m",
                "release_z_m",
                "detonation_x_m",
                "detonation_y_m",
                "detonation_z_m",
                "total_duration_s",
                "method",
            ]
        )
        writer.writerow(
            [
                "FY1",
                f"{speed:.6f}",
                f"{heading:.9f}",
                f"{heading_deg:.6f}",
                f"{direction[0]:.9f}",
                f"{direction[1]:.9f}",
                f"{release_time:.6f}",
                f"{fuse_delay:.6f}",
                f"{detonation_time:.6f}",
                f"{release_point[0]:.6f}",
                f"{release_point[1]:.6f}",
                f"{release_point[2]:.6f}",
                f"{detonation_point[0]:.6f}",
                f"{detonation_point[1]:.6f}",
                f"{detonation_point[2]:.6f}",
                f"{total_duration:.6f}",
                "deterministic coarse-to-fine search",
            ]
        )

    with (TABLE_DIR / "tab_q2_intervals.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["target_point", "start_s", "end_s", "duration_s", "min_distance_m", "threshold_m"])
        for start, end in intervals:
            writer.writerow(
                [
                    "(0, 200, 5)",
                    f"{start:.6f}",
                    f"{end:.6f}",
                    f"{end - start:.6f}",
                    f"{min_distance_in_interval(decision, start, end):.6f}",
                    f"{SMOKE_RADIUS:.6f}",
                ]
            )


def write_model_schematic(decision: np.ndarray, intervals: list[tuple[float, float]]) -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    speed, heading, release_time, fuse_delay = decision
    detonation_time, direction, release_point, detonation_point = decision_geometry(decision)
    start, end = intervals[0]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), dpi=180)

    ax = axes[0]
    ax.axis("off")
    boxes = [
        (0.08, 0.78, "决策变量", f"速度 v={speed:.2f} m/s\n航向角 θ={np.degrees(heading):.2f}°"),
        (0.08, 0.48, "投放时序", f"投放 t_r={release_time:.3f} s\n延迟 τ={fuse_delay:.3f} s"),
        (0.08, 0.18, "优化目标", "最大化有效遮蔽时长\n满足 70≤v≤140 m/s"),
        (0.58, 0.64, "投放点", f"({release_point[0]:.1f}, {release_point[1]:.1f}, {release_point[2]:.1f})"),
        (0.58, 0.34, "起爆点", f"({detonation_point[0]:.1f}, {detonation_point[1]:.1f}, {detonation_point[2]:.1f})"),
    ]
    for x, y, title, body in boxes:
        ax.text(
            x,
            y,
            f"{title}\n{body}",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=13,
            bbox={"boxstyle": "round,pad=0.45", "facecolor": "#f8fbff", "edgecolor": "#5b9bd5"},
        )
    for y1, y2 in [(0.78, 0.64), (0.48, 0.34), (0.18, 0.34)]:
        ax.annotate(
            "",
            xy=(0.56, y2),
            xytext=(0.42, y1),
            xycoords="axes fraction",
            arrowprops={"arrowstyle": "->", "linewidth": 1.6, "color": "#1f4e79"},
        )
    ax.set_title("问题二：优化变量与投放策略示意")

    ax = axes[1]
    ax.annotate(
        "",
        xy=(end + 0.8, 0.5),
        xytext=(0.0, 0.5),
        arrowprops={"arrowstyle": "->", "linewidth": 2.2, "color": "#1f4e79"},
    )
    ax.plot([start, end], [0.5, 0.5], color="#70ad47", linewidth=13, alpha=0.35, solid_capstyle="round")
    timeline = [
        (release_time, "投放"),
        (detonation_time, "起爆"),
        (start, "遮蔽开始"),
        (end, "遮蔽结束"),
    ]
    for idx, (time, label) in enumerate(timeline):
        ax.scatter([time], [0.5], s=72, color="#c00000" if idx >= 2 else "#2f5597", zorder=3)
        offset = 0.22 if idx % 2 == 0 else -0.24
        va = "bottom" if offset > 0 else "top"
        ax.plot([time, time], [0.5, 0.5 + offset * 0.7], color="#808080", linewidth=1.0)
        ax.text(time, 0.5 + offset, f"{label}\n{time:.3f} s", ha="center", va=va, fontsize=13)
    ax.text((start + end) / 2, 0.72, f"有效遮蔽 {end - start:.3f} s", ha="center", color="#548235", weight="bold")
    ax.set_xlim(0, end + 0.9)
    ax.set_ylim(0.05, 0.98)
    ax.set_yticks([])
    ax.set_xlabel("时间 / s")
    ax.set_title("问题二：投放、起爆与遮蔽时序")
    ax.grid(axis="x", alpha=0.22)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_model_schematic.png", bbox_inches="tight")
    plt.close(fig)


def write_figure(decision: np.ndarray, intervals: list[tuple[float, float]]) -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    detonation_time, _, _, detonation_point = decision_geometry(decision)
    end = min(detonation_time + SMOKE_EFFECTIVE_SECONDS, MISSILE_IMPACT_TIME)
    times = np.linspace(detonation_time, end, 1200)
    smoke_points = detonation_point + np.column_stack(
        [np.zeros_like(times), np.zeros_like(times), -SMOKE_SINK_SPEED * (times - detonation_time)]
    )
    distance, _ = distance_to_segment(smoke_points, missile_position(times))
    missile_points = missile_position(times)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), dpi=180)
    axes[0].plot(times, distance, color="#2f5597", linewidth=1.8, label="到代表视线的距离")
    axes[0].axhline(SMOKE_RADIUS, color="#c00000", linestyle="--", linewidth=1.2, label="有效半径 10 m")
    for start, stop in intervals:
        axes[0].axvspan(start, stop, color="#92d050", alpha=0.25)
    axes[0].set_xlabel("时间 / s")
    axes[0].set_ylabel("距离 / m")
    axes[0].set_title("问题二：搜索得到的遮蔽区间")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.25)

    axes[1].plot(missile_points[:, 0], missile_points[:, 2], color="#7030a0", linewidth=1.5, label="M1 轨迹")
    axes[1].plot(smoke_points[:, 0], smoke_points[:, 2], color="#548235", linewidth=1.5, label="烟幕云团中心")
    axes[1].scatter([TRUE_TARGET_AXIS_MIDPOINT[0]], [TRUE_TARGET_AXIS_MIDPOINT[2]], color="#c00000", s=28, label="真目标轴中点")
    axes[1].scatter([detonation_point[0]], [detonation_point[2]], color="#548235", s=28, marker="x", label="起爆点")
    axes[1].set_xlabel("x 坐标 / m")
    axes[1].set_ylabel("z 坐标 / m")
    axes[1].set_title("侧视几何关系")
    axes[1].legend(frameon=False)
    axes[1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_optimized_distance_geometry.png", bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    decision, coarse_score = search_best()
    intervals = find_intervals(decision)
    write_tables(decision, intervals)
    write_model_schematic(decision, intervals)
    write_figure(decision, intervals)
    total_duration = sum(end - start for start, end in intervals)
    detonation_time, _, release_point, detonation_point = decision_geometry(decision)

    print(f"coarse_score_s={coarse_score:.6f}")
    print(f"decision_speed_heading_release_fuse={decision}")
    print(f"release_point={release_point}")
    print(f"detonation_time={detonation_time:.6f}")
    print(f"detonation_point={detonation_point}")
    print(f"intervals={intervals}")
    print(f"total_effective_duration_s={total_duration:.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
