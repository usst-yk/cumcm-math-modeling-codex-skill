#!/usr/bin/env python3
"""Solve CUMCM 2025 A Q3-Q5 as reproducible benchmark examples.

The benchmark keeps the same representative line-of-sight criterion used by
Q1/Q2: a smoke cloud is effective when its center is within 10 m of the segment
from a missile to the true target axis midpoint (0, 200, 5), and the projection
lies inside that segment. The solutions are deterministic best-found benchmark
strategies, not official global optima.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plot_utils import setup_chinese_plot


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "tables"
FIGURE_DIR = ROOT / "figures"
RAW_DIR = ROOT / "data" / "raw"

G = 9.8
MISSILE_SPEED = 300.0
SMOKE_SINK_SPEED = 3.0
SMOKE_RADIUS = 10.0
SMOKE_EFFECTIVE_SECONDS = 20.0
MIN_UAV_SPEED = 70.0
MAX_UAV_SPEED = 140.0
MIN_RELEASE_GAP = 1.0

DECOY = np.array([0.0, 0.0, 0.0])
TRUE_TARGET_AXIS_MIDPOINT = np.array([0.0, 200.0, 5.0])

MISSILES = {
    "M1": np.array([20000.0, 0.0, 2000.0]),
    "M2": np.array([19000.0, 600.0, 2100.0]),
    "M3": np.array([18000.0, -600.0, 1900.0]),
}

UAVS = {
    "FY1": np.array([17800.0, 0.0, 1800.0]),
    "FY2": np.array([12000.0, 1400.0, 1400.0]),
    "FY3": np.array([6000.0, -3000.0, 700.0]),
    "FY4": np.array([11000.0, 2000.0, 1800.0]),
    "FY5": np.array([13000.0, -2000.0, 1300.0]),
}

MISSILE_DIR = {key: (DECOY - pos) / np.linalg.norm(DECOY - pos) for key, pos in MISSILES.items()}
MISSILE_IMPACT = {key: float(np.linalg.norm(pos - DECOY) / MISSILE_SPEED) for key, pos in MISSILES.items()}


@dataclass
class BombDecision:
    question: str
    uav: str
    bomb_id: int
    missile: str
    speed: float
    heading: float
    release_time: float
    fuse_delay: float

    @property
    def detonation_time(self) -> float:
        return self.release_time + self.fuse_delay

    @property
    def direction(self) -> np.ndarray:
        return np.array([np.cos(self.heading), np.sin(self.heading), 0.0])

    @property
    def heading_deg(self) -> float:
        return float((np.degrees(self.heading) + 360.0) % 360.0)

    @property
    def release_point(self) -> np.ndarray:
        return UAVS[self.uav] + self.speed * self.release_time * self.direction

    @property
    def detonation_point(self) -> np.ndarray:
        return (
            UAVS[self.uav]
            + self.speed * self.detonation_time * self.direction
            + np.array([0.0, 0.0, -0.5 * G * self.fuse_delay * self.fuse_delay])
        )


def missile_position(missile: str, t: np.ndarray | float) -> np.ndarray:
    t_arr = np.asarray(t, dtype=float)
    return MISSILES[missile] + MISSILE_SPEED * t_arr[..., None] * MISSILE_DIR[missile]


def distance_to_segment(points: np.ndarray, starts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    segment = TRUE_TARGET_AXIS_MIDPOINT - starts
    length_sq = np.sum(segment * segment, axis=-1)
    projection = np.sum((points - starts) * segment, axis=-1) / length_sq
    nearest = starts + np.clip(projection, 0.0, 1.0)[..., None] * segment
    distance = np.linalg.norm(points - nearest, axis=-1)
    return distance, projection


def effective_mask(decision: BombDecision, times: np.ndarray) -> np.ndarray:
    detonation_point = decision.detonation_point
    valid = (
        detonation_point[2] > 0
        and MIN_UAV_SPEED <= decision.speed <= MAX_UAV_SPEED
        and decision.release_time >= 0
        and decision.fuse_delay > 0
        and decision.detonation_time < MISSILE_IMPACT[decision.missile]
    )
    if not valid:
        return np.zeros_like(times, dtype=bool)

    active = (
        (times >= decision.detonation_time)
        & (times <= decision.detonation_time + SMOKE_EFFECTIVE_SECONDS)
        & (times <= MISSILE_IMPACT[decision.missile])
    )
    mask = np.zeros_like(times, dtype=bool)
    if not np.any(active):
        return mask
    active_times = times[active]
    smoke_points = detonation_point + np.column_stack(
        [
            np.zeros_like(active_times),
            np.zeros_like(active_times),
            -SMOKE_SINK_SPEED * (active_times - decision.detonation_time),
        ]
    )
    distance, projection = distance_to_segment(smoke_points, missile_position(decision.missile, active_times))
    mask[active] = (distance <= SMOKE_RADIUS) & (projection >= 0.0) & (projection <= 1.0)
    return mask


def batch_effective_mask(
    uav: str,
    missile: str,
    candidates: np.ndarray,
    times: np.ndarray,
) -> np.ndarray:
    speed = candidates[:, 0]
    heading = candidates[:, 1]
    release_time = candidates[:, 2]
    fuse_delay = candidates[:, 3]
    detonation_time = release_time + fuse_delay
    direction = np.column_stack([np.cos(heading), np.sin(heading), np.zeros_like(heading)])
    detonation_points = (
        UAVS[uav]
        + speed[:, None] * detonation_time[:, None] * direction
        + np.column_stack([np.zeros_like(fuse_delay), np.zeros_like(fuse_delay), -0.5 * G * fuse_delay * fuse_delay])
    )
    valid = (
        (speed >= MIN_UAV_SPEED)
        & (speed <= MAX_UAV_SPEED)
        & (release_time >= 0.0)
        & (fuse_delay > 0.0)
        & (detonation_time < MISSILE_IMPACT[missile])
        & (detonation_points[:, 2] > 0.0)
    )

    rel_times = times[None, :] - detonation_time[:, None]
    active = valid[:, None] & (rel_times >= 0.0) & (rel_times <= SMOKE_EFFECTIVE_SECONDS) & (
        times[None, :] <= MISSILE_IMPACT[missile]
    )
    smoke_points = detonation_points[:, None, :] + np.stack(
        [
            np.zeros_like(rel_times),
            np.zeros_like(rel_times),
            -SMOKE_SINK_SPEED * rel_times,
        ],
        axis=-1,
    )
    missile_points = missile_position(missile, times)[None, :, :]
    distance, projection = distance_to_segment(smoke_points, missile_points)
    return active & (distance <= SMOKE_RADIUS) & (projection >= 0.0) & (projection <= 1.0)


def time_grid(dt: float) -> dict[str, np.ndarray]:
    return {key: np.arange(0.0, impact + dt, dt) for key, impact in MISSILE_IMPACT.items()}


def generate_candidates(
    rng: np.random.Generator,
    uav: str,
    missile: str,
    n: int,
    fixed_config: tuple[float, float] | None = None,
    existing_releases: list[float] | None = None,
    center: np.ndarray | None = None,
    scale: np.ndarray | None = None,
) -> np.ndarray:
    candidates = np.empty((n, 4), dtype=float)
    if center is None:
        target_heading = np.arctan2(TRUE_TARGET_AXIS_MIDPOINT[1] - UAVS[uav][1], TRUE_TARGET_AXIS_MIDPOINT[0] - UAVS[uav][0])
        candidates[:, 0] = rng.uniform(MIN_UAV_SPEED, MAX_UAV_SPEED, n)
        candidates[:, 1] = rng.uniform(target_heading - 0.85, target_heading + 0.85, n)
        candidates[:, 2] = rng.uniform(0.0, min(24.0, MISSILE_IMPACT[missile] - 1.0), n)
        candidates[:, 3] = rng.uniform(0.2, 12.0, n)
    else:
        candidates = rng.normal(center, scale, size=(n, 4))
        candidates[:, 0] = np.clip(candidates[:, 0], MIN_UAV_SPEED, MAX_UAV_SPEED)
        candidates[:, 1] = np.clip(candidates[:, 1], center[1] - 0.25, center[1] + 0.25)
        candidates[:, 2] = np.clip(candidates[:, 2], 0.0, min(28.0, MISSILE_IMPACT[missile] - 0.5))
        candidates[:, 3] = np.clip(candidates[:, 3], 0.15, 14.0)

    if fixed_config is not None:
        candidates[:, 0] = fixed_config[0]
        candidates[:, 1] = fixed_config[1]

    if existing_releases:
        release = candidates[:, 2]
        ok = np.ones(n, dtype=bool)
        for old in existing_releases:
            ok &= np.abs(release - old) >= MIN_RELEASE_GAP
        if not np.all(ok):
            replacement = rng.uniform(0.0, min(28.0, MISSILE_IMPACT[missile] - 0.5), n)
            for old in existing_releases:
                too_close = np.abs(replacement - old) < MIN_RELEASE_GAP
                replacement[too_close] = np.clip(old + MIN_RELEASE_GAP + rng.uniform(0.0, 4.0, too_close.sum()), 0.0, 28.0)
            candidates[~ok, 2] = replacement[~ok]
    return candidates


def best_candidate(
    rng: np.random.Generator,
    uav: str,
    missile: str,
    coverage: dict[str, np.ndarray],
    grids: dict[str, np.ndarray],
    fixed_config: tuple[float, float] | None = None,
    existing_releases: list[float] | None = None,
    broad_n: int = 4000,
    local_n: int = 5000,
) -> BombDecision:
    times = grids[missile]
    best_vec: np.ndarray | None = None
    best_score = -1.0

    for _ in range(4):
        candidates = generate_candidates(rng, uav, missile, broad_n, fixed_config, existing_releases)
        masks = batch_effective_mask(uav, missile, candidates, times)
        scores = np.sum(masks & ~coverage[missile][None, :], axis=1)
        idx = int(np.argmax(scores))
        if scores[idx] > best_score:
            best_score = float(scores[idx])
            best_vec = candidates[idx].copy()

    assert best_vec is not None
    scale = np.array([10.0, 0.12, 1.6, 1.0])
    for _ in range(6):
        candidates = generate_candidates(
            rng,
            uav,
            missile,
            local_n,
            fixed_config,
            existing_releases,
            center=best_vec,
            scale=scale,
        )
        masks = batch_effective_mask(uav, missile, candidates, times)
        scores = np.sum(masks & ~coverage[missile][None, :], axis=1)
        idx = int(np.argmax(scores))
        if scores[idx] >= best_score:
            best_score = float(scores[idx])
            best_vec = candidates[idx].copy()
        scale *= np.array([0.55, 0.55, 0.55, 0.55])

    return BombDecision(
        question="",
        uav=uav,
        bomb_id=0,
        missile=missile,
        speed=float(best_vec[0]),
        heading=float(best_vec[1]),
        release_time=float(best_vec[2]),
        fuse_delay=float(best_vec[3]),
    )


def masks_by_missile(decisions: list[BombDecision], dt: float = 0.02) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    grids = time_grid(dt)
    coverage = {key: np.zeros_like(times, dtype=bool) for key, times in grids.items()}
    for decision in decisions:
        coverage[decision.missile] |= effective_mask(decision, grids[decision.missile])
    return coverage, grids


def intervals_from_mask(times: np.ndarray, mask: np.ndarray) -> list[tuple[float, float]]:
    intervals: list[tuple[float, float]] = []
    if len(times) == 0:
        return intervals
    current: float | None = None
    dt = float(times[1] - times[0]) if len(times) > 1 else 0.0
    for t, state in zip(times, mask):
        if state and current is None:
            current = float(t)
        if not state and current is not None:
            intervals.append((current, float(t - dt)))
            current = None
    if current is not None:
        intervals.append((current, float(times[-1])))
    return intervals


def score_decisions(decisions: list[BombDecision], dt: float = 0.02) -> dict[str, float]:
    coverage, grids = masks_by_missile(decisions, dt=dt)
    return {missile: float(mask.sum() * (grids[missile][1] - grids[missile][0])) for missile, mask in coverage.items()}


def individual_duration(decision: BombDecision, dt: float = 0.02) -> float:
    times = time_grid(dt)[decision.missile]
    mask = effective_mask(decision, times)
    return float(mask.sum() * dt)


def solve_q3(rng: np.random.Generator) -> list[BombDecision]:
    grids = time_grid(0.08)
    coverage = {key: np.zeros_like(times, dtype=bool) for key, times in grids.items()}

    first = best_candidate(rng, "FY1", "M1", coverage, grids, broad_n=6000, local_n=7000)
    fixed = (first.speed, first.heading)
    decisions = [first]
    coverage["M1"] |= effective_mask(first, grids["M1"])

    for _ in range(2):
        candidate = best_candidate(
            rng,
            "FY1",
            "M1",
            coverage,
            grids,
            fixed_config=fixed,
            existing_releases=[item.release_time for item in decisions],
            broad_n=7000,
            local_n=8000,
        )
        decisions.append(candidate)
        coverage["M1"] |= effective_mask(candidate, grids["M1"])

    decisions.sort(key=lambda item: item.release_time)
    for idx, decision in enumerate(decisions, start=1):
        decision.question = "Q3"
        decision.bomb_id = idx
    return decisions


def solve_q4(rng: np.random.Generator) -> list[BombDecision]:
    grids = time_grid(0.08)
    coverage = {key: np.zeros_like(times, dtype=bool) for key, times in grids.items()}
    decisions: list[BombDecision] = []
    for idx, uav in enumerate(["FY1", "FY2", "FY3"], start=1):
        candidate = best_candidate(rng, uav, "M1", coverage, grids, broad_n=6500, local_n=7500)
        candidate.question = "Q4"
        candidate.bomb_id = idx
        decisions.append(candidate)
        coverage["M1"] |= effective_mask(candidate, grids["M1"])
    return decisions


def solve_q5(rng: np.random.Generator) -> list[BombDecision]:
    grids = time_grid(0.12)
    coverage = {key: np.zeros_like(times, dtype=bool) for key, times in grids.items()}
    decisions: list[BombDecision] = []
    uav_configs: dict[str, tuple[float, float]] = {}

    for _ in range(15):
        best: BombDecision | None = None
        best_gain = -1.0
        for uav in UAVS:
            selected = [item for item in decisions if item.uav == uav]
            if len(selected) >= 3:
                continue
            existing_releases = [item.release_time for item in selected]
            fixed = uav_configs.get(uav)
            for missile in MISSILES:
                candidate = best_candidate(
                    rng,
                    uav,
                    missile,
                    coverage,
                    grids,
                    fixed_config=fixed,
                    existing_releases=existing_releases,
                    broad_n=1400,
                    local_n=1800,
                )
                mask = effective_mask(candidate, grids[missile])
                gain = float(np.sum(mask & ~coverage[missile]))
                if gain > best_gain:
                    best_gain = gain
                    best = candidate
        if best is None or best_gain <= 1:
            break
        if best.uav not in uav_configs:
            uav_configs[best.uav] = (best.speed, best.heading)
        else:
            best.speed, best.heading = uav_configs[best.uav]
        best.question = "Q5"
        best.bomb_id = len([item for item in decisions if item.uav == best.uav]) + 1
        decisions.append(best)
        coverage[best.missile] |= effective_mask(best, grids[best.missile])

    decisions.sort(key=lambda item: (item.uav, item.bomb_id))
    return decisions


def write_strategy_table(question: str, decisions: list[BombDecision]) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    path = TABLE_DIR / f"tab_{question.lower()}_strategy.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "question",
                "uav",
                "bomb_id",
                "missile",
                "speed_m_s",
                "heading_deg_from_positive_x",
                "heading_rad",
                "release_time_s",
                "fuse_delay_s",
                "detonation_time_s",
                "release_x_m",
                "release_y_m",
                "release_z_m",
                "detonation_x_m",
                "detonation_y_m",
                "detonation_z_m",
                "method",
            ]
        )
        for item in decisions:
            release = item.release_point
            detonation = item.detonation_point
            writer.writerow(
                [
                    item.question,
                    item.uav,
                    item.bomb_id,
                    item.missile,
                    f"{item.speed:.6f}",
                    f"{item.heading_deg:.6f}",
                    f"{item.heading:.9f}",
                    f"{item.release_time:.6f}",
                    f"{item.fuse_delay:.6f}",
                    f"{item.detonation_time:.6f}",
                    f"{release[0]:.6f}",
                    f"{release[1]:.6f}",
                    f"{release[2]:.6f}",
                    f"{detonation[0]:.6f}",
                    f"{detonation[1]:.6f}",
                    f"{detonation[2]:.6f}",
                    "fixed-seed greedy marginal coverage search",
                ]
            )


def write_interval_table(question: str, decisions: list[BombDecision]) -> dict[str, float]:
    coverage, grids = masks_by_missile(decisions, dt=0.02)
    totals: dict[str, float] = {}
    path = TABLE_DIR / f"tab_{question.lower()}_intervals.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["question", "missile", "interval_id", "start_s", "end_s", "duration_s"])
        for missile, times in grids.items():
            if not np.any(coverage[missile]):
                continue
            intervals = intervals_from_mask(times, coverage[missile])
            total = 0.0
            for idx, (start, end) in enumerate(intervals, start=1):
                duration = end - start + 0.02
                total += duration
                writer.writerow([question, missile, idx, f"{start:.6f}", f"{end:.6f}", f"{duration:.6f}"])
            totals[missile] = total
    return totals


def write_result_workbook(question: str, decisions: list[BombDecision], totals: dict[str, float]) -> None:
    if question == "Q3":
        source = RAW_DIR / "result1.xlsx"
        target = TABLE_DIR / "result1_benchmark.xlsx"
        df = pd.read_excel(source).astype(object)
        rows = []
        for item in decisions:
            rows.append(
                {
                    "无人机运动方向": item.heading_deg,
                    "无人机运动速度 (m/s)": item.speed,
                    "烟幕干扰弹编号": item.bomb_id,
                    "烟幕干扰弹投放点的x坐标 (m)": item.release_point[0],
                    "烟幕干扰弹投放点的y坐标 (m)": item.release_point[1],
                    "烟幕干扰弹投放点的z坐标 (m)": item.release_point[2],
                    "烟幕干扰弹起爆点的x坐标 (m)": item.detonation_point[0],
                    "烟幕干扰弹起爆点的y坐标 (m)": item.detonation_point[1],
                    "烟幕干扰弹起爆点的z坐标 (m)": item.detonation_point[2],
                    "有效干扰时长 (s)": individual_duration(item),
                }
            )
        df.iloc[: len(rows), :] = pd.DataFrame(rows, columns=df.columns)
    elif question == "Q4":
        source = RAW_DIR / "result2.xlsx"
        target = TABLE_DIR / "result2_benchmark.xlsx"
        df = pd.read_excel(source).astype(object)
        rows = []
        for item in decisions:
            rows.append(
                {
                    "无人机编号": item.uav,
                    "无人机运动方向": item.heading_deg,
                    "无人机运动速度 (m/s)": item.speed,
                    "烟幕干扰弹投放点的x坐标 (m)": item.release_point[0],
                    "烟幕干扰弹投放点的y坐标 (m)": item.release_point[1],
                    "烟幕干扰弹投放点的z坐标 (m)": item.release_point[2],
                    "烟幕干扰弹起爆点的x坐标 (m)": item.detonation_point[0],
                    "烟幕干扰弹起爆点的y坐标 (m)": item.detonation_point[1],
                    "烟幕干扰弹起爆点的z坐标 (m)": item.detonation_point[2],
                    "有效干扰时长 (s)": individual_duration(item),
                }
            )
        df.iloc[: len(rows), :] = pd.DataFrame(rows, columns=df.columns)
    else:
        source = RAW_DIR / "result3.xlsx"
        target = TABLE_DIR / "result3_benchmark.xlsx"
        df = pd.read_excel(source).astype(object)
        by_slot = {(item.uav, float(item.bomb_id)): item for item in decisions}
        rows = []
        for _, source_row in df.iterrows():
            uav = source_row.get("无人机编号")
            bomb_id = source_row.get("烟幕干扰弹编号")
            item = by_slot.get((uav, bomb_id))
            if item is None:
                rows.append(source_row.to_dict())
                continue
            rows.append(
                {
                    "无人机编号": item.uav,
                    "无人机运动方向": item.heading_deg,
                    "无人机运动速度 (m/s)": item.speed,
                    "烟幕干扰弹编号": item.bomb_id,
                    "烟幕干扰弹投放点的x坐标 (m)": item.release_point[0],
                    "烟幕干扰弹投放点的y坐标 (m)": item.release_point[1],
                    "烟幕干扰弹投放点的z坐标 (m)": item.release_point[2],
                    "烟幕干扰弹起爆点的x坐标 (m)": item.detonation_point[0],
                    "烟幕干扰弹起爆点的y坐标 (m)": item.detonation_point[1],
                    "烟幕干扰弹起爆点的z坐标 (m)": item.detonation_point[2],
                    "有效干扰时长 (s)": individual_duration(item),
                    "干扰的导弹编号": item.missile,
                }
            )
        df = pd.DataFrame(rows, columns=df.columns)
    df = df.fillna("未使用")
    df.to_excel(target, index=False)


def write_schematic(question: str, decisions: list[BombDecision], totals: dict[str, float]) -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), dpi=180)

    ax = axes[0]
    ax.axis("off")
    title = {"Q3": "问题三：同一无人机三弹协同", "Q4": "问题四：三机单弹协同", "Q5": "问题五：多机多弹多导弹协同"}[question]
    ax.set_title(title)
    y_positions = np.linspace(0.82, 0.18, min(len(decisions), 7))
    shown = decisions[:7]
    for y, item in zip(y_positions, shown):
        ax.text(
            0.05,
            y,
            f"{item.uav}-{item.bomb_id} → {item.missile}\n"
            f"v={item.speed:.1f} m/s, θ={item.heading_deg:.1f}°\n"
            f"投放 {item.release_time:.2f}s，起爆 {item.detonation_time:.2f}s",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=11,
            bbox={"boxstyle": "round,pad=0.35", "facecolor": "#f8fbff", "edgecolor": "#5b9bd5"},
        )
    if len(decisions) > len(shown):
        ax.text(0.05, 0.04, f"其余 {len(decisions) - len(shown)} 枚见策略表", transform=ax.transAxes, fontsize=12)

    ax = axes[1]
    for missile, color in zip(["M1", "M2", "M3"], ["#c00000", "#7030a0", "#2f5597"]):
        if missile in totals:
            ax.bar(missile, totals[missile], color=color, alpha=0.78)
            ax.text(missile, totals[missile] + 0.25, f"{totals[missile]:.2f}s", ha="center", va="bottom")
    ax.set_ylabel("有效遮蔽总时长 / s")
    ax.set_title("各导弹遮蔽时长汇总")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"fig_{question.lower()}_model_flow.png", bbox_inches="tight")
    plt.close(fig)


def write_result_figure(question: str, decisions: list[BombDecision], totals: dict[str, float]) -> None:
    setup_chinese_plot()
    coverage, grids = masks_by_missile(decisions, dt=0.05)
    missiles = [key for key in ["M1", "M2", "M3"] if np.any(coverage[key])]
    fig, axes = plt.subplots(len(missiles), 1, figsize=(11, max(3.0, 2.4 * len(missiles))), dpi=180, sharex=False)
    if len(missiles) == 1:
        axes = [axes]
    for ax, missile in zip(axes, missiles):
        times = grids[missile]
        ax.fill_between(times, 0, coverage[missile].astype(float), step="mid", color="#70ad47", alpha=0.45)
        for item in [d for d in decisions if d.missile == missile]:
            ax.axvline(item.detonation_time, color="#2f5597", linestyle=":", linewidth=1.0)
            ax.text(item.detonation_time, 1.05, f"{item.uav}-{item.bomb_id}", rotation=90, va="bottom", ha="center", fontsize=9)
        ax.set_ylim(-0.08, 1.25)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["无", "有"])
        ax.set_ylabel(missile)
        ax.set_title(f"{missile} 的有效遮蔽时间轴，总时长 {totals.get(missile, 0):.2f} s")
        ax.grid(axis="x", alpha=0.25)
    axes[-1].set_xlabel("时间 / s")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"fig_{question.lower()}_result.png", bbox_inches="tight")
    plt.close(fig)


def write_validation_figure(question: str, decisions: list[BombDecision]) -> None:
    setup_chinese_plot()
    rows = []
    for item in decisions:
        rows.append(
            {
                "label": f"{item.uav}-{item.bomb_id}",
                "speed_margin_low": item.speed - MIN_UAV_SPEED,
                "speed_margin_high": MAX_UAV_SPEED - item.speed,
                "detonation_height": item.detonation_point[2],
                "release_time": item.release_time,
            }
        )
    labels = [row["label"] for row in rows]
    x = np.arange(len(labels))

    fig, axes = plt.subplots(2, 1, figsize=(12, 7), dpi=180)
    axes[0].bar(x - 0.18, [row["speed_margin_low"] for row in rows], width=0.36, label="距 70 m/s 裕度")
    axes[0].bar(x + 0.18, [row["speed_margin_high"] for row in rows], width=0.36, label="距 140 m/s 裕度")
    axes[0].set_ylabel("速度约束裕度 / (m/s)")
    axes[0].set_title(f"{question}：速度约束可行性检查")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=45, ha="right")
    axes[0].legend(frameon=False)
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].bar(x, [row["detonation_height"] for row in rows], color="#70ad47", alpha=0.75)
    axes[1].axhline(0, color="#c00000", linewidth=1.2)
    axes[1].set_ylabel("起爆高度 / m")
    axes[1].set_title("起爆点高度检查")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=45, ha="right")
    axes[1].grid(axis="y", alpha=0.25)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / f"fig_{question.lower()}_validation.png", bbox_inches="tight")
    plt.close(fig)


def write_all_outputs(question: str, decisions: list[BombDecision]) -> dict[str, float]:
    write_strategy_table(question, decisions)
    totals = write_interval_table(question, decisions)
    write_result_workbook(question, decisions, totals)
    write_schematic(question, decisions, totals)
    write_result_figure(question, decisions, totals)
    write_validation_figure(question, decisions)
    return totals


def main() -> int:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20260510)

    q3 = solve_q3(rng)
    q3_totals = write_all_outputs("Q3", q3)
    print("Q3", q3_totals)

    q4 = solve_q4(rng)
    q4_totals = write_all_outputs("Q4", q4)
    print("Q4", q4_totals)

    q5 = solve_q5(rng)
    q5_totals = write_all_outputs("Q5", q5)
    print("Q5", q5_totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
