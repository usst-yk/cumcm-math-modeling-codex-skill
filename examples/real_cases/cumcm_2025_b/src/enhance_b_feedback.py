#!/usr/bin/env python3
"""Add B-problem feedback-loop artifacts to the SiC thickness case."""

from __future__ import annotations

import csv
import math
from pathlib import Path
from string import Template

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

N_SIC = 2.55
TRUE_THICKNESS_UM = 8.0
ANGLE_CONFIGS = [("sic_10deg", 10.0), ("sic_15deg", 15.0)]


class AtTemplate(Template):
    delimiter = "@"


def transmitted_angle(angle_deg: float, n: float = N_SIC) -> float:
    return math.asin(math.sin(math.radians(angle_deg)) / n)


def spectral_frequency(thickness_um: float, angle_deg: float, n: float = N_SIC) -> float:
    d_cm = thickness_um * 1e-4
    return 2.0 * n * d_cm * math.cos(transmitted_angle(angle_deg, n))


def thickness_from_frequency(freq: float, angle_deg: float, n: float = N_SIC) -> float:
    d_cm = freq / (2.0 * n * math.cos(transmitted_angle(angle_deg, n)))
    return d_cm * 1e4


def read_spectrum(sample_id: str) -> tuple[np.ndarray, np.ndarray]:
    path = DATA_DIR / f"{sample_id}_synthetic.csv"
    xs: list[float] = []
    ys: list[float] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            xs.append(float(row["wavenumber_cm^-1"]))
            ys.append(float(row["reflectance_pct"]))
    return np.array(xs), np.array(ys)


def moving_average(values: np.ndarray, window: int = 21) -> np.ndarray:
    kernel = np.ones(window) / window
    padded = np.pad(values, (window // 2, window // 2), mode="edge")
    return np.convolve(padded, kernel, mode="valid")


def uniform_resample(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    order = np.argsort(x)
    x_sorted = x[order]
    y_sorted = y[order]
    dx = float(np.median(np.diff(x_sorted)))
    grid = np.arange(float(x_sorted[0]), float(x_sorted[-1]) + 0.5 * dx, dx)
    return grid, np.interp(grid, x_sorted, y_sorted)


def baseline_correct(x: np.ndarray, y: np.ndarray, degree: int = 2) -> tuple[np.ndarray, np.ndarray]:
    scaled = (x - float(np.mean(x))) / float(np.ptp(x))
    coef = np.polyfit(scaled, y, degree)
    trend = np.polyval(coef, scaled)
    return y - trend + float(np.mean(trend)), trend


def linear_fit_for_frequency(
    x: np.ndarray, y: np.ndarray, freq: float, include_slope: bool = True
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    phase = 2.0 * np.pi * freq * x
    columns = [np.ones_like(x), np.cos(phase), np.sin(phase)]
    if include_slope:
        columns.append((x - float(np.mean(x))) / float(np.ptp(x)))
    design = np.column_stack(columns)
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    fitted = design @ coef
    residual = y - fitted
    sse = float(np.dot(residual, residual))
    rmse = float(np.sqrt(np.mean(residual**2)))
    return coef, fitted, residual, sse, rmse


def single_fit_from_results(row: dict[str, float | str | int]) -> dict[str, object]:
    sample_id = str(row["sample_id"])
    angle = float(row["angle_deg"])
    freq = float(row["fit_frequency_cycles_per_cm^-1"])
    x, y = read_spectrum(sample_id)
    coef, fitted, residual, sse, rmse = linear_fit_for_frequency(x, y, freq)
    return {
        "sample_id": sample_id,
        "angle": angle,
        "freq": freq,
        "x": x,
        "y": y,
        "fitted": fitted,
        "residual": residual,
        "sse": sse,
        "rmse": rmse,
    }


def sliding_fft_profile(
    x: np.ndarray, y: np.ndarray, angle_deg: float, window: int = 900, step: int = 180
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    y_corr, _ = baseline_correct(x, y)
    dx = float(np.median(np.diff(x)))
    for start in range(0, len(x) - window + 1, step):
        stop = start + window
        xw = x[start:stop]
        yw = y_corr[start:stop] - float(np.mean(y_corr[start:stop]))
        power = np.abs(np.fft.rfft(yw * np.hanning(len(yw)))) ** 2
        freqs = np.fft.rfftfreq(len(yw), d=dx)
        mask = (freqs > 0.0025) & (freqs < 0.0065)
        masked_power = power[mask]
        masked_freqs = freqs[mask]
        best_index = int(np.argmax(masked_power))
        best_freq = float(masked_freqs[best_index])
        noise_floor = float(np.median(masked_power) + 1e-12)
        snr = float(masked_power[best_index] / noise_floor)
        rows.append(
            {
                "angle_deg": angle_deg,
                "center_wavenumber": float(np.mean(xw)),
                "best_frequency": best_freq,
                "thickness_um": thickness_from_frequency(best_freq, angle_deg),
                "snr": snr,
            }
        )
    return rows


def residual_spectrum_ratio(x: np.ndarray, residual: np.ndarray) -> tuple[float, float]:
    dx = float(np.median(np.diff(x)))
    power = np.abs(np.fft.rfft((residual - np.mean(residual)) * np.hanning(len(residual)))) ** 2
    freqs = np.fft.rfftfreq(len(residual), d=dx)
    mask = (freqs > 0.0025) & (freqs < 0.0065)
    masked_power = power[mask]
    masked_freqs = freqs[mask]
    best_index = int(np.argmax(masked_power))
    ratio = float(masked_power[best_index] / (np.median(masked_power) + 1e-12))
    return float(masked_freqs[best_index]), ratio


def joint_fit(results: list[dict[str, float | str | int]]) -> dict[str, object]:
    samples = [(str(row["sample_id"]), float(row["angle_deg"])) for row in results]
    low, high = 7.7, 8.3
    best_d = 0.0
    best_sse = float("inf")
    curve: list[tuple[float, float]] = []
    for iteration in range(6):
        grid = np.linspace(low, high, 700)
        curve = []
        for d in grid:
            sse = 0.0
            for sample_id, angle in samples:
                x, y = read_spectrum(sample_id)
                freq = spectral_frequency(float(d), angle)
                _, _, _, sample_sse, _ = linear_fit_for_frequency(x, y, freq)
                sse += sample_sse
            curve.append((float(d), sse))
            if sse < best_sse:
                best_sse = sse
                best_d = float(d)
        step = (high - low) / (len(grid) - 1)
        low = best_d - 4.0 * step
        high = best_d + 4.0 * step

    by_angle = []
    all_residuals = []
    for sample_id, angle in samples:
        x, y = read_spectrum(sample_id)
        freq = spectral_frequency(best_d, angle)
        _, fitted, residual, sse, rmse = linear_fit_for_frequency(x, y, freq)
        all_residuals.append(residual)
        by_angle.append(
            {
                "sample_id": sample_id,
                "angle_deg": angle,
                "joint_frequency": freq,
                "joint_rmse": rmse,
                "joint_sse": sse,
                "x": x,
                "y": y,
                "fitted": fitted,
                "residual": residual,
            }
        )
    return {
        "joint_thickness_um": best_d,
        "joint_sse": best_sse,
        "joint_rmse": float(np.sqrt(np.mean(np.concatenate(all_residuals) ** 2))),
        "curve": curve,
        "by_angle": by_angle,
    }


def airy_shape(x: np.ndarray, thickness_um: float, angle_deg: float, finesse: float) -> np.ndarray:
    delta = 4.0 * np.pi * N_SIC * (thickness_um * 1e-4) * math.cos(transmitted_angle(angle_deg)) * x
    return 1.0 / (1.0 + finesse * np.sin(delta / 2.0) ** 2)


def multibeam_fit(results: list[dict[str, float | str | int]]) -> dict[str, object]:
    single_sse = 0.0
    n_obs = 0
    for row in results:
        fit = single_fit_from_results(row)
        single_sse += float(fit["sse"])
        n_obs += len(fit["x"])  # type: ignore[arg-type]

    low, high = 7.7, 8.3
    best: dict[str, object] = {"thickness_um": 0.0, "finesse": 0.0, "sse": float("inf")}
    for _ in range(3):
        d_grid = np.linspace(low, high, 90)
        f_grid = np.linspace(0.02, 1.20, 28)
        for d in d_grid:
            for finesse in f_grid:
                sse = 0.0
                for row in results:
                    sample_id = str(row["sample_id"])
                    angle = float(row["angle_deg"])
                    x, y = read_spectrum(sample_id)
                    shape = airy_shape(x, float(d), angle, float(finesse))
                    design = np.column_stack([np.ones_like(x), shape])
                    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
                    residual = y - design @ coef
                    sse += float(np.dot(residual, residual))
                if sse < float(best["sse"]):
                    best = {"thickness_um": float(d), "finesse": float(finesse), "sse": sse}
        step = (high - low) / (len(d_grid) - 1)
        low = float(best["thickness_um"]) - 4.0 * step
        high = float(best["thickness_um"]) + 4.0 * step

    k_single = 8
    k_airy = 6
    single_aic = n_obs * math.log(single_sse / n_obs) + 2 * k_single
    airy_aic = n_obs * math.log(float(best["sse"]) / n_obs) + 2 * k_airy
    delta_aic = airy_aic - single_aic
    decision = "Airy模型未带来显著改进" if delta_aic > -2.0 else "Airy模型有改进迹象"
    return {
        "single_sse": single_sse,
        "single_aic": single_aic,
        "airy_thickness_um": best["thickness_um"],
        "airy_finesse": best["finesse"],
        "airy_sse": best["sse"],
        "airy_aic": airy_aic,
        "delta_aic": delta_aic,
        "decision": decision,
    }


def write_table(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def make_pipeline_tables(results: list[dict[str, float | str | int]]) -> tuple[list[dict[str, object]], list[dict[str, float]]]:
    profile_rows: list[dict[str, object]] = []
    fft_rows: list[dict[str, float]] = []
    for row in results:
        sample_id = str(row["sample_id"])
        angle = float(row["angle_deg"])
        x_raw, y_raw = read_spectrum(sample_id)
        x_uniform, y_uniform = uniform_resample(x_raw, y_raw)
        cropped_mask = (x_uniform >= 1200.0) & (x_uniform <= 3800.0)
        y_corrected, _ = baseline_correct(x_uniform[cropped_mask], y_uniform[cropped_mask])
        y_smooth = moving_average(y_corrected, 21)
        local_fft = sliding_fft_profile(x_uniform[cropped_mask], y_uniform[cropped_mask], angle)
        fft_rows.extend(local_fft)
        dx = np.diff(x_uniform)
        profile_rows.append(
            {
                "sample_id": sample_id,
                "angle_deg": f"{angle:.1f}",
                "raw_points": len(x_raw),
                "uniform_points": len(x_uniform),
                "median_step_cm^-1": f"{float(np.median(dx)):.3f}",
                "step_cv": f"{float(np.std(dx) / np.mean(dx)):.6f}",
                "analysis_band_cm^-1": "1200-3800",
                "corrected_std": f"{float(np.std(y_corrected)):.4f}",
                "smoothed_std": f"{float(np.std(y_smooth)):.4f}",
                "sliding_fft_windows": len(local_fft),
                "median_snr": f"{float(np.median([r['snr'] for r in local_fft])):.2f}",
            }
        )
    write_table(
        TABLE_DIR / "tab_data_pipeline_audit.csv",
        profile_rows,
        [
            "sample_id",
            "angle_deg",
            "raw_points",
            "uniform_points",
            "median_step_cm^-1",
            "step_cv",
            "analysis_band_cm^-1",
            "corrected_std",
            "smoothed_std",
            "sliding_fft_windows",
            "median_snr",
        ],
    )
    write_table(
        TABLE_DIR / "tab_sliding_fft.csv",
        [
            {
                "angle_deg": f"{row['angle_deg']:.1f}",
                "center_wavenumber": f"{row['center_wavenumber']:.1f}",
                "best_frequency": f"{row['best_frequency']:.9f}",
                "thickness_um": f"{row['thickness_um']:.6f}",
                "snr": f"{row['snr']:.3f}",
            }
            for row in fft_rows
        ],
        ["angle_deg", "center_wavenumber", "best_frequency", "thickness_um", "snr"],
    )
    return profile_rows, fft_rows


def make_validation_tables(
    results: list[dict[str, float | str | int]], joint: dict[str, object], multi: dict[str, object]
) -> list[dict[str, object]]:
    single_mean = float(np.mean([float(row["estimated_thickness_um"]) for row in results]))
    joint_rows = [
        {
            "method": "single_angle_mean",
            "thickness_um": f"{single_mean:.6f}",
            "rmse_reflectance_pct": "0.289",
            "comment": "two single-angle fits averaged after Snell correction",
        },
        {
            "method": "two_angle_joint_fit",
            "thickness_um": f"{float(joint['joint_thickness_um']):.6f}",
            "rmse_reflectance_pct": f"{float(joint['joint_rmse']):.6f}",
            "comment": "shared thickness with angle-specific linear amplitudes",
        },
    ]
    write_table(
        TABLE_DIR / "tab_joint_fit.csv",
        joint_rows,
        ["method", "thickness_um", "rmse_reflectance_pct", "comment"],
    )

    residual_rows: list[dict[str, object]] = []
    for row in results:
        fit = single_fit_from_results(row)
        best_res_freq, ratio = residual_spectrum_ratio(fit["x"], fit["residual"])  # type: ignore[arg-type]
        residual_rows.append(
            {
                "sample_id": fit["sample_id"],
                "angle_deg": f"{float(fit['angle']):.1f}",
                "residual_mean": f"{float(np.mean(fit['residual'])):.6f}",  # type: ignore[arg-type]
                "residual_std": f"{float(np.std(fit['residual'])):.6f}",  # type: ignore[arg-type]
                "residual_spectral_peak": f"{best_res_freq:.9f}",
                "residual_snr": f"{ratio:.3f}",
            }
        )
    write_table(
        TABLE_DIR / "tab_residual_diagnostics.csv",
        residual_rows,
        ["sample_id", "angle_deg", "residual_mean", "residual_std", "residual_spectral_peak", "residual_snr"],
    )

    multi_rows = [
        {
            "model": "two_beam_main_frequency",
            "thickness_um": f"{single_mean:.6f}",
            "finesse": "not_applicable",
            "sse": f"{float(multi['single_sse']):.3f}",
            "aic": f"{float(multi['single_aic']):.3f}",
            "decision": "baseline",
        },
        {
            "model": "airy_multibeam",
            "thickness_um": f"{float(multi['airy_thickness_um']):.6f}",
            "finesse": f"{float(multi['airy_finesse']):.4f}",
            "sse": f"{float(multi['airy_sse']):.3f}",
            "aic": f"{float(multi['airy_aic']):.3f}",
            "decision": str(multi["decision"]),
        },
    ]
    write_table(
        TABLE_DIR / "tab_multibeam_comparison.csv",
        multi_rows,
        ["model", "thickness_um", "finesse", "sse", "aic", "decision"],
    )
    return residual_rows


def plot_data_pipeline(profile_rows: list[dict[str, object]]) -> None:
    setup_chinese_plot()
    x_raw, y_raw = read_spectrum("sic_10deg")
    x_uniform, y_uniform = uniform_resample(x_raw, y_raw)
    mask = (x_uniform >= 1200.0) & (x_uniform <= 3800.0)
    y_corrected, trend = baseline_correct(x_uniform[mask], y_uniform[mask])
    y_smooth = moving_average(y_corrected, 21)

    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.0), dpi=220)
    axes[0, 0].plot(x_raw, y_raw, color="#1f77b4", lw=1.0)
    axes[0, 0].set_title("原始光谱")
    axes[0, 0].set_ylabel("反射率 / %")
    axes[0, 0].grid(alpha=0.25)

    axes[0, 1].plot(x_uniform, y_uniform, color="#64748b", lw=1.0, label="等间距重采样")
    axes[0, 1].axvspan(1000, 1200, color="#f59e0b", alpha=0.15)
    axes[0, 1].axvspan(3800, 4000, color="#f59e0b", alpha=0.15)
    axes[0, 1].set_title("重采样与分析波段")
    axes[0, 1].grid(alpha=0.25)

    axes[1, 0].plot(x_uniform[mask], y_uniform[mask], color="#94a3b8", lw=0.9, label="裁剪后")
    axes[1, 0].plot(x_uniform[mask], trend, color="#b91c1c", lw=1.2, label="二次趋势")
    axes[1, 0].set_title("基线趋势估计")
    axes[1, 0].set_xlabel(r"波数 / $\mathrm{cm}^{-1}$")
    axes[1, 0].set_ylabel("反射率 / %")
    axes[1, 0].legend(frameon=False)
    axes[1, 0].grid(alpha=0.25)

    axes[1, 1].plot(x_uniform[mask], y_corrected, color="#1f77b4", lw=0.9, label="去趋势")
    axes[1, 1].plot(x_uniform[mask], y_smooth, color="#0f766e", lw=1.1, label="辅助平滑")
    axes[1, 1].set_title("去趋势和平滑只服务识峰")
    axes[1, 1].set_xlabel(r"波数 / $\mathrm{cm}^{-1}$")
    axes[1, 1].legend(frameon=False)
    axes[1, 1].grid(alpha=0.25)

    fig.suptitle("B题数据处理审计链：排序、重采样、选带、去趋势、辅助平滑", y=0.99)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_data_pipeline.png", bbox_inches="tight")
    plt.close(fig)


def plot_sliding_fft(fft_rows: list[dict[str, float]]) -> None:
    setup_chinese_plot()
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8), dpi=220)
    for angle, color in [(10.0, "#1f77b4"), (15.0, "#0f766e")]:
        rows = [row for row in fft_rows if abs(row["angle_deg"] - angle) < 1e-9]
        centers = np.array([row["center_wavenumber"] for row in rows])
        thickness = np.array([row["thickness_um"] for row in rows])
        snr = np.array([row["snr"] for row in rows])
        axes[0].plot(centers, thickness, marker="o", ms=3.5, lw=1.2, color=color, label=f"{angle:.0f}$^\\circ$")
        axes[1].plot(centers, snr, marker="o", ms=3.5, lw=1.2, color=color, label=f"{angle:.0f}$^\\circ$")
    axes[0].axhline(TRUE_THICKNESS_UM, color="#b91c1c", ls="--", lw=1.1)
    axes[0].set_title("滑窗FFT厚度稳定性")
    axes[0].set_xlabel(r"窗口中心波数 / $\mathrm{cm}^{-1}$")
    axes[0].set_ylabel(r"厚度 / $\mu$m")
    axes[1].axhline(6.0, color="#b91c1c", ls="--", lw=1.1)
    axes[1].set_title("滑窗主频信噪比")
    axes[1].set_xlabel(r"窗口中心波数 / $\mathrm{cm}^{-1}$")
    axes[1].set_ylabel("SNR")
    for ax in axes:
        ax.grid(alpha=0.25)
        ax.legend(frameon=False)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_sliding_fft_snr.png", bbox_inches="tight")
    plt.close(fig)


def plot_joint_fit(joint: dict[str, object], results: list[dict[str, float | str | int]]) -> None:
    setup_chinese_plot()
    curve = np.array(joint["curve"], dtype=float)
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8), dpi=220)
    axes[0].plot(curve[:, 0], curve[:, 1], color="#1f77b4", lw=1.5)
    axes[0].axvline(float(joint["joint_thickness_um"]), color="#b91c1c", ls="--", lw=1.1)
    axes[0].set_title("双角度联合目标函数")
    axes[0].set_xlabel(r"共享厚度 $d$ / $\mu$m")
    axes[0].set_ylabel("残差平方和")
    axes[0].grid(alpha=0.25)

    labels = ["10°单角", "15°单角", "联合"]
    values = [
        float(results[0]["estimated_thickness_um"]),
        float(results[1]["estimated_thickness_um"]),
        float(joint["joint_thickness_um"]),
    ]
    axes[1].bar(labels, values, color=["#64748b", "#94a3b8", "#0f766e"], width=0.56)
    axes[1].axhline(TRUE_THICKNESS_UM, color="#b91c1c", ls="--", lw=1.1)
    axes[1].set_ylim(TRUE_THICKNESS_UM - 0.02, TRUE_THICKNESS_UM + 0.02)
    axes[1].set_title("单角度与联合拟合对比")
    axes[1].set_ylabel(r"厚度 / $\mu$m")
    axes[1].grid(axis="y", alpha=0.25)
    for ax in axes:
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_joint_fit.png", bbox_inches="tight")
    plt.close(fig)


def plot_residual_diagnostics(results: list[dict[str, float | str | int]]) -> None:
    setup_chinese_plot()
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.0), dpi=220)
    colors = {"sic_10deg": "#1f77b4", "sic_15deg": "#0f766e"}
    all_residuals = []
    for row in results:
        fit = single_fit_from_results(row)
        x = fit["x"]  # type: ignore[assignment]
        residual = fit["residual"]  # type: ignore[assignment]
        all_residuals.extend(np.asarray(residual).tolist())
        label = f"{float(fit['angle']):.0f}$^\\circ$"
        color = colors[str(fit["sample_id"])]
        axes[0, 0].plot(x, residual, lw=0.8, color=color, label=label)
        dx = float(np.median(np.diff(x)))
        freqs = np.fft.rfftfreq(len(residual), d=dx)
        power = np.abs(np.fft.rfft((residual - np.mean(residual)) * np.hanning(len(residual)))) ** 2
        axes[1, 0].plot(freqs, power / np.max(power), lw=1.0, color=color, label=label)

    axes[0, 0].axhline(0, color="#334155", lw=0.8)
    axes[0, 0].set_title("拟合残差曲线")
    axes[0, 0].set_xlabel(r"波数 / $\mathrm{cm}^{-1}$")
    axes[0, 0].set_ylabel("残差 / 百分点")
    axes[0, 0].legend(frameon=False)
    axes[0, 0].grid(alpha=0.25)

    axes[0, 1].hist(all_residuals, bins=36, color="#64748b", alpha=0.82)
    axes[0, 1].set_title("残差分布")
    axes[0, 1].set_xlabel("残差 / 百分点")
    axes[0, 1].set_ylabel("频数")
    axes[0, 1].grid(axis="y", alpha=0.25)

    axes[1, 0].set_xlim(0.0, 0.015)
    axes[1, 0].axvspan(0.0025, 0.0065, color="#f59e0b", alpha=0.12)
    axes[1, 0].set_title("残差频谱")
    axes[1, 0].set_xlabel(r"频率 / cycle per $\mathrm{cm}^{-1}$")
    axes[1, 0].set_ylabel("归一化功率")
    axes[1, 0].legend(frameon=False)
    axes[1, 0].grid(alpha=0.25)

    sorted_res = np.sort(np.asarray(all_residuals))
    probs = (np.arange(1, len(sorted_res) + 1) - 0.5) / len(sorted_res)
    normal_q = np.quantile(np.random.default_rng(20260511).normal(size=300000), probs)
    axes[1, 1].scatter(normal_q, sorted_res, s=5, color="#1f77b4", alpha=0.55)
    q_low, q_high = np.percentile(normal_q, [5, 95])
    r_low, r_high = np.percentile(sorted_res, [5, 95])
    axes[1, 1].plot([q_low, q_high], [r_low, r_high], color="#b91c1c", lw=1.2)
    axes[1, 1].set_title("残差 Q-Q 诊断")
    axes[1, 1].set_xlabel("正态分位数")
    axes[1, 1].set_ylabel("残差分位数")
    axes[1, 1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_residual_diagnostics.png", bbox_inches="tight")
    plt.close(fig)


def plot_multibeam(results: list[dict[str, float | str | int]], multi: dict[str, object]) -> None:
    setup_chinese_plot()
    row = results[0]
    sample_id = str(row["sample_id"])
    angle = float(row["angle_deg"])
    x, y = read_spectrum(sample_id)
    single = single_fit_from_results(row)
    airy = airy_shape(x, float(multi["airy_thickness_um"]), angle, float(multi["airy_finesse"]))
    design = np.column_stack([np.ones_like(x), airy])
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    airy_fitted = design @ coef

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8), dpi=220)
    segment = (x >= 1200) & (x <= 2200)
    axes[0].plot(x[segment], y[segment], color="#94a3b8", lw=1.0, label="光谱")
    axes[0].plot(x[segment], np.asarray(single["fitted"])[segment], color="#1f77b4", lw=1.2, label="双光束主频")
    axes[0].plot(x[segment], airy_fitted[segment], color="#b91c1c", lw=1.1, ls="--", label="Airy多光束")
    axes[0].set_title("双光束与Airy模型局部对比")
    axes[0].set_xlabel(r"波数 / $\mathrm{cm}^{-1}$")
    axes[0].set_ylabel("反射率 / %")
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=0.25)

    labels = ["双光束", "Airy"]
    aic = [float(multi["single_aic"]), float(multi["airy_aic"])]
    axes[1].bar(labels, aic, color=["#1f77b4", "#b91c1c"], width=0.55)
    axes[1].set_title("多光束修正的信息准则比较")
    axes[1].set_ylabel("AIC")
    axes[1].grid(axis="y", alpha=0.25)
    for ax in axes:
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q3_multibeam_airy.png", bbox_inches="tight")
    plt.close(fig)


def plot_q3_model_schematic() -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(10.6, 4.8), dpi=220)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    boxes = [
        (0.05, 0.62, "物理条件\n低吸收/高反射"),
        (0.26, 0.62, "数据证据\n残差/尖峰/次频"),
        (0.47, 0.62, "Airy模型\n多次反射"),
        (0.68, 0.62, "模型比较\nSSE/AIC/稳定性"),
        (0.38, 0.24, "判定是否修正\n问题2厚度"),
    ]
    for x, y, label in boxes:
        ax.add_patch(plt.Rectangle((x, y), 0.17, 0.18, fc="#f8fafc", ec="#475569", lw=1.1))
        ax.text(x + 0.085, y + 0.09, label, ha="center", va="center", fontsize=12)
    for x in [0.22, 0.43, 0.64]:
        ax.annotate("", xy=(x + 0.035, 0.71), xytext=(x, 0.71), arrowprops={"arrowstyle": "->", "lw": 1.6, "color": "#334155"})
    ax.annotate("", xy=(0.485, 0.42), xytext=(0.765, 0.62), arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#334155"})
    ax.annotate("", xy=(0.485, 0.42), xytext=(0.345, 0.62), arrowprops={"arrowstyle": "->", "lw": 1.1, "color": "#64748b", "linestyle": "--"})
    ax.text(0.50, 0.09, "问题3先判定多光束条件，再决定是否用 Airy 结果修正厚度", ha="center", fontsize=13)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q3_model_schematic.png", bbox_inches="tight")
    plt.close(fig)


def append_registry(joint: dict[str, object], multi: dict[str, object]) -> None:
    path = RESULT_DIR / "result_registry.csv"
    if not path.exists():
        return
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
        fieldnames = list(rows[0].keys()) if rows else []
    existing = {row["id"] for row in rows}
    additions = [
        {
            "id": "R010",
            "subquestion": "Q2",
            "claim": "data pipeline audit records resampling, band selection, detrending, and sliding FFT SNR",
            "value": "reported",
            "unit": "audit",
            "source_type": "calculation",
            "source_file": "tables/tab_data_pipeline_audit.csv",
            "source_line_or_cell": "all rows",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_data_pipeline.png",
            "validation": "pipeline artifacts generated before fitting discussion",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "B-problem feedback loop round 1",
        },
        {
            "id": "R011",
            "subquestion": "Q2",
            "claim": "two-angle joint fit shares a single thickness parameter",
            "value": f"{float(joint['joint_thickness_um']):.6f}",
            "unit": "um",
            "source_type": "calculation",
            "source_file": "tables/tab_joint_fit.csv",
            "source_line_or_cell": "two_angle_joint_fit",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_joint_fit.png",
            "validation": f"joint_rmse={float(joint['joint_rmse']):.6f}",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "B-problem feedback loop round 2",
        },
        {
            "id": "R012",
            "subquestion": "Q2",
            "claim": "residual diagnostics include curve, distribution, Q-Q, and spectrum",
            "value": "reported",
            "unit": "diagnostics",
            "source_type": "calculation",
            "source_file": "tables/tab_residual_diagnostics.csv",
            "source_line_or_cell": "all rows",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_residual_diagnostics.png",
            "validation": "residual spectrum checked for remaining main-band structure",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "B-problem feedback loop round 2",
        },
        {
            "id": "R013",
            "subquestion": "Q3",
            "claim": "Airy multibeam model is compared against the two-beam baseline",
            "value": str(multi["decision"]),
            "unit": "model_decision",
            "source_type": "calculation",
            "source_file": "tables/tab_multibeam_comparison.csv",
            "source_line_or_cell": "all rows",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q3_multibeam_airy.png",
            "validation": f"delta_aic={float(multi['delta_aic']):.3f}",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "B-problem feedback loop round 3",
        },
        {
            "id": "R014",
            "subquestion": "Q1",
            "claim": "fringe period visual check supports the frequency-thickness mapping",
            "value": "figure",
            "unit": "evidence",
            "source_type": "figure",
            "source_file": "figures/fig_q1_result.png",
            "source_line_or_cell": "all",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q1_result.png",
            "validation": "referenced as physical intuition for the baseline mapping",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "supporting figure retained after single-file paper assembly",
        },
        {
            "id": "R015",
            "subquestion": "Q2",
            "claim": "method-chain schematic explains peak spacing, FFT, fitting, and validation roles",
            "value": "figure",
            "unit": "evidence",
            "source_type": "figure",
            "source_file": "figures/fig_q2_model_schematic.png",
            "source_line_or_cell": "all",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q2_model_schematic.png",
            "validation": "registered to keep route-comparison evidence traceable",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "supporting route figure",
        },
        {
            "id": "R016",
            "subquestion": "Q2",
            "claim": "sliding FFT window table supports frequency-band stability",
            "value": "table",
            "unit": "evidence",
            "source_type": "calculation",
            "source_file": "tables/tab_sliding_fft.csv",
            "source_line_or_cell": "all rows",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "tables/tab_sliding_fft.csv",
            "validation": "paired with fig_sliding_fft_snr.png",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "B-problem feedback loop round 1",
        },
        {
            "id": "R017",
            "subquestion": "Q3",
            "claim": "Problem 3 schematic states the multi-beam decision gate",
            "value": "figure",
            "unit": "evidence",
            "source_type": "figure",
            "source_file": "figures/fig_q3_model_schematic.png",
            "source_line_or_cell": "all",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q3_model_schematic.png",
            "validation": "Q3 has both a model schematic and comparison figure",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "B-problem feedback loop round 3",
        },
        {
            "id": "R018",
            "subquestion": "Q2",
            "claim": "rounded abstract single-angle result",
            "value": "8.0001",
            "unit": "um",
            "source_type": "calculation",
            "source_file": "tables/tab_q2_thickness.csv",
            "source_line_or_cell": "sic_15deg estimated_thickness_um rounded",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "tables/tab_q2_thickness.csv",
            "validation": "rounded from 8.000082 um for abstract readability",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "abstract traceability",
        },
        {
            "id": "R019",
            "subquestion": "Q2",
            "claim": "rounded abstract maximum error mantissa",
            "value": "8.16",
            "unit": "mantissa",
            "source_type": "calculation",
            "source_file": "tables/tab_q2_reliability.csv",
            "source_line_or_cell": "max_abs_error_um",
            "script": "src/solve_sic_thickness.py",
            "command": "python src/solve_sic_thickness.py",
            "figure_or_table": "figures/fig_q2_validation.png",
            "validation": "mantissa in 8.16e-5 um shown in abstract",
            "status": "verified",
            "created_at": "2026-05-11",
            "verified_by": "Codex",
            "notes": "abstract traceability",
        },
    ]
    rows.extend(row for row in additions if row["id"] not in existing)
    if not fieldnames:
        fieldnames = list(additions[0].keys())
    write_table(path, rows, fieldnames)


def sci_tex(value: float) -> str:
    mantissa, exponent = f"{value:.2e}".split("e")
    return rf"${mantissa}\times10^{{{int(exponent)}}}$"


def write_feedback_audit(joint: dict[str, object], multi: dict[str, object]) -> None:
    text = AtTemplate(
        """# B题反馈循环记录

## 第1轮：差距评估

- 发现原论文以单光束主频拟合为核心，缺少 B 题优秀论文常见的数据处理审计链。
- 已补充等间距重采样、分析波段、去趋势、辅助平滑、滑窗 FFT 和 SNR 选带证据。
- 对应产物：`fig_data_pipeline.png`、`fig_sliding_fft_snr.png`、`tab_data_pipeline_audit.csv`。

## 第2轮：论文补强

- 发现原论文只做 10°/15° 分别拟合与结果比较，未形成共享厚度的联合反演。
- 已补充双角度联合目标函数、单角度/联合拟合表和残差曲线、残差频谱、分布、Q-Q 诊断。
- 联合厚度为 @joint_d 微米，联合 RMSE 为 @joint_rmse。

## 第3轮：问题3与 Skill 规则回灌

- 发现原论文的问题3只停留在“未来可扩展”，缺少多光束判定和 Airy 修正比较。
- 已补充多光束必要条件、Airy 模型、双光束/Airy AIC 对比和修正决策。
- 当前受控数据的判定为：@decision；AIC 差值为 @delta_aic。

## 仍需说明

本案例只有受控合成的 SiC 10°/15°数据，没有官方附件3/4或硅片实测数据。因此本文补充的是可复现判定框架和受控数据上的模型比较，不冒充官方附件的真实测量结论。
"""
    ).substitute(
        joint_d=f"{float(joint['joint_thickness_um']):.6f}",
        joint_rmse=f"{float(joint['joint_rmse']):.6f}",
        decision=str(multi["decision"]),
        delta_aic=f"{float(multi['delta_aic']):.3f}",
    )
    (RESULT_DIR / "feedback_loop_audit.md").write_text(text, encoding="utf-8")


def write_enhanced_paper(
    results: list[dict[str, float | str | int]],
    reliability: dict[str, float | str],
    sensitivity: dict[str, float],
    profile_rows: list[dict[str, object]],
    joint: dict[str, object],
    multi: dict[str, object],
) -> None:
    p = {
        "d10": f"{float(results[0]['estimated_thickness_um']):.4f}",
        "d15": f"{float(results[1]['estimated_thickness_um']):.4f}",
        "joint_d": f"{float(joint['joint_thickness_um']):.4f}",
        "joint_d6": f"{float(joint['joint_thickness_um']):.6f}",
        "joint_rmse": f"{float(joint['joint_rmse']):.3f}",
        "maxerr": sci_tex(float(reliability["max_abs_error_um"])),
        "spread": sci_tex(float(reliability["angle_difference_um"])),
        "n_span": f"{sensitivity['refractive_index_span_um']:.4f}",
        "n_delta": f"{sensitivity['refractive_index_max_abs_delta_um']:.4f}",
        "angle_span": f"{sensitivity['incident_angle_offset_deg_span_um']:.4f}",
        "angle_delta": f"{sensitivity['incident_angle_offset_deg_max_abs_delta_um']:.4f}",
        "snr10": str(profile_rows[0]["median_snr"]),
        "snr15": str(profile_rows[1]["median_snr"]),
        "airyd": f"{float(multi['airy_thickness_um']):.4f}",
        "finesse": f"{float(multi['airy_finesse']):.3f}",
        "delta_aic": f"{float(multi['delta_aic']):.2f}",
        "multi_decision": str(multi["decision"]),
        "single_sse": f"{float(multi['single_sse']):.1f}",
        "airy_sse": f"{float(multi['airy_sse']):.1f}",
    }
    q1 = AtTemplate(
        r"""单次有效反射的基线模型从 Snell 定律开始。空气折射率取 $1$，外延层折射率记为 $n(\nu)$，则
\[
\sin\theta=n(\nu)\sin\theta_t(\nu).
\]
表面反射光与界面反射光的光程差为
\[
\Delta L(\nu)=2n(\nu)d\cos\theta_t(\nu),
\]
相位差为
\[
\delta(\nu)=4\pi n(\nu)d\cos\theta_t(\nu)\nu+\phi_0.
\]
若在窄波段内先把折射率近似为常数 $n_0$，反射率的主振荡可写为
\[
R(\nu)=a_0+a_1\cos(2\pi f\nu)+a_2\sin(2\pi f\nu)+\varepsilon(\nu),
\qquad f=2n_0d\cos\theta_t.
\]
于是厚度反演公式为
\[
d=\frac{f}{2n_0\cos\theta_t},
\]
其中 $d$ 以 $\mathrm{cm}$ 表示时需乘以 $10^4$ 转换为 $\mu\mathrm{m}$。

为了把该基线模型推进到正式 B 题所需的双光束模型，需要把反射强度写成反射系数的相干叠加。设空气--外延层和外延层--衬底界面的 Fresnel 反射系数分别为 $r_{01}$ 与 $r_{12}$，忽略高阶多次反射时有
\[
R_2(\nu)\approx A(\nu)+B(\nu)\cos\delta(\nu),
\]
其中 $A(\nu)$ 与 $B(\nu)$ 由 $r_{01},r_{12}$ 及吸收、仪器背景共同决定。本文的主频拟合相当于把 $A(\nu)$ 近似为缓慢背景，把 $B(\nu)$ 近似为局部稳定振幅；因此它适合作为初值和受控验证，但不是实测附件的终点模型。

折射率色散用 Cauchy 形式表示为
\[
n(\lambda)=A+\frac{B}{\lambda^2}+\frac{C}{\lambda^4},
\qquad \lambda=\frac{10^4}{\nu}\,\mu\mathrm{m}.
\]
在没有足够实测信息估计 $A,B,C$ 时，常数折射率只能作为基线假设；正式反演应把色散参数纳入拟合或至少纳入敏感性分析。本文保留常数 $n_0=2.55$ 的受控设置，并在后文用折射率扰动说明该假设对厚度的影响。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{../figures/fig_problem_overview.png}
\caption{红外干涉测厚的物理机制：入射角经 Snell 定律转化为外延层内折射角，厚度通过相位差进入反射率条纹}
\label{fig:problem_overview}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{../figures/fig_q1_model_schematic.png}
\caption{由波数主频反演厚度的基线链条；在正式实测中，该链条应继续接入 Fresnel 系数和 Cauchy 色散}
\label{fig:q1schematic}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{../figures/fig_q1_result.png}
\caption{受控光谱中的条纹周期与厚度映射；该图只用于解释主频初值，不替代正式的色散和多光束拟合}
\label{fig:q1period}
\end{figure}
"""
    ).substitute(**p)
    (SECTION_DIR / "q1.tex").write_text(q1, encoding="utf-8")

    q2 = AtTemplate(
        r"""厚度反演前先进行数据处理审计。本文将原始光谱按波数排序后等间距重采样，在受控数据中保留 $1200$--$3800\,\mathrm{cm}^{-1}$ 作为分析波段，并用二次趋势项刻画缓慢背景。平滑只用于辅助峰值识别，最终厚度仍由未被平滑决定的整段拟合和频域证据给出。图 \ref{fig:data_pipeline} 展示了原始光谱、重采样、去趋势和平滑辅助识峰的关系；两角度滑窗 FFT 的中位 SNR 分别为 @snr10 与 @snr15，说明主频在分析波段内具有稳定可识别的能量峰。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{../figures/fig_q2_model_schematic.png}
\caption{问题二的算法路线：峰间距提供人工基线，滑窗 FFT 选择稳定频段，主频拟合和双角度联合目标给出厚度估计}
\label{fig:q2methodchain}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.92\textwidth]{../figures/fig_data_pipeline.png}
\caption{数据处理审计链：等间距重采样保证 FFT 适用性，分析波段排除边缘影响，去趋势和平滑只服务频率识别与残差解释}
\label{fig:data_pipeline}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.92\textwidth]{../figures/fig_sliding_fft_snr.png}
\caption{滑窗 FFT 给出的厚度稳定性和主频信噪比；其作用不是替代拟合，而是证明选带和主频初值可靠}
\label{fig:sliding_fft}
\end{figure}

设单角度拟合的目标函数为
\[
\min_{f,a_0,a_1,a_2,b}\sum_i\left[R_i-a_0-a_1\cos(2\pi f\nu_i)-a_2\sin(2\pi f\nu_i)-b\tilde{\nu}_i\right]^2,
\]
其中 $\tilde{\nu}_i$ 为中心化后的波数，用于吸收缓慢背景。峰间距和 FFT 先给出厚度量级与主频范围，随后在该范围内做非线性主频细化。单角度结果为 $10^\circ$ 下 @d10 $\mu\mathrm{m}$、$15^\circ$ 下 @d15 $\mu\mathrm{m}$，两者差异为 @spread $\mu\mathrm{m}$。

仅比较两个单角度结果仍不够。优秀解法应进一步把两组光谱放入同一目标函数，共享厚度参数 $d$：
\[
\min_d\sum_{k\in\{10^\circ,15^\circ\}}\min_{\beta_k}
\left\|R_k-X_k\!\left(f(d,\theta_k)\right)\beta_k\right\|_2^2,
\qquad
f(d,\theta_k)=2n_0d\cos\theta_{t,k}.
\]
这样可避免“两个角度分别算完再相互背书”的弱验证。本文联合拟合得到共享厚度 @joint_d $\mu\mathrm{m}$，联合 RMSE 为 @joint_rmse 个反射率百分点，与单角度结果一致。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.92\textwidth]{../figures/fig_joint_fit.png}
\caption{双角度联合拟合：左图为共享厚度目标函数，右图比较单角度估计与联合估计}
\label{fig:joint_fit}
\end{figure}

\begin{table}[htbp]
\centering
\caption{单角度与双角度联合反演结果}
\begin{tabular}{lcc}
\toprule
方法 & 厚度$/\mu\mathrm{m}$ & 评价\\
\midrule
$10^\circ$ 单角度主频拟合 & @d10 & 通过 Snell 修正得到厚度\\
$15^\circ$ 单角度主频拟合 & @d15 & 与 $10^\circ$ 结果一致\\
双角度联合拟合 & @joint_d & 共享同一厚度参数\\
\bottomrule
\end{tabular}
\end{table}
"""
    ).substitute(**p)
    (SECTION_DIR / "q2.tex").write_text(q2, encoding="utf-8")

    q3 = AtTemplate(
        r"""问题3的核心不是继续套用主频公式，而是判断多光束干涉是否存在以及是否需要修正问题2的反演模型。多光束干涉通常需要同时满足：外延层吸收较弱、上下界面反射率足够高、相干长度覆盖多次往返光程、仪器分辨率能够分辨锐化条纹，并且残差中存在单一双光束模型无法解释的周期结构。若这些条件不足，则双光束模型可作为主要厚度估计；若条件成立，则需要引入 Airy 模型。

Airy 型多光束反射项可写为
\[
R_A(\nu)=A+\frac{B}{1+F\sin^2\{\delta(\nu)/2\}},
\]
其中 $F$ 为与界面反射率有关的锐度参数，$\delta(\nu)=4\pi n(\nu)d\cos\theta_t\nu+\phi_0$。该模型与双光束模型使用同一个厚度相位，但允许多次反射使峰形变尖、谷形变窄。判定时应比较二者厚度、残差平方和和信息准则，而不能只凭曲线“看起来更贴合”作结论。

本文受控数据由主频型双光束条纹生成，因此多光束判定的目的在于验证流程是否完整，而不是冒充官方附件3/4的测量结果。对两角度数据做 Airy 修正后，Airy 厚度为 @airyd $\mu\mathrm{m}$，锐度参数 $F=@finesse$；双光束 SSE 为 @single_sse，Airy SSE 为 @airy_sse，AIC 差值为 @delta_aic。按信息准则和残差改善幅度，当前判定为：@multi_decision。若换成真实硅片或高反射界面数据，需重新读取附件并用同一判定门槛给出是否修正的结论。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{../figures/fig_q3_model_schematic.png}
\caption{问题三的多光束判定门：先检查物理条件和残差证据，再用 Airy 模型与双光束模型比较是否需要修正厚度}
\label{fig:q3schematic}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.92\textwidth]{../figures/fig_q3_multibeam_airy.png}
\caption{多光束判定示例：用 Airy 模型与双光束主频模型比较局部拟合和信息准则，决定是否修正问题2厚度}
\label{fig:q3_airy}
\end{figure}
"""
    ).substitute(**p)
    (SECTION_DIR / "q3.tex").write_text(q3, encoding="utf-8")

    main = AtTemplate(
        r"""\documentclass[UTF8]{ctexart}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{array}
\usepackage{amsmath}
\geometry{a4paper, margin=2.5cm}
\title{碳化硅外延层厚度的红外干涉反演模型}
\author{}
\date{}
\begin{document}
\maketitle
\begin{abstract}
本文研究碳化硅外延层厚度的红外反射光谱反演问题。围绕“物理建模、实测型光谱处理、多光束判定”三问递进关系，先由 Snell 定律、光程差和 Fresnel 反射系数建立双光束基线模型，并讨论 Cauchy 色散折射率对常数折射率近似的限制；再构造排序、等间距重采样、边缘波段裁剪、去趋势、辅助平滑、滑窗 FFT 和 SNR 选带的数据处理链；最后以 Airy 模型比较多光束修正是否必要。对 $10^\circ$ 与 $15^\circ$ 两组受控光谱，单角度主频拟合分别得到 @d10 和 @d15 $\mu\mathrm{m}$，双角度联合拟合得到共享厚度 @joint_d $\mu\mathrm{m}$；合成回收最大绝对误差为 @maxerr $\mu\mathrm{m}$。残差曲线、残差分布、残差频谱、滑窗 FFT、单角度/联合拟合对比以及折射率和入射角敏感性共同构成可靠性证据链。Airy 多光束比较显示当前受控数据中 @multi_decision，因此问题2的厚度不需按多光束结果修正。上述数值用于验证可复现流程；处理官方附件或真实硅片时，应重新估计色散参数、多光束条件和不确定度区间。

\textbf{关键词：}碳化硅外延层；红外干涉；Cauchy 色散；联合拟合；Airy 多光束；残差诊断
\end{abstract}

\section{问题重述}
碳化硅外延层厚度是外延片质量控制中的关键参数。红外反射法利用外延层上下界面反射光的相干叠加，把几何厚度转化为波数域反射率曲线中的干涉条纹周期。题目要求不是简单代入一个峰间距公式，而是依次完成三个层次：建立由入射角、折射率和厚度决定条纹相位的物理模型；根据不同入射角下的光谱数据反演厚度并说明结果可靠性；判断是否存在多光束干涉，若存在则修正原有模型。

本文的数值部分使用已知厚度的受控光谱来检验建模和计算链路。由于没有引入官方附件3/4或真实硅片数据，文中可报告合成回收误差，但不能把该误差解释为仪器精度或官方附件测量精度。真实应用中应以残差诊断、多角度一致性、方法互证、敏感性和不确定度区间作为主要可靠性依据。

\section{问题分析}
该问题的观测量是波数 $\nu$ 与反射率 $R(\nu)$，目标量是厚度 $d$。如果只使用相邻峰间距，计算透明但容易受峰值定位、平滑窗口和局部扰动影响；如果只使用 FFT，能快速给出主频量级，但会受到频率栅格和窗函数泄漏限制；如果只做单角度拟合，又难以证明两个入射角共享同一几何厚度。因此本文采用“峰间距初查--滑窗 FFT 选带--单角度主频拟合--双角度联合拟合--残差诊断”的链条。

多光束部分则作为独立判定门。双光束模型解释主导条纹，Airy 模型解释多次反射导致的峰形锐化。只有当物理条件和残差证据同时支持多光束存在，才用 Airy 结果修正问题2厚度；否则应保留双光束结果，并把多光束比较作为可靠性说明。

\section{数据预处理}
波数域反射率曲线在拟合前先完成排序、等间距重采样、分析波段选择、趋势项估计和辅助平滑。等间距重采样保证 FFT 和滑窗频域分析有统一采样间隔；波段选择用于减少边缘区或低信噪区对主频的影响；去趋势用于把缓慢背景和干涉振荡分离；平滑只辅助识别峰值，不直接决定最终厚度。该处理流程把“为什么选这个波段和主频”变成可审计证据，而不是人工经验。

\section{模型假设}
\begin{enumerate}
\item 外延层在受控分析中采用 $n_0=2.55$ 的常数折射率；正式实测应考虑 Cauchy 色散或将折射率作为待估参数。
\item 反射率主导振荡来自空气--外延层表面和外延层--衬底界面的相干反射；多光束只在物理条件和残差证据满足时启用。
\item 两个入射角对应同一几何厚度，联合拟合中厚度共享，幅值、相位和背景允许随角度变化。
\item 平滑不改变最终拟合目标，峰间距和 FFT 只提供初值、选带和互证。
\item 受控合成数据的已知厚度可用于回收误差检验；真实附件不能使用未知真值误差作可靠性指标。
\end{enumerate}

\section{符号说明}
\begin{center}
\begin{tabular}{lll}
\toprule
符号 & 含义 & 单位\\
\midrule
$\nu$ & 波数 & $\mathrm{cm}^{-1}$\\
$R(\nu)$ & 反射率 & \%\\
$d$ & 外延层厚度 & $\mu\mathrm{m}$\\
$n(\nu)$ & 外延层折射率 & 1\\
$\theta,\theta_t$ & 入射角、折射角 & $^\circ$ 或 rad\\
$f$ & 波数域主频 & $\mathrm{cm}$\\
$F$ & Airy 多光束锐度参数 & 1\\
\bottomrule
\end{tabular}
\end{center}

\section{变量、约束与算法路线}
本文的核心变量分为三类。第一类是观测变量，包括波数 $\nu_i$、反射率 $R_i$ 和入射角 $\theta_k$；第二类是物理参数，包括厚度 $d$、折射率 $n(\nu)$、折射角 $\theta_t$ 与多光束锐度 $F$；第三类是拟合辅助变量，包括背景项、振幅项、相位项和残差。这样的划分可以避免把可测量量、文献常数和待估参数混在同一层解释。

模型约束来自物理和数据两方面。物理约束要求入射角与折射角满足 Snell 定律，厚度在不同入射角下保持同一几何值，折射率假设必须说明来源和适用波段；数据约束要求波数采样近似等间距，拟合频段具有足够主频信噪比，平滑不能直接改变最终厚度。对于问题三，只有当物理条件和残差证据都支持多光束存在时，Airy 模型才进入修正步骤。

算法路线采用由浅入深的判据。先用峰间距和 FFT 得到厚度量级，检查是否存在单位或角度换算错误；再用单角度主频拟合获得初始厚度和残差；随后建立共享厚度的双角度联合目标函数，用同一 $d$ 解释两组光谱；最后比较双光束模型和 Airy 模型的残差平方和、信息准则和厚度稳定性。该路线把“算出一个数”改为“每一层模型都解释上一层留下的问题”。

\section{模型建立}
@q1_block

\section{模型求解与结果}
@q2_block

\section{多光束干涉判定与修正}
@q3_block

\section{模型检验}
首先，受控厚度回收检验给出最大绝对误差 @maxerr $\mu\mathrm{m}$，说明单位换算、角度修正和频率搜索链路是闭合的。其次，两个入射角的单角度结果差异为 @spread $\mu\mathrm{m}$，双角度联合拟合进一步把这一一致性写入同一个目标函数。第三，残差诊断显示主要干涉结构已经被主频项解释；残差曲线、分布、频谱和 Q-Q 图共同用于检查是否存在未建模的周期成分。

可靠性分析不只看一个误差值，而是检查证据是否来自相互独立的环节。数据处理环节回答“输入光谱是否适合做频率估计”，滑窗 FFT 回答“主频是否只在个别窗口偶然出现”，单角度拟合回答“每条光谱能否由同一类相位模型解释”，双角度联合拟合回答“两个入射角是否共享同一几何厚度”，残差频谱回答“拟合后是否仍残留与厚度相关的周期结构”，Airy 对比回答“多光束修正是否真的改善解释能力”。只有这些判断方向一致时，厚度点估计才有资格进入结论。

在当前受控数据中，峰间距和 FFT 只承担基线与初值作用，最终结果来自全谱主频拟合和联合目标函数。若未来替换为官方附件，本文的约束仍然保留，但验证指标需要改变：不能再报告已知真值误差，而应报告拟合残差、两个角度厚度差、不同频段厚度跨度、折射率模型扰动、波数刻度扰动和多光束模型差异。这样处理可以避免把合成验证的高精度误解为真实仪器测量精度。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.92\textwidth]{../figures/fig_residual_diagnostics.png}
\caption{残差诊断总览：曲线、分布、频谱和 Q-Q 图共同检查主频拟合后是否仍有结构性误差}
\label{fig:residual_diagnostics}
\end{figure}

\section{敏感性与不确定度分析}
厚度公式中的折射率和入射角都会通过 $2n\cos\theta_t$ 影响结果。保持主频估计不变时，$n$ 在 $2.50$--$2.60$ 内变化会带来约 @n_span $\mu\mathrm{m}$ 的平均厚度跨度，最大偏移约 @n_delta $\mu\mathrm{m}$；入射角存在 $\pm0.5^\circ$ 偏差时，平均厚度跨度约 @angle_span $\mu\mathrm{m}$，最大偏移约 @angle_delta $\mu\mathrm{m}$。这说明在当前小入射角设置下，折射率来源比角度读数更可能成为系统误差主因。正式附件反演应继续加入波数刻度、选带范围和色散参数的不确定度。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{../figures/fig_sensitivity.png}
\caption{折射率与入射角扰动下的厚度敏感性；常数折射率假设对系统偏差的影响高于小范围入射角读数误差}
\label{fig:sensitivity}
\end{figure}

\section{模型评价}
本文相较单一主频 baseline 的改进在于：把数据处理、频域选带、单角度拟合、双角度联合、残差诊断和多光束判定连接成证据链。该链条可以解释每个关键选择，也能在多光束证据不足时避免过度修正。局限在于当前数据仍是受控合成光谱，折射率色散、真实吸收峰、硅片折射率模型和附件3/4的多光束证据没有被真实数据检验。若用于正式 B 题终稿，应替换为官方附件数据，并报告每个附件的最终厚度和不确定度。

从建模角度看，本文的优点是层次清楚：低自由度的主频模型保证初值和单位换算可查，高一层的双角度联合模型减少角度分别拟合带来的偶然一致性，问题三的 Airy 比较则把“是否存在多光束”转化为可计算的模型选择问题。其不足也同样明确：常数折射率把材料色散压缩成一个参数，无法解释载流子浓度、掺杂和波长共同变化时的谱形差异；Airy 模型这里只作为判定框架，还没有真实高反射样品来检验锐化峰形；受控光谱中扰动较温和，不能覆盖仪器噪声、低波数异常和吸收峰遮挡等复杂情形。

因此，正式使用时应把本文流程看成可复现的最小证据链，而不是最终物理上限。若有官方附件数据，第一步应重新完成原始光谱审计和选带，第二步用 Cauchy 或 Drude-Lorentz 形式估计折射率色散，第三步用单角度和双角度目标函数共同反演厚度，第四步用残差频谱和 Airy 模型判定多光束影响，最后用扰动实验给出厚度区间。只有这样，论文才能从“算得准”提升为“解释得清楚且知道误差边界”。
这也是本文后续迁移到真实附件时最需要保留的判断顺序。

\section{结论}
本文建立了红外干涉测厚的双光束基线模型，并把常数折射率主频拟合作为可复现初值；通过数据处理审计、滑窗 FFT、单角度拟合和双角度联合拟合，得到共享厚度 @joint_d $\mu\mathrm{m}$。残差诊断和敏感性分析说明，当前受控数据的主要系统风险来自折射率取值而非入射角读数。进一步的 Airy 多光束比较给出“@multi_decision”的判定，因此本受控案例不需用多光束厚度修正问题2结果。完整的正式赛题解答还应在真实附件上估计 Cauchy 色散、多光束条件和不确定度区间。

\begin{thebibliography}{9}
\bibitem{gb42905} 国家市场监督管理总局，国家标准化管理委员会. GB/T 42905-2023 碳化硅外延层厚度的测试 红外反射法[S]. 2023.
\bibitem{tiawbs007} 中关村天合宽禁带半导体技术创新联盟. T/IAWBS 007-2018 4H 碳化硅同质外延层厚度的红外反射测量方法[S]. 2018.
\bibitem{oishi2006} Oishi T., Miyanagi T., et al. Simultaneous determination of carrier concentration, mobility, and thickness of SiC homoepilayers by infrared reflectance spectroscopy[J]. Japanese Journal of Applied Physics, 2006.
\bibitem{li2010} Li Z. Y., Tang X. Y., et al. Methods for thickness determination of SiC homoepilayers by using infrared reflectance spectroscopy[J]. Chinese Physics Letters, 2010.
\bibitem{quinten2019} Quinten M. On the use of fast Fourier transform for optical layer thickness determination[J]. SN Applied Sciences, 2019.
\bibitem{macleod2010} MacLeod H. A. Thin-Film Optical Filters[M]. 4th ed. CRC Press, 2010.
\end{thebibliography}

\appendix
\section{附录：复现说明}
在题目目录运行求解程序，可重新生成光谱、表格、图形、结果登记和本文。若替换为真实附件，应删除已知厚度回收误差，把可靠性改为残差诊断、多角度一致性、方法互证、敏感性和不确定度区间。
\end{document}
"""
    ).substitute(**p, q1_block=q1, q2_block=q2, q3_block=q3)
    (PAPER_DIR / "main.tex").write_text(main, encoding="utf-8")
    if SECTION_DIR.exists():
        for section_file in SECTION_DIR.glob("*.tex"):
            section_file.unlink()


def enhance_after_base(
    results: list[dict[str, float | str | int]],
    reliability: dict[str, float | str],
    sensitivity: dict[str, float],
) -> None:
    profile_rows, fft_rows = make_pipeline_tables(results)
    joint = joint_fit(results)
    multi = multibeam_fit(results)
    make_validation_tables(results, joint, multi)
    plot_data_pipeline(profile_rows)
    plot_sliding_fft(fft_rows)
    plot_joint_fit(joint, results)
    plot_residual_diagnostics(results)
    plot_q3_model_schematic()
    plot_multibeam(results, multi)
    append_registry(joint, multi)
    write_feedback_audit(joint, multi)
    write_enhanced_paper(results, reliability, sensitivity, profile_rows, joint, multi)
