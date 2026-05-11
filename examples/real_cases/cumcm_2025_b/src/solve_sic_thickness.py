#!/usr/bin/env python3
"""Solve a reproducible SiC epitaxial-layer thickness inverse problem."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import numpy as np

from plot_utils import setup_chinese_plot


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
TABLE_DIR = ROOT / "tables"
FIGURE_DIR = ROOT / "figures"
RESULT_DIR = ROOT / "results"
PAPER_DIR = ROOT / "paper"
SECTION_DIR = PAPER_DIR / "sections"

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


def generate_spectra() -> None:
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


def estimate_fft(wavenumber: np.ndarray, reflectance: np.ndarray, angle_deg: float) -> tuple[float, float]:
    y = reflectance - np.mean(reflectance)
    y = y * np.hanning(len(y))
    dx = float(wavenumber[1] - wavenumber[0])
    freqs = np.fft.rfftfreq(len(y), d=dx)
    power = np.abs(np.fft.rfft(y)) ** 2
    mask = (freqs > 0.0025) & (freqs < 0.0065)
    best_freq = float(freqs[mask][np.argmax(power[mask])])
    return thickness_from_frequency(best_freq, angle_deg), best_freq


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
    fft_thickness, fft_freq = estimate_fft(wavenumber, reflectance, angle_deg)
    fit_thickness, fit_freq, rmse = fit_frequency(wavenumber, reflectance, angle_deg)
    return {
        "sample_id": sample_id,
        "angle_deg": angle_deg,
        "peak_count": int(len(peaks)),
        "mean_peak_spacing_cm^-1": mean_spacing,
        "peak_thickness_um": peak_thickness,
        "fft_frequency_cycles_per_cm^-1": fft_freq,
        "fft_thickness_um": fft_thickness,
        "fit_frequency_cycles_per_cm^-1": fit_freq,
        "estimated_thickness_um": fit_thickness,
        "abs_error_um": abs(fit_thickness - TRUE_THICKNESS_UM),
        "relative_error_pct": abs(fit_thickness - TRUE_THICKNESS_UM) / TRUE_THICKNESS_UM * 100.0,
        "fit_rmse_reflectance_pct": rmse,
    }


def sensitivity_profiles(results: list[dict[str, float | str | int]]) -> list[dict[str, object]]:
    base_mean = float(np.mean([float(row["estimated_thickness_um"]) for row in results]))
    rows: list[dict[str, object]] = []
    n_values = np.linspace(2.50, 2.60, 21)
    for n_value in n_values:
        estimates = [
            thickness_from_frequency(
                float(row["fit_frequency_cycles_per_cm^-1"]),
                float(row["angle_deg"]),
                float(n_value),
            )
            for row in results
        ]
        mean_thickness = float(np.mean(estimates))
        rows.append(
            {
                "sensitivity_type": "refractive_index",
                "input_value": f"{n_value:.3f}",
                "mean_thickness_um": f"{mean_thickness:.6f}",
                "delta_from_base_um": f"{mean_thickness - base_mean:.6f}",
            }
        )

    angle_offsets = np.linspace(-0.5, 0.5, 21)
    for offset in angle_offsets:
        estimates = [
            thickness_from_frequency(
                float(row["fit_frequency_cycles_per_cm^-1"]),
                float(row["angle_deg"]) + float(offset),
                N_SIC,
            )
            for row in results
        ]
        mean_thickness = float(np.mean(estimates))
        rows.append(
            {
                "sensitivity_type": "incident_angle_offset_deg",
                "input_value": f"{offset:.3f}",
                "mean_thickness_um": f"{mean_thickness:.6f}",
                "delta_from_base_um": f"{mean_thickness - base_mean:.6f}",
            }
        )
    return rows


def sensitivity_summary(rows: list[dict[str, object]]) -> dict[str, float]:
    summary: dict[str, float] = {}
    for sensitivity_type in ["refractive_index", "incident_angle_offset_deg"]:
        values = [
            float(row["mean_thickness_um"])
            for row in rows
            if row["sensitivity_type"] == sensitivity_type
        ]
        deltas = [
            abs(float(row["delta_from_base_um"]))
            for row in rows
            if row["sensitivity_type"] == sensitivity_type
        ]
        summary[f"{sensitivity_type}_span_um"] = float(max(values) - min(values))
        summary[f"{sensitivity_type}_max_abs_delta_um"] = float(max(deltas))
    return summary


def write_table(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def method_rows(results: list[dict[str, float | str | int]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in results:
        rows.extend(
            [
                {
                    "sample_id": row["sample_id"],
                    "angle_deg": f"{float(row['angle_deg']):.1f}",
                    "method": "peak_spacing",
                    "thickness_um": f"{float(row['peak_thickness_um']):.6f}",
                    "frequency_or_spacing": f"{float(row['mean_peak_spacing_cm^-1']):.6f}",
                    "rmse_reflectance_pct": "not_applicable",
                },
                {
                    "sample_id": row["sample_id"],
                    "angle_deg": f"{float(row['angle_deg']):.1f}",
                    "method": "fft",
                    "thickness_um": f"{float(row['fft_thickness_um']):.6f}",
                    "frequency_or_spacing": f"{float(row['fft_frequency_cycles_per_cm^-1']):.9f}",
                    "rmse_reflectance_pct": "not_applicable",
                },
                {
                    "sample_id": row["sample_id"],
                    "angle_deg": f"{float(row['angle_deg']):.1f}",
                    "method": "least_squares_main_frequency",
                    "thickness_um": f"{float(row['estimated_thickness_um']):.6f}",
                    "frequency_or_spacing": f"{float(row['fit_frequency_cycles_per_cm^-1']):.9f}",
                    "rmse_reflectance_pct": f"{float(row['fit_rmse_reflectance_pct']):.6f}",
                },
            ]
        )
    return rows


def write_tables(results: list[dict[str, float | str | int]]) -> dict[str, float | str]:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    write_table(
        TABLE_DIR / "tab_q1_model_parameters.csv",
        [
            {
                "parameter": "refractive_index",
                "value": f"{N_SIC:.6f}",
                "unit": "1",
                "meaning": "constant refractive index used in the inverse formula",
            },
            {
                "parameter": "known_thickness",
                "value": f"{TRUE_THICKNESS_UM:.6f}",
                "unit": "um",
                "meaning": "known reference thickness",
            },
            {
                "parameter": "error_tolerance",
                "value": f"{TOLERANCE_UM:.6f}",
                "unit": "um",
                "meaning": "accepted upper bound of absolute error",
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
    write_table(
        TABLE_DIR / "tab_method_comparison.csv",
        method_rows(results),
        ["sample_id", "angle_deg", "method", "thickness_um", "frequency_or_spacing", "rmse_reflectance_pct"],
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


def write_sensitivity_table(rows: list[dict[str, object]]) -> dict[str, float]:
    write_table(
        TABLE_DIR / "tab_sensitivity.csv",
        rows,
        ["sensitivity_type", "input_value", "mean_thickness_um", "delta_from_base_um"],
    )
    return sensitivity_summary(rows)


def plot_problem_overview() -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=220)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    air_y = 0.68
    epi_bottom = 0.34
    ax.add_patch(plt.Rectangle((0.12, epi_bottom), 0.68, air_y - epi_bottom, color="#edf2f4", ec="#64748b", lw=1.2))
    ax.add_patch(plt.Rectangle((0.12, 0.16), 0.68, epi_bottom - 0.16, color="#dbe7f3", ec="#475569", lw=1.2))
    ax.plot([0.12, 0.80], [air_y, air_y], color="#334155", lw=1.4)
    ax.plot([0.12, 0.80], [epi_bottom, epi_bottom], color="#334155", lw=1.4)
    ax.text(0.15, 0.76, "空气", fontsize=13, color="#334155")
    ax.text(0.15, 0.49, "SiC 外延层  $n$", fontsize=14, color="#334155")
    ax.text(0.15, 0.23, "衬底", fontsize=14, color="#334155")

    surface = (0.42, air_y)
    interface = (0.54, epi_bottom)
    exit_point = (0.66, air_y)
    incident_start = (0.24, 0.93)
    surface_reflect_end = (0.60, 0.93)
    interface_reflect_end = (0.77, 0.88)
    line_kw = {"arrowstyle": "->", "lw": 2.1, "color": "#2563eb"}
    ax.annotate("", xy=surface, xytext=incident_start, arrowprops=line_kw)
    ax.annotate("", xy=surface_reflect_end, xytext=surface, arrowprops={**line_kw, "color": "#0f766e"})
    ax.annotate("", xy=interface, xytext=surface, arrowprops={**line_kw, "color": "#7c3aed"})
    ax.annotate("", xy=exit_point, xytext=interface, arrowprops={**line_kw, "color": "#7c3aed"})
    ax.annotate("", xy=interface_reflect_end, xytext=exit_point, arrowprops={**line_kw, "color": "#7c3aed"})
    ax.plot([surface[0], surface[0]], [0.31, 0.91], color="#94a3b8", lw=1, ls="--")
    ax.add_patch(Arc(surface, 0.16, 0.16, theta1=92, theta2=128, color="#334155", lw=1.2))
    ax.add_patch(Arc(surface, 0.13, 0.13, theta1=250, theta2=288, color="#334155", lw=1.2))
    ax.text(0.31, 0.79, r"$\theta$", fontsize=13, color="#334155")
    ax.text(0.46, 0.57, r"$\theta_t$", fontsize=13, color="#334155")
    ax.text(0.23, 0.90, "入射光", fontsize=13, color="#2563eb")
    ax.text(0.60, 0.91, "表面反射", fontsize=13, color="#0f766e")
    ax.text(0.69, 0.82, "界面反射", fontsize=13, color="#7c3aed")
    ax.annotate("", xy=(0.84, epi_bottom), xytext=(0.84, air_y), arrowprops={"arrowstyle": "<->", "lw": 1.6, "color": "#b91c1c"})
    ax.text(0.87, (air_y + epi_bottom) / 2, r"厚度 $d$", ha="left", va="center", color="#b91c1c", fontsize=15)
    ax.text(0.48, 0.08, r"$\Delta L=2nd\cos\theta_t,\quad f=2nd\cos\theta_t$", ha="center", fontsize=15, color="#111827")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_problem_overview.png", bbox_inches="tight")
    plt.close(fig)


def plot_q1_schematic() -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=180)
    ax.axis("off")
    boxes = [
        (0.06, "波数-反射率曲线"),
        (0.29, "估计条纹主频 f"),
        (0.52, "由 Snell 定律修正角度"),
        (0.75, "反演厚度 d"),
    ]
    for x, label in boxes:
        ax.add_patch(plt.Rectangle((x, 0.42), 0.16, 0.18, fc="#f2f7fb", ec="#2f5597", lw=1.4))
        ax.text(x + 0.08, 0.51, label, ha="center", va="center", fontsize=13)
    for x in [0.22, 0.45, 0.68]:
        ax.annotate("", xy=(x + 0.05, 0.51), xytext=(x, 0.51), arrowprops={"arrowstyle": "->", "lw": 2})
    ax.text(0.50, 0.25, r"$d=f/(2n\cos\theta_t)$,  $\theta_t=\arcsin(\sin\theta/n)$", ha="center", fontsize=15)
    ax.text(0.50, 0.13, r"频率以 $\mathrm{cm}$ 表示时，厚度换算为 $\mu$m", ha="center", fontsize=15)
    ax.set_title("单光束干涉厚度反演链条")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_model_flow.png", bbox_inches="tight")
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
        f"一个条纹周期约 {period:.1f} $\\mathrm{{cm}}^{{-1}}$",
        xy=(wavenumber[0] + period / 2, np.max(reflectance)),
        xytext=(wavenumber[0] + period / 2, np.max(reflectance) + 1.8),
        ha="center",
        arrowprops={"arrowstyle": "<->", "lw": 1.5, "color": "#c00000"},
        color="#c00000",
    )
    ax.set_xlabel(r"波数 / $\mathrm{cm}^{-1}$")
    ax.set_ylabel("反射率 / %")
    ax.set_title("条纹周期与厚度反演关系")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_result.png", bbox_inches="tight")
    plt.close(fig)


def plot_q2_result(results: list[dict[str, float | str | int]]) -> None:
    setup_chinese_plot()
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), dpi=180, sharex=True)
    for ax, row in zip(axes, results):
        sample_id = str(row["sample_id"])
        angle = float(row["angle_deg"])
        wavenumber, reflectance = read_spectrum(DATA_DIR / f"{sample_id}_synthetic.csv")
        peaks = detect_peaks(wavenumber, reflectance)
        ax.plot(wavenumber, reflectance, color="#2f5597", lw=1.2, label="反射率曲线")
        peak_y = np.interp(peaks, wavenumber, reflectance)
        ax.scatter(peaks, peak_y, color="#c00000", s=18, label="局部峰值")
        ax.set_ylabel("反射率 / %")
        ax.set_title(f"入射角 {angle:.0f}$^\\circ$，厚度估计 {float(row['estimated_thickness_um']):.4f} $\\mu$m")
        ax.grid(alpha=0.25)
        ax.legend(frameon=False, loc="upper right")
    axes[-1].set_xlabel(r"波数 / $\mathrm{cm}^{-1}$")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_result.png", bbox_inches="tight")
    plt.close(fig)


def plot_q2_model_flow() -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(10.6, 4.8), dpi=220)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    boxes = [
        (0.04, 0.62, "波数-反射率\n数据"),
        (0.23, 0.62, "峰值间隔\n先验估计"),
        (0.42, 0.62, "FFT\n粗估主频"),
        (0.61, 0.62, "全谱最小二乘\n主频拟合"),
        (0.80, 0.62, "Snell 修正\n厚度换算"),
        (0.23, 0.24, "多角度\n一致性"),
        (0.42, 0.24, "残差与方法\n对照"),
        (0.61, 0.24, "折射率/角度\n敏感性"),
    ]
    for x, y, label in boxes:
        ax.add_patch(plt.Rectangle((x, y), 0.15, 0.18, fc="#f8fafc", ec="#475569", lw=1.1))
        ax.text(x + 0.075, y + 0.09, label, ha="center", va="center", fontsize=12)
    for x in [0.19, 0.38, 0.57, 0.76]:
        ax.annotate("", xy=(x + 0.035, 0.71), xytext=(x, 0.71), arrowprops={"arrowstyle": "->", "lw": 1.6, "color": "#334155"})
    for start_x, end_x in [(0.875, 0.685), (0.875, 0.495), (0.875, 0.305)]:
        ax.annotate("", xy=(end_x, 0.42), xytext=(start_x, 0.62), arrowprops={"arrowstyle": "->", "lw": 1.2, "color": "#64748b"})
    ax.text(0.50, 0.08, "最终估计必须同时通过量级、残差、多角度一致性和敏感性检验", ha="center", fontsize=13)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_model_flow.png", bbox_inches="tight")
    plt.close(fig)


def plot_q2_validation(results: list[dict[str, float | str | int]]) -> None:
    setup_chinese_plot()
    labels = [f"{float(row['angle_deg']):.0f}$^\\circ$" for row in results]
    estimates = np.array([float(row["estimated_thickness_um"]) for row in results])
    abs_errors = np.abs(estimates - TRUE_THICKNESS_UM)
    x = np.arange(len(labels))
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6), dpi=220)
    axes[0].plot(x, estimates, color="#1f77b4", marker="o", ms=7, lw=1.8, label="主频拟合")
    axes[0].axhline(TRUE_THICKNESS_UM, color="#b91c1c", ls="--", lw=1.3)
    axes[0].text(1.04, TRUE_THICKNESS_UM + 0.004, r"$8.000\,\mu$m 参考线", color="#b91c1c", fontsize=11)
    axes[0].set_xticks(x, labels)
    axes[0].set_ylim(TRUE_THICKNESS_UM - 0.06, TRUE_THICKNESS_UM + 0.06)
    axes[0].set_ylabel(r"厚度 / $\mu$m")
    axes[0].set_title("不同入射角下的厚度估计值")
    for spine in ["top", "right"]:
        axes[0].spines[spine].set_visible(False)
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].scatter(x, abs_errors, color="#1f77b4", s=46, zorder=3)
    axes[1].vlines(x, 1e-6, abs_errors, color="#94a3b8", lw=1.1)
    axes[1].axhline(TOLERANCE_UM, color="#b91c1c", ls="--", lw=1.2)
    axes[1].text(0.60, TOLERANCE_UM * 1.12, r"$0.05\,\mu$m 容差", color="#b91c1c", fontsize=11)
    axes[1].set_xticks(x, labels)
    axes[1].set_yscale("log")
    axes[1].set_ylim(1e-6, 0.1)
    axes[1].set_ylabel(r"绝对误差 / $\mu$m")
    axes[1].set_title("合成验证误差")
    for spine in ["top", "right"]:
        axes[1].spines[spine].set_visible(False)
    axes[1].grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_validation.png", bbox_inches="tight")
    plt.close(fig)


def plot_sensitivity(rows: list[dict[str, object]]) -> None:
    setup_chinese_plot()
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6), dpi=220)
    n_rows = [row for row in rows if row["sensitivity_type"] == "refractive_index"]
    angle_rows = [row for row in rows if row["sensitivity_type"] == "incident_angle_offset_deg"]
    n_x = np.array([float(row["input_value"]) for row in n_rows])
    n_y = np.array([float(row["mean_thickness_um"]) for row in n_rows])
    angle_x = np.array([float(row["input_value"]) for row in angle_rows])
    angle_y = np.array([float(row["mean_thickness_um"]) for row in angle_rows])

    axes[0].plot(n_x, n_y, color="#1f77b4", lw=1.9)
    axes[0].axvline(N_SIC, color="#b91c1c", ls="--", lw=1.1)
    axes[0].axhline(TRUE_THICKNESS_UM, color="#64748b", ls=":", lw=1.1)
    axes[0].set_xlabel("折射率 n")
    axes[0].set_ylabel(r"平均厚度 / $\mu$m")
    axes[0].set_title("折射率敏感性")
    for spine in ["top", "right"]:
        axes[0].spines[spine].set_visible(False)
    axes[0].grid(alpha=0.25)

    axes[1].plot(angle_x, angle_y, color="#0f766e", lw=1.9)
    axes[1].axvline(0.0, color="#b91c1c", ls="--", lw=1.1)
    axes[1].axhline(TRUE_THICKNESS_UM, color="#64748b", ls=":", lw=1.1)
    axes[1].set_xlabel(r"入射角误差 / $^\circ$")
    axes[1].set_ylabel(r"平均厚度 / $\mu$m")
    axes[1].set_title("入射角敏感性")
    for spine in ["top", "right"]:
        axes[1].spines[spine].set_visible(False)
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_sensitivity.png", bbox_inches="tight")
    plt.close(fig)


def write_registry(results: list[dict[str, float | str | int]], reliability: dict[str, float | str]) -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    rows = [
        {
            "id": "R001",
            "subquestion": "Q1",
            "claim": "single-beam interference converts thickness inversion to spectral frequency estimation",
            "value": "d_um = f / (2 n cos(theta_t)) * 1e4",
            "unit": "formula",
            "source_type": "model",
            "source_file": "tables/tab_q1_model_parameters.csv",
            "source_line_or_cell": "rows 1-3",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q1_model_flow.png",
            "validation": "unit conversion and angle correction checked",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "reproducible spectra with a known reference thickness",
        }
    ]
    for idx, row in enumerate(results, start=2):
        rows.append(
            {
                "id": f"R{idx:03d}",
                "subquestion": "Q2",
                "claim": f"{row['sample_id']} thickness estimate",
                "value": f"{float(row['estimated_thickness_um']):.6f}",
                "unit": "um",
                "source_type": "calculation",
                "source_file": "tables/tab_q2_thickness.csv",
                "source_line_or_cell": f"row {idx - 1}",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "figures/fig_q2_result.png",
                "validation": f"abs_error={float(row['abs_error_um']):.6f} um <= {TOLERANCE_UM:.6f} um",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "known reference comparison",
            }
        )
    rows.append(
        {
            "id": "R004",
            "subquestion": "Q2",
            "claim": "two-angle consistency",
            "value": f"{float(reliability['mean_estimated_thickness_um']):.4f}",
            "unit": "um",
            "source_type": "calculation",
            "source_file": "tables/tab_q2_reliability.csv",
            "source_line_or_cell": "row 1",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q2_validation.png",
            "validation": f"max_abs_error={float(reliability['max_abs_error_um']):.6f} um",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "angle-corrected estimates agree",
        }
    )
    rows.extend(
        [
            {
                "id": "R005",
                "subquestion": "Q2",
                "claim": "reference thickness used for controlled validation",
                "value": f"{TRUE_THICKNESS_UM:.6f}",
                "unit": "um",
                "source_type": "assumption",
                "source_file": "tables/tab_q1_model_parameters.csv",
                "source_line_or_cell": "known_thickness",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "tables/tab_q1_model_parameters.csv",
                "validation": "fixed reference for method validation",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "not a measured contest result",
            },
            {
                "id": "R006",
                "subquestion": "Q2",
                "claim": "error tolerance",
                "value": f"{TOLERANCE_UM:.6f}",
                "unit": "um",
                "source_type": "assumption",
                "source_file": "tables/tab_q1_model_parameters.csv",
                "source_line_or_cell": "error_tolerance",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "figures/fig_q2_validation.png",
                "validation": "used as the acceptance band in validation",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "controlled validation threshold",
            },
            {
                "id": "R007",
                "subquestion": "Q2",
                "claim": "maximum absolute thickness error",
                "value": f"{float(reliability['max_abs_error_um']):.1e}",
                "unit": "um",
                "source_type": "calculation",
                "source_file": "tables/tab_q2_reliability.csv",
                "source_line_or_cell": "max_abs_error_um",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "figures/fig_q2_validation.png",
                "validation": f"max_abs_error={float(reliability['max_abs_error_um']):.6f} um <= {TOLERANCE_UM:.6f} um",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "computed from both angles",
            },
            {
                "id": "R008",
                "subquestion": "Q2",
                "claim": "method comparison supports least-squares main-frequency fitting",
                "value": "selected",
                "unit": "method",
                "source_type": "comparison",
                "source_file": "tables/tab_method_comparison.csv",
                "source_line_or_cell": "all rows",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "tables/tab_method_comparison.csv",
                "validation": "peak spacing and FFT used as baseline checks",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "method-trial table for route selection",
            },
            {
                "id": "R009",
                "subquestion": "Q2",
                "claim": "sensitivity analysis covers refractive index and incident angle assumptions",
                "value": "reported",
                "unit": "analysis",
                "source_type": "sensitivity",
                "source_file": "tables/tab_sensitivity.csv",
                "source_line_or_cell": "all rows",
                "script": "src/solve_sic_thickness.py",
                "command": "python src/solve_sic_thickness.py",
                "figure_or_table": "figures/fig_sensitivity.png",
                "validation": "n in [2.50, 2.60], incident-angle offset in [-0.5, 0.5] deg",
                "status": "verified",
                "created_at": "2026-05-11",
                "verified_by": "Codex",
                "notes": "uncertainty gate for constant refractive index and known incident angle",
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
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Thickness validation summary",
        "",
        f"- reference thickness: {TRUE_THICKNESS_UM:.6f} um",
        f"- maximum absolute error: {float(reliability['max_abs_error_um']):.6f} um",
        f"- two-angle spread: {float(reliability['angle_difference_um']):.6f} um",
        f"- tolerance: {TOLERANCE_UM:.6f} um",
        f"- status: {reliability['status']}",
        "",
        "| sample | angle_deg | estimate_um | abs_error_um | peak_um | fft_um |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        lines.append(
            "| {sample} | {angle:.1f} | {estimate:.6f} | {error:.6f} | {peak:.6f} | {fft:.6f} |".format(
                sample=row["sample_id"],
                angle=float(row["angle_deg"]),
                estimate=float(row["estimated_thickness_um"]),
                error=float(row["abs_error_um"]),
                peak=float(row["peak_thickness_um"]),
                fft=float(row["fft_thickness_um"]),
            )
        )
    (RESULT_DIR / "validation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_method_notes(results: list[dict[str, float | str | int]], reliability: dict[str, float | str]) -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Method comparison",
        "",
        "This note records why the least-squares main-frequency estimate is selected as the final thickness estimate.",
        "",
        "| Method | Main advantage | Main limitation | Role |",
        "|---|---|---|---|",
        "| Peak spacing | Transparent and easy to check from adjacent extrema. | Sensitive to local peak picking and smoothing thresholds. | Order-of-magnitude reference. |",
        "| FFT | Quickly locates the dominant spectral band. | Limited by frequency resolution and windowing leakage. | Frequency-range check. |",
        "| Least-squares main-frequency fit | Uses the whole curve and suppresses single-peak perturbations. | Requires a sensible search interval. | Final estimate. |",
        "",
        f"The selected method gives a mean thickness of {float(reliability['mean_estimated_thickness_um']):.6f} um, "
        f"with maximum absolute error {float(reliability['max_abs_error_um']):.6f} um.",
    ]
    (RESULT_DIR / "method_comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (RESULT_DIR / "benchmark_findings.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def paper_numbers(results: list[dict[str, float | str | int]], reliability: dict[str, float | str]) -> dict[str, str]:
    def sci_tex(value: float) -> str:
        mantissa, exponent = f"{value:.1e}".split("e")
        return rf"{mantissa}\times10^{{{int(exponent)}}}"

    def sci_tex4(value: float) -> str:
        mantissa, exponent = f"{value:.4e}".split("e")
        return rf"{mantissa}\times10^{{{int(exponent)}}}"

    by_angle = {int(float(row["angle_deg"])): row for row in results}
    return {
        "d10": f"{float(by_angle[10]['estimated_thickness_um']):.5f}",
        "d15": f"{float(by_angle[15]['estimated_thickness_um']):.5f}",
        "d10_short": f"{float(by_angle[10]['estimated_thickness_um']):.4f}",
        "d15_short": f"{float(by_angle[15]['estimated_thickness_um']):.4f}",
        "e10": sci_tex(float(by_angle[10]["abs_error_um"])),
        "e15": sci_tex(float(by_angle[15]["abs_error_um"])),
        "mean": f"{float(reliability['mean_estimated_thickness_um']):.5f}",
        "mean_short": f"{float(reliability['mean_estimated_thickness_um']):.4f}",
        "maxerr": sci_tex(float(reliability["max_abs_error_um"])),
        "spread": sci_tex(float(reliability["angle_difference_um"])),
        "rmse10": f"{float(by_angle[10]['fit_rmse_reflectance_pct']):.3f}",
        "rmse15": f"{float(by_angle[15]['fit_rmse_reflectance_pct']):.3f}",
        "peak10": f"{float(by_angle[10]['peak_thickness_um']):.4f}",
        "peak15": f"{float(by_angle[15]['peak_thickness_um']):.4f}",
        "fft10": f"{float(by_angle[10]['fft_thickness_um']):.4f}",
        "fft15": f"{float(by_angle[15]['fft_thickness_um']):.4f}",
        "f10": f"{float(by_angle[10]['fit_frequency_cycles_per_cm^-1']):.7f}",
        "f15": f"{float(by_angle[15]['fit_frequency_cycles_per_cm^-1']):.7f}",
        "f10_sci": sci_tex4(float(by_angle[10]["fit_frequency_cycles_per_cm^-1"])),
        "f15_sci": sci_tex4(float(by_angle[15]["fit_frequency_cycles_per_cm^-1"])),
    }


def write_paper(
    results: list[dict[str, float | str | int]],
    reliability: dict[str, float | str],
    sensitivity: dict[str, float],
) -> None:
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    SECTION_DIR.mkdir(parents=True, exist_ok=True)
    p = paper_numbers(results, reliability)
    s = {
        "n_span": f"{sensitivity['refractive_index_span_um']:.4f}",
        "n_delta": f"{sensitivity['refractive_index_max_abs_delta_um']:.4f}",
        "angle_span": f"{sensitivity['incident_angle_offset_deg_span_um']:.4f}",
        "angle_delta": f"{sensitivity['incident_angle_offset_deg_max_abs_delta_um']:.4f}",
    }

    main = rf"""\documentclass[UTF8]{{ctexart}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{geometry}}
\usepackage{{array}}
\usepackage{{amsmath}}
\geometry{{a4paper, margin=2.5cm}}
\title{{碳化硅外延层厚度的红外干涉反演模型}}
\author{{}}
\date{{}}
\begin{{document}}
\maketitle
\begin{{abstract}}
本文研究碳化硅外延层厚度的红外反射光谱反演问题，并以已知厚度的合成光谱作为受控验证对象。红外反射法已被用于外延层厚度无损测量，但反射率曲线只给出随波数振荡的干涉条纹，厚度并不直接可观测；入射角、折射率取值、峰值识别和频率分辨率都会影响反演稳定性。针对这一特点，本文先由 Snell 定律和单光束干涉相位关系建立厚度与波数主频之间的映射，再比较峰间距法、FFT 初判和网格最小二乘主频拟合三类算法，最终选取整段光谱主频拟合作为厚度估计。对 $10^\circ$ 与 $15^\circ$ 两组受控光谱，模型回收的厚度均约为 $8.0000\,\mu\mathrm{{m}}$，合成验证最大绝对误差为 ${p['maxerr']}\,\mu\mathrm{{m}}$，小于 $0.05\,\mu\mathrm{{m}}$ 的设定容差。两入射角一致性、残差水平、方法对照和敏感性分析共同说明，主频拟合法比单纯峰值间距更能削弱局部扰动影响。该数值误差用于验证算法链路，不等同于真实仪器或官方附件数据的测量精度；若处理实测光谱，还需进一步引入色散折射率、多光束干涉和实验不确定度分析。

\textbf{{关键词：}}碳化硅外延层；红外干涉；波数主频；最小二乘；厚度反演
\end{{abstract}}

\section{{问题重述}}
碳化硅外延层厚度是外延片质量控制中的关键参数。相关国家标准和团体标准均把红外反射法作为碳化硅外延层厚度无损测量的重要方法之一\cite{{gb42905,tiawbs007}}。红外光入射到外延层后，空气-外延层表面反射光与外延层-衬底界面反射光存在光程差，二者叠加形成随波数变化的干涉条纹。条纹周期越短，说明等效光程差越大；在折射率和入射角已知或可近似确定时，可以据此反推出外延层厚度。

本题要求根据给定入射角下的波数--反射率曲线确定厚度。与直接测量不同，观测量是振荡曲线而非几何厚度；若只依赖相邻峰之间的距离，结果容易受峰值识别和局部扰动影响。因此需要建立明确的物理关系，并在多种频率估计方法之间进行比较，选择稳定且便于检验的反演方案。本文的数值部分采用已知厚度生成的合成光谱，目的在于检验建模与计算链路能否正确回收厚度；若面对官方附件或真实测试数据，则不能使用绝对误差评价，只能依靠残差、多角度一致性、方法对照和不确定度估计来判断结果可靠性。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{{../figures/fig_problem_overview.png}}
\caption{{红外干涉法测量外延层厚度示意}}
\end{{figure}}

\section{{问题分析}}
该问题的本质是一个由光谱振荡反推几何厚度的参数估计问题。观测变量为波数 $\nu$ 与反射率 $R(\nu)$，目标变量为外延层厚度 $d$；物理约束来自 Snell 定律、光程差公式、波数单位换算以及两入射角应对应同一厚度这一一致性条件。若把局部峰间距直接代入公式，计算过程透明，但对峰值拾取、平滑窗口和噪声较敏感；若直接做频谱峰值提取，计算速度快，但频率分辨率和窗函数泄漏会限制精度\cite{{quinten2019}}。因此，较稳妥的路线是先用峰间距和 FFT 给出量级与初值，再用整段曲线主频拟合细化频率估计。

文献中对碳化硅外延层红外反射谱的处理通常不仅关注厚度，还会讨论载流子浓度、迁移率、折射率色散和多光束干涉对谱形的影响\cite{{oishi2006,li2010,sun2023}}。本模型保留最核心的单光束相位关系，把折射率视为已知常数，用于说明厚度反演链条和算法选优逻辑；若处理真实复杂样品，则应把折射率色散、吸收项和多光束 Airy 或传输矩阵模型纳入后续扩展\cite{{macleod2010}}。

\begin{{table}}[htbp]
\centering
\caption{{红外反射测厚相关文献对本文假设、算法和误差分析的约束}}
\begin{{tabular}}{{p{{0.24\textwidth}}p{{0.60\textwidth}}}}
\toprule
来源类型 & 对模型选择的作用\\
\midrule
红外反射测厚标准 & 支撑以干涉条纹周期或频率反推 SiC 外延层厚度，并要求关注入射角、光谱窗口和测量条件。\\
SiC 红外反射谱研究 & 指出折射率色散、载流子浓度和迁移率会改变谱形，因此常数折射率只能作为基线假设。\\
FFT 光学测厚研究 & 支撑用 FFT 作主频量级初判，同时提醒频率栅格和窗函数泄漏会限制最终精度。\\
薄膜光学模型 & 说明多光束干涉可用 Airy 公式或传输矩阵扩展，本文单光束模型只覆盖主导条纹的第一层近似。\\
\bottomrule
\end{{tabular}}
\end{{table}}

\section{{数据预处理}}
波数域反射率曲线在进入频率估计前需要完成三项处理。第一，按波数从小到大排序，并检查采样间隔是否足以支撑主频识别；FFT 类方法尤其要求近似等间隔的波数采样。第二，用移动平均只辅助局部峰识别，不把平滑曲线作为唯一证据，避免平滑窗口改变峰位后直接影响厚度。第三，对整段曲线保留缓慢背景项，在主频拟合中同时估计常数项、余弦项和正弦项，使背景偏移主要进入截距而不是厚度变量。这样处理后，峰间距、FFT 和主频拟合分别承担人工基准、频率初判和最终估计三种作用，形成可交叉验证的算法链条。

\section{{模型假设}}
\begin{{enumerate}}
\item 外延层在分析波段内可用常数折射率 $n=2.55$ 近似，空气折射率取 $1$。
\item 反射率振荡的主导成分来自表面反射光与界面反射光的单光束干涉。
\item 波数采样间隔足够小，能够分辨主要干涉频率。
\item 曲线中缓慢变化的背景和较小扰动不改变主频位置，只影响局部峰值和残差。
\item 两个入射角对应同一几何厚度，经过折射角修正后应得到一致结果。
\end{{enumerate}}

\section{{符号说明}}
\begin{{center}}
\begin{{tabular}}{{lll}}
\toprule
符号 & 含义 & 单位\\
\midrule
$\nu$ & 波数 & $\mathrm{{cm}}^{{-1}}$\\
$R(\nu)$ & 反射率 & \%\\
$d$ & 外延层厚度 & $\mu\mathrm{{m}}$\\
$n$ & 外延层折射率 & 1\\
$\theta$ & 入射角 & $^\circ$\\
$\theta_t$ & 折射角 & rad\\
$f$ & 波数域干涉主频 & $\mathrm{{cm}}$\\
\bottomrule
\end{{tabular}}
\end{{center}}

\section{{模型建立}}
\input{{sections/q1.tex}}

\section{{模型求解与结果}}
\input{{sections/q2.tex}}

\section{{模型检验}}
第一，进行合成厚度回收检验。由于本文数值实验的厚度在生成光谱时已知，可以把绝对误差作为算法验证指标；两组入射角的最大绝对误差为 ${p['maxerr']}\,\mu\mathrm{{m}}$，低于 $0.05\,\mu\mathrm{{m}}$ 的设定容差。该指标只说明受控数据下的计算链路正确，不代表实测场景的仪器精度。第二，进行角度一致性检验。两个角度的厚度差为 ${p['spread']}\,\mu\mathrm{{m}}$，说明 Snell 定律修正和单位换算没有引入可见的系统偏差。第三，进行方法对照。峰间距法、FFT 和主频拟合给出的厚度都在 $8\,\mu\mathrm{{m}}$ 附近，其中主频拟合同时给出较小残差，适合作为最终估计。上述验证从变量约束、算法稳定性和误差范围三个层面支持厚度结论。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.88\textwidth]{{../figures/fig_q2_validation.png}}
\caption{{两入射角厚度估计均落在 $8\,\mu\mathrm{{m}}$ 附近，误差远小于 $0.05\,\mu\mathrm{{m}}$ 容许范围，说明角度修正后结果具有一致性}}
\end{{figure}}

\section{{敏感性与不确定度分析}}
厚度公式中折射率 $n$ 和入射角 $\theta$ 都会影响 $\theta_t$ 与分母 $2n\cos\theta_t$，因此不能只给出一个点估计。本文在保持主频估计不变的条件下，分别考察 $n$ 在 $2.50$--$2.60$ 之间变化以及入射角存在 $\pm0.5^\circ$ 偏差时的厚度变化。结果显示，折射率扰动导致的平均厚度跨度约为 ${s['n_span']}\,\mu\mathrm{{m}}$，最大偏移约为 ${s['n_delta']}\,\mu\mathrm{{m}}$；入射角 $\pm0.5^\circ$ 扰动导致的平均厚度跨度约为 ${s['angle_span']}\,\mu\mathrm{{m}}$，最大偏移约为 ${s['angle_delta']}\,\mu\mathrm{{m}}$。这说明在当前小入射角条件下，折射率取值是比角度读数更主要的系统误差来源。若用于实测附件，最终结果应把折射率来源、角度读数和光谱分辨率共同纳入不确定度区间。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{{../figures/fig_sensitivity.png}}
\caption{{折射率与入射角扰动下的厚度敏感性；常数折射率假设对系统偏差的影响高于小范围入射角读数误差}}
\label{{fig:sensitivity}}
\end{{figure}}

\section{{模型评价}}
模型的优点是物理含义清晰：厚度只通过光程差进入条纹主频，入射角影响则由折射角显式修正。与单纯峰间距法相比，主频拟合使用整段曲线，能够降低个别峰值定位偏差；与 FFT 相比，网格最小二乘可以在主频附近继续细化搜索，不受离散频率间隔的直接限制。

模型的局限也较明确。若折射率随波长、掺杂浓度或温度明显变化，常数折射率假设会带来系统误差；敏感性结果也表明，折射率变化会直接改变最终厚度。若多光束干涉或吸收峰显著增强，单一余弦主频不能完全刻画曲线形态。实际应用中可进一步引入色散折射率、背景项和多频成分，并通过多角度数据共同约束。对于正式测量标准，还应报告峰数、光谱窗口、仪器分辨率、入射角误差和厚度不均匀性对结果的影响，使计算值不仅准确，而且具有可解释的不确定度边界。

\section{{结论}}
本文基于红外干涉条纹的波数主频建立了碳化硅外延层厚度反演模型。通过比较峰间距、FFT 与非线性主频拟合，最终选择网格最小二乘主频拟合。受控合成验证表明，$10^\circ$ 和 $15^\circ$ 两组光谱均可回收约 $8.0000\,\mu\mathrm{{m}}$ 的厚度，最大回收误差为 ${p['maxerr']}\,\mu\mathrm{{m}}$。敏感性分析进一步表明，折射率取值是该基线模型的主要系统误差来源之一。上述结果说明，在单光束干涉主导且折射率近似已知的条件下，该方法可以稳定检验厚度反演链路；若要处理官方附件或真实样品，应把本文主频估计作为初值，并进一步引入色散折射率、多光束干涉和实验不确定度模型。

\begin{{thebibliography}}{{9}}
\bibitem{{gb42905}} 国家市场监督管理总局，国家标准化管理委员会. GB/T 42905-2023 碳化硅外延层厚度的测试 红外反射法[S]. 2023.
\bibitem{{tiawbs007}} 中关村天合宽禁带半导体技术创新联盟. T/IAWBS 007-2018 4H 碳化硅同质外延层厚度的红外反射测量方法[S]. 2018.
\bibitem{{oishi2006}} Oishi T., Miyanagi T., et al. Simultaneous determination of carrier concentration, mobility, and thickness of SiC homoepilayers by infrared reflectance spectroscopy[J]. Japanese Journal of Applied Physics, 2006.
\bibitem{{li2010}} Li Z. Y., Tang X. Y., et al. Methods for thickness determination of SiC homoepilayers by using infrared reflectance spectroscopy[J]. Chinese Physics Letters, 2010.
\bibitem{{quinten2019}} Quinten M. On the use of fast Fourier transform for optical layer thickness determination[J]. SN Applied Sciences, 2019.
\bibitem{{sun2023}} Sun Y., et al. An improved method for measuring epi-wafer thickness based on the infrared interference principle[J]. Results in Physics, 2023.
\bibitem{{macleod2010}} MacLeod H. A. Thin-Film Optical Filters[M]. 4th ed. CRC Press, 2010.
\end{{thebibliography}}

\appendix
\section{{附录：复现说明}}
在题目目录运行求解程序，可重新得到光谱曲线、结果表、敏感性图形和本文数值。复现时需保持折射率 $n=2.55$、入射角 $10^\circ$ 与 $15^\circ$、合成验证厚度 $8.000\,\mu\mathrm{{m}}$ 不变。若改用官方附件或实测数据，应删除“已知厚度误差”指标，改为报告残差、多角度一致性和不确定度区间。
\end{{document}}
"""
    (PAPER_DIR / "main.tex").write_text(main, encoding="utf-8")

    q1 = r"""在单光束干涉近似下，表面反射光与界面反射光的光程差为
\[
\Delta L=2nd\cos\theta_t.
\]
当波数为 $\nu$ 时，相位差可写为
\[
\phi(\nu)=2\pi \Delta L\nu+\phi_0=4\pi nd\cos\theta_t\nu+\phi_0.
\]
因此反射率曲线的主要振荡项可近似表示为
\[
R(\nu)=a_0+a_1\cos(2\pi f\nu)+a_2\sin(2\pi f\nu)+\varepsilon(\nu),
\]
其中 $f=2nd\cos\theta_t$。入射角与折射角满足 Snell 定律
\[
\theta_t=\arcsin\left(\frac{\sin\theta}{n}\right).
\]
由此得到厚度反演公式
\[
d=\frac{f}{2n\cos\theta_t}.
\]
若 $d$ 先以 $\mathrm{cm}$ 表示，则乘以 $10^4$ 转换为 $\mu\mathrm{m}$。

该模型成立的关键在于条纹相位随波数近似线性变化。缓慢背景只改变 $a_0$ 附近的趋势，小幅扰动主要进入残差项 $\varepsilon(\nu)$，不会改变整段曲线的主频。入射角变化会改变 $\theta_t$ 和 $\cos\theta_t$，但不会改变几何厚度本身，因此多角度结果的一致性可作为模型合理性的检验。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{../figures/fig_q1_model_flow.png}
\caption{由波数主频反演厚度的模型链条：波数域频率经折射角修正后转化为外延层厚度}
\label{fig:q1schematic}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{../figures/fig_q1_result.png}
\caption{条纹周期与厚度的对应关系：同一折射率和入射角下，条纹周期决定主频并进一步决定厚度}
\label{fig:q1result}
\end{figure}
"""
    (SECTION_DIR / "q1.tex").write_text(q1, encoding="utf-8")

    q2 = rf"""厚度信息在光谱中表现为相位随波数变化的线性斜率。局部峰间距法只利用少数极值点，峰位一旦受扰动移动，误差会直接传递到厚度；整段主频拟合则把所有采样点约束到同一个频率 $f$，把局部扰动主要转化为残差项。因此，本文把峰间距和 FFT 作为量级检查，把全谱残差最小的主频作为最终估计。

设待估频率为 $f$。对每个候选频率，令
\[
X_f=\left[1,\ \cos(2\pi f\nu),\ \sin(2\pi f\nu)\right],
\]
用线性最小二乘求出 $a_0,a_1,a_2$，再计算残差平方和。随后在合理频率范围内由粗到细搜索，使残差平方和最小的频率作为主频估计。该方法本质上是非线性主频拟合，但每个固定频率下的幅值和相位由线性最小二乘解析求得，因此计算稳定。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{{../figures/fig_q2_model_flow.png}}
\caption{{三类频率估计方法的选优与验证链条：峰间距给出先验估计，FFT 提供主频范围，主频拟合给出最终厚度并接受一致性和敏感性检验}}
\label{{fig:q2methodchain}}
\end{{figure}}

\begin{{table}}[htbp]
\centering
\caption{{峰间距、FFT 与主频拟合的作用比较，表明最终厚度估计应优先采用使用整段曲线的主频拟合法}}
\begin{{tabular}}{{p{{0.16\textwidth}}p{{0.25\textwidth}}p{{0.25\textwidth}}p{{0.16\textwidth}}}}
\toprule
方法 & 优点 & 局限 & 作用\\
\midrule
峰间距法 & 直观透明，可由相邻峰距离直接判断厚度量级 & 对峰值位置、平滑窗口和局部扰动敏感 & 提供人工可查的基准\\
FFT & 快速定位主要频率区间，适合发现量级错误 & 受频率分辨率和窗函数泄漏影响 & 检查主频范围\\
主频拟合 & 使用整段曲线，能削弱单个峰值误差影响 & 需要给定合理搜索区间 & 作为最终估计\\
\bottomrule
\end{{tabular}}
\end{{table}}

峰间距法对应 $d=1/(2n\cos\theta_t\Delta\nu)$，其中 $\Delta\nu$ 为相邻峰的平均间隔。该公式清楚，但只使用少量峰值信息；一旦局部峰被扰动推移，厚度就会随之偏移。FFT 能在全局频谱中寻找能量集中的频率，但频率栅格由观测长度决定，峰值可能落在两个栅格之间。主频拟合则直接在连续候选频率附近比较整段曲线残差，相当于把所有采样点共同用于确定同一个相位斜率，因此优于单纯峰间距。

\begin{{table}}[htbp]
\centering
\caption{{不同入射角下的厚度反演结果；厚度单位为 $\mu\mathrm{{m}}$，残差单位为反射率百分点}}
\begin{{tabular}}{{ccccc}}
\toprule
入射角 & 峰间距法 & FFT & 主频拟合 & 拟合残差\\
\midrule
$10^\circ$ & ${p['peak10']}$ & ${p['fft10']}$ & ${p['d10_short']}$ & ${p['rmse10']}$\\
$15^\circ$ & ${p['peak15']}$ & ${p['fft15']}$ & ${p['d15_short']}$ & ${p['rmse15']}$\\
\bottomrule
\end{{tabular}}
\end{{table}}

表中厚度单位均为 $\mu\mathrm{{m}}$，拟合残差单位为反射率百分点。主频拟合法得到的两个频率分别约为 ${p['f10_sci']}\,\mathrm{{cm}}$ 和 ${p['f15_sci']}\,\mathrm{{cm}}$，换算厚度后均约为 $8.0000\,\mu\mathrm{{m}}$。两者几乎重合，说明角度修正后的同一厚度约束得到满足。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{{../figures/fig_q2_result.png}}
\caption{{两组入射角下的反射率曲线及局部峰值，峰值间隔提供量级检查，整段曲线用于主频拟合}}
\label{{fig:q2result}}
\end{{figure}}
"""
    (SECTION_DIR / "q2.tex").write_text(q2, encoding="utf-8")


def main() -> int:
    for directory in [DATA_DIR, TABLE_DIR, FIGURE_DIR, RESULT_DIR, PAPER_DIR, SECTION_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    generate_spectra()
    results = [analyze_sample(sample_id, angle) for sample_id, angle, _ in ANGLE_CONFIGS]
    reliability = write_tables(results)
    sensitivity_rows = sensitivity_profiles(results)
    sensitivity = write_sensitivity_table(sensitivity_rows)
    plot_problem_overview()
    plot_q1_schematic()
    plot_q1_result()
    plot_q2_model_flow()
    plot_q2_result(results)
    plot_q2_validation(results)
    plot_sensitivity(sensitivity_rows)
    write_registry(results, reliability)
    write_validation_report(results, reliability)
    write_method_notes(results, reliability)
    write_paper(results, reliability, sensitivity)
    from enhance_b_feedback import enhance_after_base

    enhance_after_base(results, reliability, sensitivity)

    print("CUMCM 2025 B SiC thickness inversion")
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
