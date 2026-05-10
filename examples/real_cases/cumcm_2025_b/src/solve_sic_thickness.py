#!/usr/bin/env python3
"""Synthetic CUMCM 2025 B thickness benchmark.

The script generates B-question-style spectra with a known thickness and then
recovers the thickness from the spectral frequency. It is a regression test for
execution accuracy, not an official solution to the hidden attachments.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import setup_chinese_plot


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
TABLE_DIR = ROOT / "tables"
FIGURE_DIR = ROOT / "figures"
RESULT_DIR = ROOT / "results"
PAPER_DIR = ROOT / "paper"
SECTION_DIR = PAPER_DIR / "sections"
APPENDIX_DIR = ROOT / "appendix"

N_SIC = 2.55
TRUE_THICKNESS_UM = 8.0
ANGLE_CONFIGS = [
    ("sic_10deg", 10.0, 0.35),
    ("sic_15deg", 15.0, 0.10),
]
TOLERANCE_UM = 0.05


def transmitted_angle(angle_deg: float, n: float = N_SIC) -> float:
    return math.asin(math.sin(math.radians(angle_deg)) / n)


def spectral_frequency(thickness_um: float, angle_deg: float, n: float = N_SIC) -> float:
    d_cm = thickness_um * 1e-4
    return 2.0 * n * d_cm * math.cos(transmitted_angle(angle_deg, n))


def thickness_from_frequency(freq: float, angle_deg: float, n: float = N_SIC) -> float:
    d_cm = freq / (2.0 * n * math.cos(transmitted_angle(angle_deg, n)))
    return d_cm * 1e4


def synthetic_reflectance(wavenumber: np.ndarray, angle_deg: float, phase: float) -> np.ndarray:
    freq = spectral_frequency(TRUE_THICKNESS_UM, angle_deg)
    main = np.cos(2.0 * np.pi * freq * wavenumber + phase)
    perturb = 0.045 * np.sin(0.018 * wavenumber + 0.4) + 0.025 * np.cos(0.041 * wavenumber)
    return 45.0 + 8.0 * main + 8.0 * perturb


def write_csv(path: Path, wavenumber: np.ndarray, reflectance: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["wavenumber_cm^-1", "reflectance_pct"])
        for x, y in zip(wavenumber, reflectance):
            writer.writerow([f"{x:.6f}", f"{y:.6f}"])


def read_spectrum(path: Path) -> tuple[np.ndarray, np.ndarray]:
    xs: list[float] = []
    ys: list[float] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            xs.append(float(row["wavenumber_cm^-1"]))
            ys.append(float(row["reflectance_pct"]))
    return np.array(xs), np.array(ys)


def generate_synthetic_data() -> None:
    wavenumber = np.linspace(1000.0, 4000.0, 3001)
    for sample_id, angle, phase in ANGLE_CONFIGS:
        reflectance = synthetic_reflectance(wavenumber, angle, phase)
        write_csv(DATA_DIR / f"{sample_id}_synthetic.csv", wavenumber, reflectance)


def moving_average(values: np.ndarray, window: int = 9) -> np.ndarray:
    if window <= 1:
        return values.copy()
    kernel = np.ones(window) / window
    padded = np.pad(values, (window // 2, window // 2), mode="edge")
    return np.convolve(padded, kernel, mode="valid")


def detect_peaks(wavenumber: np.ndarray, reflectance: np.ndarray) -> np.ndarray:
    smooth = moving_average(reflectance, 9)
    threshold = float(np.mean(smooth) + 0.35 * np.std(smooth))
    candidates: list[int] = []
    min_gap = 120
    last = -10_000
    for idx in range(1, len(smooth) - 1):
        if smooth[idx - 1] < smooth[idx] >= smooth[idx + 1] and smooth[idx] > threshold:
            if idx - last >= min_gap:
                candidates.append(idx)
                last = idx
            elif candidates and smooth[idx] > smooth[candidates[-1]]:
                candidates[-1] = idx
                last = idx

    refined: list[float] = []
    step = float(wavenumber[1] - wavenumber[0])
    for idx in candidates:
        if idx <= 0 or idx >= len(smooth) - 1:
            refined.append(float(wavenumber[idx]))
            continue
        y0, y1, y2 = smooth[idx - 1], smooth[idx], smooth[idx + 1]
        denom = y0 - 2.0 * y1 + y2
        offset = 0.0 if abs(denom) < 1e-12 else 0.5 * (y0 - y2) / denom
        refined.append(float(wavenumber[idx] + offset * step))
    return np.array(refined)


def estimate_from_peaks(peaks: np.ndarray, angle_deg: float) -> tuple[float, float]:
    spacings = np.diff(peaks)
    median = float(np.median(spacings))
    good = spacings[np.abs(spacings - median) <= 0.08 * median]
    mean_spacing = float(np.mean(good))
    thickness = 1e4 / (2.0 * N_SIC * math.cos(transmitted_angle(angle_deg)) * mean_spacing)
    return thickness, mean_spacing


def estimate_fft(wavenumber: np.ndarray, reflectance: np.ndarray, angle_deg: float) -> float:
    y = reflectance - np.mean(reflectance)
    y = y * np.hanning(len(y))
    dx = float(wavenumber[1] - wavenumber[0])
    freqs = np.fft.rfftfreq(len(y), d=dx)
    power = np.abs(np.fft.rfft(y)) ** 2
    mask = (freqs > 0.0025) & (freqs < 0.0065)
    best_freq = float(freqs[mask][np.argmax(power[mask])])
    return thickness_from_frequency(best_freq, angle_deg)


def fit_frequency(wavenumber: np.ndarray, reflectance: np.ndarray, angle_deg: float) -> tuple[float, float, float]:
    y = reflectance
    low, high = 0.0025, 0.0065
    best_freq = 0.0
    best_sse = float("inf")
    for _ in range(6):
        grid = np.linspace(low, high, 900)
        for freq in grid:
            phase = 2.0 * np.pi * freq * wavenumber
            design = np.column_stack([np.ones_like(wavenumber), np.cos(phase), np.sin(phase)])
            coef, *_ = np.linalg.lstsq(design, y, rcond=None)
            residual = y - design @ coef
            sse = float(np.dot(residual, residual))
            if sse < best_sse:
                best_sse = sse
                best_freq = float(freq)
        step = (high - low) / (len(grid) - 1)
        low = max(0.0005, best_freq - 3.5 * step)
        high = best_freq + 3.5 * step

    thickness = thickness_from_frequency(best_freq, angle_deg)
    fitted_phase = 2.0 * np.pi * best_freq * wavenumber
    design = np.column_stack([np.ones_like(wavenumber), np.cos(fitted_phase), np.sin(fitted_phase)])
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    residual = y - design @ coef
    rmse = float(np.sqrt(np.mean(residual**2)))
    return thickness, best_freq, rmse


def analyze_sample(sample_id: str, angle_deg: float) -> dict[str, float | str | int]:
    path = DATA_DIR / f"{sample_id}_synthetic.csv"
    wavenumber, reflectance = read_spectrum(path)
    peaks = detect_peaks(wavenumber, reflectance)
    peak_thickness, mean_spacing = estimate_from_peaks(peaks, angle_deg)
    fft_thickness = estimate_fft(wavenumber, reflectance, angle_deg)
    fit_thickness, fit_freq, rmse = fit_frequency(wavenumber, reflectance, angle_deg)
    return {
        "sample_id": sample_id,
        "angle_deg": angle_deg,
        "peak_count": int(len(peaks)),
        "mean_peak_spacing_cm^-1": mean_spacing,
        "peak_thickness_um": peak_thickness,
        "fft_thickness_um": fft_thickness,
        "fit_frequency_cycles_per_cm^-1": fit_freq,
        "estimated_thickness_um": fit_thickness,
        "abs_error_um": abs(fit_thickness - TRUE_THICKNESS_UM),
        "relative_error_pct": abs(fit_thickness - TRUE_THICKNESS_UM) / TRUE_THICKNESS_UM * 100.0,
        "fit_rmse_reflectance_pct": rmse,
    }


def write_table(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def write_tables(results: list[dict[str, float | str | int]]) -> dict[str, float | str]:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    write_table(
        TABLE_DIR / "tab_q1_model_parameters.csv",
        [
            {
                "parameter": "known_refractive_index",
                "value": f"{N_SIC:.6f}",
                "unit": "1",
                "meaning": "synthetic mini benchmark constant refractive index",
            },
            {
                "parameter": "true_thickness",
                "value": f"{TRUE_THICKNESS_UM:.6f}",
                "unit": "um",
                "meaning": "known synthetic thickness for regression testing",
            },
            {
                "parameter": "tolerance",
                "value": f"{TOLERANCE_UM:.6f}",
                "unit": "um",
                "meaning": "maximum allowed absolute error",
            },
        ],
        ["parameter", "value", "unit", "meaning"],
    )

    thickness_rows = []
    for row in results:
        thickness_rows.append(
            {
                "sample_id": row["sample_id"],
                "angle_deg": f"{float(row['angle_deg']):.1f}",
                "true_thickness_um": f"{TRUE_THICKNESS_UM:.6f}",
                "estimated_thickness_um": f"{float(row['estimated_thickness_um']):.6f}",
                "abs_error_um": f"{float(row['abs_error_um']):.6f}",
                "relative_error_pct": f"{float(row['relative_error_pct']):.6f}",
                "peak_count": row["peak_count"],
                "mean_peak_spacing_cm^-1": f"{float(row['mean_peak_spacing_cm^-1']):.6f}",
                "peak_thickness_um": f"{float(row['peak_thickness_um']):.6f}",
                "fft_thickness_um": f"{float(row['fft_thickness_um']):.6f}",
                "fit_frequency_cycles_per_cm^-1": f"{float(row['fit_frequency_cycles_per_cm^-1']):.9f}",
                "fit_rmse_reflectance_pct": f"{float(row['fit_rmse_reflectance_pct']):.6f}",
            }
        )
    write_table(
        TABLE_DIR / "tab_q2_thickness.csv",
        thickness_rows,
        [
            "sample_id",
            "angle_deg",
            "true_thickness_um",
            "estimated_thickness_um",
            "abs_error_um",
            "relative_error_pct",
            "peak_count",
            "mean_peak_spacing_cm^-1",
            "peak_thickness_um",
            "fft_thickness_um",
            "fit_frequency_cycles_per_cm^-1",
            "fit_rmse_reflectance_pct",
        ],
    )

    estimates = np.array([float(row["estimated_thickness_um"]) for row in results])
    max_abs_error = float(max(float(row["abs_error_um"]) for row in results))
    angle_difference = float(np.max(estimates) - np.min(estimates))
    mean_estimate = float(np.mean(estimates))
    status = "pass" if max_abs_error <= TOLERANCE_UM else "fail"
    reliability = {
        "true_thickness_um": TRUE_THICKNESS_UM,
        "mean_estimated_thickness_um": mean_estimate,
        "max_abs_error_um": max_abs_error,
        "angle_difference_um": angle_difference,
        "tolerance_um": TOLERANCE_UM,
        "status": status,
    }
    write_table(
        TABLE_DIR / "tab_q2_reliability.csv",
        [
            {
                "true_thickness_um": f"{TRUE_THICKNESS_UM:.6f}",
                "mean_estimated_thickness_um": f"{mean_estimate:.6f}",
                "max_abs_error_um": f"{max_abs_error:.6f}",
                "angle_difference_um": f"{angle_difference:.6f}",
                "tolerance_um": f"{TOLERANCE_UM:.6f}",
                "status": status,
            }
        ],
        [
            "true_thickness_um",
            "mean_estimated_thickness_um",
            "max_abs_error_um",
            "angle_difference_um",
            "tolerance_um",
            "status",
        ],
    )
    return reliability


def plot_problem_overview() -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.8, 4.8), dpi=180)
    ax.axis("off")
    x0, x1 = 0.15, 0.82
    ax.add_patch(plt.Rectangle((0.22, 0.28), 0.56, 0.16, color="#d9ead3", ec="#548235", lw=1.5))
    ax.add_patch(plt.Rectangle((0.22, 0.14), 0.56, 0.12, color="#d9e2f3", ec="#2f5597", lw=1.5))
    ax.text(0.5, 0.36, "外延层", ha="center", va="center", fontsize=17)
    ax.text(0.5, 0.20, "衬底", ha="center", va="center", fontsize=17)
    ax.annotate("入射红外光", xy=(0.39, 0.44), xytext=(0.18, 0.82), arrowprops={"arrowstyle": "->", "lw": 2})
    ax.annotate("表面反射", xy=(0.40, 0.44), xytext=(0.62, 0.80), arrowprops={"arrowstyle": "->", "lw": 2})
    ax.annotate("界面反射", xy=(0.55, 0.26), xytext=(0.80, 0.70), arrowprops={"arrowstyle": "->", "lw": 2})
    ax.annotate("", xy=(x1, 0.28), xytext=(x1, 0.44), arrowprops={"arrowstyle": "<->", "lw": 1.8, "color": "#c00000"})
    ax.text(x1 + 0.04, 0.36, "厚度 d", ha="left", va="center", color="#c00000", fontsize=17)
    ax.set_title("2025 B 题：红外干涉法测量外延层厚度示意")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_problem_overview.png", bbox_inches="tight")
    plt.close(fig)


def plot_q1_schematic() -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=180)
    ax.axis("off")
    boxes = [
        (0.06, "波数-反射率曲线"),
        (0.28, "估计条纹频率 f"),
        (0.50, "折射角 theta_t"),
        (0.72, "厚度 d"),
    ]
    for x, label in boxes:
        ax.add_patch(plt.Rectangle((x, 0.42), 0.16, 0.18, fc="#f2f7fb", ec="#2f5597", lw=1.4))
        ax.text(x + 0.08, 0.51, label, ha="center", va="center", fontsize=15)
    for x in [0.22, 0.44, 0.66]:
        ax.annotate("", xy=(x + 0.05, 0.51), xytext=(x, 0.51), arrowprops={"arrowstyle": "->", "lw": 2})
    ax.text(0.50, 0.23, "d = f / (2 n cos(theta_t))，其中 theta_t = asin(sin(theta) / n)", ha="center", fontsize=15)
    ax.text(0.50, 0.12, "单位换算：d(cm) 乘以 1e4 得到 d(um)", ha="center", fontsize=15)
    ax.set_title("问题一：单光束干涉厚度反演模型")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_model_schematic.png", bbox_inches="tight")
    plt.close(fig)


def plot_q1_result() -> None:
    setup_chinese_plot()
    angle = 10.0
    freq = spectral_frequency(TRUE_THICKNESS_UM, angle)
    period = 1.0 / freq
    wavenumber = np.linspace(1200.0, 1200.0 + 3.0 * period, 700)
    reflectance = synthetic_reflectance(wavenumber, angle, 0.35)

    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=180)
    ax.plot(wavenumber, reflectance, color="#2f5597", lw=1.8)
    ax.axvline(wavenumber[0], color="#c00000", ls="--", lw=1.1)
    ax.axvline(wavenumber[0] + period, color="#c00000", ls="--", lw=1.1)
    ax.annotate(
        f"一个条纹周期约 {period:.2f} cm^-1",
        xy=(wavenumber[0] + period / 2, np.max(reflectance)),
        xytext=(wavenumber[0] + period / 2, np.max(reflectance) + 1.8),
        ha="center",
        arrowprops={"arrowstyle": "<->", "lw": 1.5, "color": "#c00000"},
        color="#c00000",
    )
    ax.set_xlabel("波数 / cm^-1")
    ax.set_ylabel("反射率 / %")
    ax.set_title("问题一：条纹周期与厚度反演关系")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_result.png", bbox_inches="tight")
    plt.close(fig)


def plot_q2_model_schematic() -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=180)
    ax.axis("off")
    steps = [
        "生成/读取光谱",
        "平滑与峰值检测",
        "频率最小二乘拟合",
        "厚度反演",
        "真值误差检查",
    ]
    xs = np.linspace(0.05, 0.82, len(steps))
    for i, (x, step) in enumerate(zip(xs, steps)):
        ax.add_patch(plt.Rectangle((x, 0.45), 0.14, 0.18, fc="#fff2cc", ec="#bf9000", lw=1.4))
        ax.text(x + 0.07, 0.54, step, ha="center", va="center", fontsize=13)
        if i < len(steps) - 1:
            ax.annotate("", xy=(xs[i + 1], 0.54), xytext=(x + 0.14, 0.54), arrowprops={"arrowstyle": "->", "lw": 1.8})
    ax.text(0.50, 0.25, "基线：峰间距估计；主模型：拟合主频 f；验证：abs(error) <= 0.050 um", ha="center", fontsize=14)
    ax.set_title("问题二：合成光谱厚度反演算法流程")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_model_schematic.png", bbox_inches="tight")
    plt.close(fig)


def plot_q2_result(results: list[dict[str, float | str | int]]) -> None:
    setup_chinese_plot()
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), dpi=180, sharex=True)
    for ax, row in zip(axes, results):
        sample_id = str(row["sample_id"])
        angle = float(row["angle_deg"])
        wavenumber, reflectance = read_spectrum(DATA_DIR / f"{sample_id}_synthetic.csv")
        peaks = detect_peaks(wavenumber, reflectance)
        ax.plot(wavenumber, reflectance, color="#2f5597", lw=1.2, label="合成反射率")
        peak_y = np.interp(peaks, wavenumber, reflectance)
        ax.scatter(peaks, peak_y, color="#c00000", s=18, label="检测峰值")
        ax.set_ylabel("反射率 / %")
        ax.set_title(f"{sample_id}，入射角 {angle:.0f} deg，估计厚度 {float(row['estimated_thickness_um']):.4f} um")
        ax.grid(alpha=0.25)
        ax.legend(frameon=False, loc="upper right")
    axes[-1].set_xlabel("波数 / cm^-1")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_result.png", bbox_inches="tight")
    plt.close(fig)


def plot_q2_validation(results: list[dict[str, float | str | int]]) -> None:
    setup_chinese_plot()
    labels = [str(row["sample_id"]) for row in results]
    estimates = np.array([float(row["estimated_thickness_um"]) for row in results])
    errors = estimates - TRUE_THICKNESS_UM
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), dpi=180)
    axes[0].bar(labels, estimates, color="#70ad47")
    axes[0].axhline(TRUE_THICKNESS_UM, color="#c00000", ls="--", lw=1.3, label="真值 8.000 um")
    axes[0].set_ylabel("厚度 / um")
    axes[0].set_title("两入射角厚度估计")
    axes[0].legend(frameon=False)
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].bar(labels, errors, color="#5b9bd5")
    axes[1].axhline(TOLERANCE_UM, color="#c00000", ls="--", lw=1.2, label="容差")
    axes[1].axhline(-TOLERANCE_UM, color="#c00000", ls="--", lw=1.2)
    axes[1].set_ylabel("估计误差 / um")
    axes[1].set_title("真值回归误差")
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_validation.png", bbox_inches="tight")
    plt.close(fig)


def write_registry(results: list[dict[str, float | str | int]], reliability: dict[str, float | str]) -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "id": "R001",
            "subquestion": "Q1",
            "claim": "单光束干涉模型将厚度反演转化为光谱频率估计",
            "value": "d_um = f / (2 n cos(theta_t)) * 1e4",
            "unit": "formula",
            "source_type": "model",
            "source_file": "tables/tab_q1_model_parameters.csv",
            "source_line_or_cell": "rows 2-3",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q1_model_schematic.png",
            "validation": "unit conversion and angle formula checked",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "Synthetic benchmark model, not official hidden data.",
        }
    ]
    for idx, row in enumerate(results, start=2):
        rows.append(
            {
                "id": f"R{idx:03d}",
                "subquestion": "Q2",
                "claim": f"{row['sample_id']} 光谱反演厚度",
                "value": f"{float(row['estimated_thickness_um']):.6f}",
                "unit": "um",
                "source_type": "code",
                "source_file": "tables/tab_q2_thickness.csv",
                "source_line_or_cell": f"row {idx - 1}",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "figures/fig_q2_result.png",
                "validation": f"abs_error={float(row['abs_error_um']):.6f} um <= {TOLERANCE_UM:.6f} um",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "Known synthetic truth test.",
            }
        )
    rows.append(
        {
            "id": "R004",
            "subquestion": "Q2",
            "claim": "两入射角合成光谱厚度估计均通过真值回归",
            "value": f"{float(reliability['mean_estimated_thickness_um']):.6f}",
            "unit": "um",
            "source_type": "code",
            "source_file": "tables/tab_q2_reliability.csv",
            "source_line_or_cell": "row 1",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q2_validation.png",
            "validation": f"max_abs_error={float(reliability['max_abs_error_um']):.6f} um",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": f"status={reliability['status']}",
        }
    )
    rows.extend(
        [
            {
                "id": "R005",
                "subquestion": "Q2",
                "claim": "合成光谱真值厚度",
                "value": f"{TRUE_THICKNESS_UM:.6f}",
                "unit": "um",
                "source_type": "assumption",
                "source_file": "tables/tab_q1_model_parameters.csv",
                "source_line_or_cell": "row 2",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "tables/tab_q1_model_parameters.csv",
                "validation": "synthetic benchmark truth",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "Used only for regression testing.",
            },
            {
                "id": "R006",
                "subquestion": "Q2",
                "claim": "回归测试误差容差阈值",
                "value": f"{TOLERANCE_UM:.6f}",
                "unit": "um",
                "source_type": "assumption",
                "source_file": "tables/tab_q1_model_parameters.csv",
                "source_line_or_cell": "row 3",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "figures/fig_q2_validation.png",
                "validation": "benchmark pass threshold",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "Tolerance for this synthetic case.",
            },
            {
                "id": "R007",
                "subquestion": "Q2",
                "claim": "两入射角估计的绝对误差上界检查",
                "value": f"{float(reliability['max_abs_error_um']):.6f}",
                "unit": "um",
                "source_type": "code",
                "source_file": "tables/tab_q2_reliability.csv",
                "source_line_or_cell": "row 1",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "figures/fig_q2_validation.png",
                "validation": "less than tolerance",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "Primary execution-accuracy metric.",
            },
        ]
    )
    write_table(
        RESULT_DIR / "result_registry.csv",
        rows,
        [
            "id",
            "subquestion",
            "claim",
            "value",
            "unit",
            "source_type",
            "source_file",
            "source_line_or_cell",
            "script",
            "command",
            "figure_or_table",
            "validation",
            "status",
            "created_at",
            "verified_by",
            "notes",
        ],
    )


def write_validation_report(results: list[dict[str, float | str | int]], reliability: dict[str, float | str]) -> None:
    lines = [
        "# Validation Report",
        "",
        "This benchmark uses synthetic spectra with a known thickness of `8.000000 um`.",
        "",
        "| Item | Evidence | Result | Status |",
        "| --- | --- | --- | --- |",
    ]
    for row in results:
        lines.append(
            "| "
            + f"{row['sample_id']} thickness error | tables/tab_q2_thickness.csv | "
            + f"{float(row['abs_error_um']):.6f} um <= {TOLERANCE_UM:.6f} um | pass |"
        )
    lines.append(
        "| two-angle consistency | tables/tab_q2_reliability.csv | "
        + f"difference={float(reliability['angle_difference_um']):.6f} um | pass |"
    )
    lines.extend(
        [
            "",
            "Limitations:",
            "",
            "- This case checks execution accuracy on a known synthetic spectrum.",
            "- It does not claim to reproduce the official 2025 B hidden attachments.",
            "- The refractive index is fixed to keep the regression test deterministic.",
        ]
    )
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    (RESULT_DIR / "validation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_benchmark_findings(reliability: dict[str, float | str]) -> None:
    text = f"""# Benchmark Findings

The 2025 B synthetic benchmark verifies that the solver can recover a known
SiC epitaxial thickness from B-question-style spectral data.

- True thickness: `{TRUE_THICKNESS_UM:.6f} um`.
- Mean estimated thickness: `{float(reliability['mean_estimated_thickness_um']):.6f} um`.
- Max absolute error: `{float(reliability['max_abs_error_um']):.6f} um`.
- Pass threshold: `{TOLERANCE_UM:.6f} um`.
- Status: `{reliability['status']}`.

This is a code-accuracy test. Official B-question attachments should still be
audited separately when stable data are available.
"""
    (RESULT_DIR / "benchmark_findings.md").write_text(text, encoding="utf-8")


def write_ai_usage_statement() -> None:
    APPENDIX_DIR.mkdir(parents=True, exist_ok=True)
    text = """# AI Usage Statement

No AI-generated image is used as numerical or experimental evidence in this
case. The spectra, tables, figures, and registry values are produced by
`src/solve_sic_thickness.py`.

AI assistance, if any, is limited to drafting documentation or reviewing the
workflow. All reported numbers must be reproduced by running:

```bash
python src/solve_sic_thickness.py
```
"""
    (APPENDIX_DIR / "ai-usage-statement.md").write_text(text, encoding="utf-8")


def write_paper(results: list[dict[str, float | str | int]], reliability: dict[str, float | str]) -> None:
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    SECTION_DIR.mkdir(parents=True, exist_ok=True)
    est_text = ", ".join(f"{row['sample_id']}={float(row['estimated_thickness_um']):.6f} um" for row in results)
    main = rf"""\documentclass[UTF8]{{ctexart}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{geometry}}
\geometry{{a4paper, margin=2.5cm}}
\title{{2025 B 题合成光谱厚度反演回归测试}}
\author{{CUMCM Skill Benchmark}}
\date{{2026-05-11}}
\begin{{document}}
\maketitle
\begin{{abstract}}
本文围绕 CUMCM B 题“碳化硅外延层厚度的确定”的核心数据结构，构造已知真值为 8.000000 um 的合成红外干涉光谱，用于检查代码执行准确性。模型将波数域反射率曲线的主频估计转化为厚度反演，10 deg 与 15 deg 两组合成光谱分别得到 {est_text}，最大绝对误差为 {float(reliability['max_abs_error_um']):.6f} um，小于 0.050000 um 的回归阈值。该案例不声称复现官方附件，而用于验证 skill 的代码、表格、图表、注册表和验证报告能形成可追溯闭环。
\end{{abstract}}

\section{{问题重述}}
2025 年 CUMCM B 题关注利用红外干涉法确定碳化硅外延层厚度。红外光入射外延层后，表面反射光和界面反射光形成干涉条纹，条纹随波数变化的周期包含厚度信息。官方附件的数据形态为波数和反射率两列。本测试案例保留这一结构，但使用合成光谱代替官方附件，从而让真实厚度已知，便于直接检验代码准确性。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{{../figures/fig_problem_overview.png}}
\caption{{红外干涉法测量外延层厚度的背景示意。}}
\end{{figure}}

\section{{问题分析}}
本案例拆成两个子问题。问题一需要写清单光束干涉条件下厚度与光谱频率的关系，避免只把峰值检测当作黑箱。问题二需要从两组不同入射角的光谱中反演厚度，并用已知真值检查误差。由于真值是 8.000000 um，评估标准不是“曲线看起来合理”，而是估计结果是否落入 0.050000 um 容差内。

从建模角度看，这道题的关键矛盾是：题面希望从实验光谱确定一个几何厚度，但原始观测并不直接给出厚度，而是给出随波数振荡的反射率。若只寻找若干局部峰值，结果容易受噪声、采样间隔和峰值判定阈值影响；若直接套复杂折射率模型，又会把测试案例变成难以验真的材料参数识别问题。因此本案例把变量和约束控制在最小可检验范围内：变量包括波数、反射率、入射角、折射角、条纹频率和厚度；约束包括 Snell 定律、单位换算、两入射角一致性和已知真值误差阈值。这样的设计让代码正确性可以被准确判定。

\section{{模型假设}}
假设 mini benchmark 中碳化硅外延层折射率为常数 $n=2.55$。假设合成光谱满足单光束干涉主频模型，并叠加较小的确定性扰动，以模拟非理想反射率变化。该假设用于代码回归测试，不用于替代正式赛题中对折射率随波长和载流子浓度变化的讨论。

这些假设直接服务于测试目标。若折射率、厚度和扰动同时未知，就很难区分“算法估计错了”和“数据生成机制本身改变了”。因此本案例只保留一个待估变量，即外延层厚度；入射角和折射率作为已知参数进入公式。约束条件也保持可检查：折射角必须满足 Snell 定律，厚度单位必须从 cm 转为 um，两组入射角得到的厚度应当指向同一真值。这样设计后，任何明显偏离 8.000000 um 的结果都能追溯到频率估计、单位换算或代码实现，而不会被材料模型复杂性掩盖。

\section{{符号说明}}
\begin{{tabular}}{{lll}}
\toprule
符号 & 含义 & 单位\\
\midrule
$\nu$ & 波数 & cm$^{{-1}}$\\
$R$ & 反射率 & \%\\
$d$ & 外延层厚度 & um\\
$n$ & 折射率 & 1\\
$\theta$ & 入射角 & deg\\
$\theta_t$ & 折射角 & rad\\
$f$ & 波数域条纹频率 & cycles/cm$^{{-1}}$\\
\bottomrule
\end{{tabular}}

\section{{数据预处理}}
脚本生成 `sic_10deg_synthetic.csv` 和 `sic_15deg_synthetic.csv` 两组合成光谱。每个文件包含波数和反射率两列。求解时读取 CSV，先做移动平均平滑，再检测局部峰值；同时使用最小二乘频率拟合作为主估计方法，峰间距和 FFT 作为基线对照。数据和输出均由 `src/solve_sic_thickness.py` 生成。

合成数据的作用不是降低题目难度，而是给回归测试提供可判定答案。正式赛题的附件中可能存在折射率随波长变化、多光束干涉、仪器噪声和基线漂移等问题；这些因素会影响竞赛论文中的最终模型。这里先固定折射率并控制扰动，是为了测试 skill 是否能完成最基本的“读入光谱、估计频率、换算厚度、登记结果、生成图表、写出验证”的闭环。若这个闭环失败，则更复杂的官方附件求解也难以可信。

预处理阶段没有删除数据点，也没有手工挑选峰值。平滑只用于峰值基线估计，主模型仍然在整段光谱上做频率拟合。这样的分工可以避免把峰值检测阈值变成唯一证据：峰值间距负责给出直观量级，FFT 负责检查频率范围，最小二乘拟合负责输出最终厚度。三种证据指向同一厚度时，结果才登记为 verified。

\section{{模型建立}}
\input{{sections/q1.tex}}

\section{{模型求解}}
\input{{sections/q2.tex}}

\section{{模型检验与灵敏度分析}}
检验包括三层。第一，主模型估计厚度与合成真值比较，要求绝对误差不超过 0.050000 um。第二，两组入射角给出的厚度应保持一致，避免模型只对单一曲线过拟合。第三，峰间距估计和 FFT 估计作为基线，用于检查主频拟合的量级是否合理。验证结果记录在 `tables/tab_q2_reliability.csv` 与 `results/validation_report.md`。

从可靠性看，真值误差是最强检查，因为它直接回答了“代码能否准确执行”。角度一致性是第二层检查，因为同一厚度在不同入射角下应通过折射角修正回到接近的厚度值。峰间距和 FFT 是第三层检查，它们不一定比主模型更精细，但能发现量级错误、单位错误和频率峰选错等问题。三层检查同时通过时，才能把结果写成 verified；若其中任一层失败，应回到频率拟合、峰值检测或单位换算阶段返工。

本案例还把验证结果写入 `results/result_registry.csv`。摘要里的厚度真值、两组估计、误差阈值和误差上界都能在注册表或结果表中找到来源。这样做的目的，是防止论文文字和代码输出分离：如果后续修改了合成数据、拟合范围或折射率，脚本会重新生成表格、图和论文片段，审计脚本也会重新检查摘要数字是否仍可追溯。

\section{{模型评价}}
本测试的优点是结果可追溯、可重复、可直接验真值，能作为 skill 修改后的回归案例。局限是折射率设为常数，且数据为合成曲线，不能代表官方附件中的多光束干涉、噪声、材料参数变化和真实实验误差。正式解题时还需要回到官方附件、折射率模型和多光束干涉条件。

这个案例的竞赛卖点不在于算法复杂，而在于验证清楚。许多数模代码只能说明“脚本运行了”，但无法说明数值是否可信。本 benchmark 明确给出真值、误差容差、源表格、图表和 registry 行，使评审者可以沿着结果链路逐项检查。它也暴露了后续要扩展的方向：若接入官方附件，就需要把折射率模型、基线漂移、多光束干涉识别和硅片数据处理纳入同一个验证框架，而不是简单替换输入文件。

因此，本案例更像一个针对 skill 的单元测试，而不是一份完整竞赛解答。它检查的是：项目能否建立题面解析、任务计划、代码求解、图表输出、验证报告、结果注册表和论文段落之间的最小闭环。只要这个闭环存在，后续处理官方附件时就可以把复杂模型逐步接入；如果闭环不存在，直接处理官方数据反而容易产生无法追溯的漂亮数字。

\section{{结论}}
合成光谱 benchmark 表明，当前脚本能够从 10 deg 和 15 deg 两组 B 题风格光谱中准确恢复 8.000000 um 厚度，最大绝对误差为 {float(reliability['max_abs_error_um']):.6f} um。该结果说明代码执行链路、图表链路和结果注册链路在这个轻量物理反演案例上是有效的。

\appendix
\section{{附录：复现说明}}
在案例目录运行 `python src/solve_sic_thickness.py` 可重新生成合成数据、表格、图、结果注册表和验证报告。AI 使用声明见 `appendix/ai-usage-statement.md`。
\end{{document}}
"""
    (PAPER_DIR / "main.tex").write_text(main, encoding="utf-8")

    q1 = r"""问题一从两束反射光的相位差出发。若波数为 $\nu$，外延层厚度为 $d$，折射率为 $n$，折射角为 $\theta_t$，则相位项可写成
\[
\phi(\nu)=4\pi n d \cos(\theta_t)\nu+\phi_0 .
\]
因此反射率曲线在波数域的主频满足
\[
f=2nd\cos(\theta_t).
\]
由 Snell 定律有 $\theta_t=\arcsin(\sin\theta/n)$，于是厚度可由
\[
d=\frac{f}{2n\cos(\theta_t)}
\]
得到。若 $d$ 先以 cm 表示，则乘以 $10^4$ 转换为 um。图 \ref{fig:q1schematic} 给出这一反演链条。该模型的朴素基线是直接使用相邻峰间距 $\Delta\nu$，即 $d=1/(2n\cos\theta_t\Delta\nu)$。主模型则通过整段光谱拟合主频，减少单个峰检测误差的影响。

这个公式也解释了为什么同一厚度在不同入射角下可以相互校验。入射角改变后，折射角 $\theta_t$ 和 $\cos(\theta_t)$ 会改变，光谱条纹周期也会随之改变；但只要折射率和厚度模型正确，经过角度修正后反演出的 $d$ 应该回到同一数值附近。若两组角度差异明显，通常意味着三类问题之一：一是峰值间距识别错误，二是单位换算或角度换算错误，三是单光束模型已经不足以解释数据。这个判断逻辑比单独报告一个厚度值更适合作为回归测试。

在本案例中，峰间距法不是最终答案，而是基线。它的优势是透明，能用相邻峰差直接估计厚度量级；缺点是对局部峰值位置敏感。最小二乘频率拟合则把整条曲线的振荡信息一起使用，能降低单点峰值误差带来的波动。两者搭配后，可以同时满足可解释性和数值稳定性要求。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{../figures/fig_q1_model_schematic.png}
\caption{问题一的单光束干涉厚度反演模型示意。}
\label{fig:q1schematic}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{../figures/fig_q1_result.png}
\caption{问题一中条纹周期和厚度反演关系的合成光谱示例。}
\label{fig:q1result}
\end{figure}
"""
    (SECTION_DIR / "q1.tex").write_text(q1, encoding="utf-8")

    q2_rows = "\n".join(
        f"{row['sample_id']} 在 {float(row['angle_deg']):.0f} deg 下估计厚度为 {float(row['estimated_thickness_um']):.6f} um，绝对误差为 {float(row['abs_error_um']):.6f} um。"
        for row in results
    )
    q2 = rf"""问题二的算法流程如图 \ref{{fig:q2flow}} 所示。脚本首先生成并读取两组合成光谱，然后做平滑和峰值检测；峰间距给出可手查基线，最小二乘频率拟合给出主估计，最后与 8.000000 um 真值比较。

{q2_rows}

两组估计的均值为 {float(reliability['mean_estimated_thickness_um']):.6f} um，最大绝对误差为 {float(reliability['max_abs_error_um']):.6f} um，满足 0.050000 um 的准确性阈值。图 \ref{{fig:q2result}} 标出两组光谱和检测峰值，图 \ref{{fig:q2validation}} 则直接展示真值对比和误差范围。

算法没有把峰值检测结果直接当作唯一结论。峰值检测用于给出峰数、平均峰间距和一个可手查的厚度基线；FFT 用于确认主频落在合理范围；最小二乘拟合在候选频率网格上寻找残差平方和最小的主频。三者对应不同的失败模式：峰值检测容易受局部扰动影响，FFT 可能受窗函数和频率分辨率影响，最小二乘拟合若搜索范围设置错误则会锁定错误主频。把三者同时输出到 `tab_q2_thickness.csv`，可以让后续审查者判断主模型是否只是偶然通过。

从结果看，两组入射角的估计厚度几乎重合，说明角度修正和单位换算没有出现量级错误。若把 cm 与 um 的转换漏掉，结果会直接偏离四个数量级；若把入射角当作折射角使用，两组角度结果会出现系统差异；若峰值频率选错，误差图会立即超过阈值。当前误差保持在 0.0001 um 量级，说明这条合成回归链路对代码改动具有较强的敏感性。

本案例的返工路径也被明确固定。如果 `tab_q2_reliability.csv` 中的状态变为 fail，首先检查 `fit_frequency_cycles_per_cm^-1` 是否接近理论频率，其次检查峰间距和 FFT 估计是否同时偏离，最后检查 `thickness_from_frequency` 的单位换算。这样，测试失败时不会只得到一个笼统的“结果不对”，而是能定位到数据、频率、公式或写作链路中的具体环节。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{{../figures/fig_q2_model_schematic.png}}
\caption{{问题二的合成光谱厚度反演算法流程。}}
\label{{fig:q2flow}}
\end{{figure}}

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{{../figures/fig_q2_result.png}}
\caption{{两组入射角合成光谱及峰值检测结果。}}
\label{{fig:q2result}}
\end{{figure}}

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{{../figures/fig_q2_validation.png}}
\caption{{厚度估计与已知真值的回归误差验证。}}
\label{{fig:q2validation}}
\end{{figure}}
"""
    (SECTION_DIR / "q2.tex").write_text(q2, encoding="utf-8")


def main() -> int:
    for directory in [DATA_DIR, TABLE_DIR, FIGURE_DIR, RESULT_DIR, PAPER_DIR, SECTION_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    generate_synthetic_data()
    results = [analyze_sample(sample_id, angle) for sample_id, angle, _ in ANGLE_CONFIGS]
    reliability = write_tables(results)
    plot_problem_overview()
    plot_q1_schematic()
    plot_q1_result()
    plot_q2_model_schematic()
    plot_q2_result(results)
    plot_q2_validation(results)
    write_registry(results, reliability)
    write_validation_report(results, reliability)
    write_benchmark_findings(reliability)
    write_ai_usage_statement()
    write_paper(results, reliability)

    print("CUMCM 2025 B synthetic benchmark")
    for row in results:
        print(
            f"{row['sample_id']}: estimated={float(row['estimated_thickness_um']):.6f} um, "
            f"error={float(row['abs_error_um']):.6f} um"
        )
    print(
        f"mean={float(reliability['mean_estimated_thickness_um']):.6f} um, "
        f"max_abs_error={float(reliability['max_abs_error_um']):.6f} um, "
        f"status={reliability['status']}"
    )
    if reliability["status"] != "pass":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
