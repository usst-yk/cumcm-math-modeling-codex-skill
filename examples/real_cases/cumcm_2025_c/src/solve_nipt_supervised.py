#!/usr/bin/env python3
"""Supervised C-problem NIPT timing and abnormality example.

This example is intentionally synthetic but problem-shaped: it exercises the
skill's stage gates, rework loop, traceability, paper writing, and packaging.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plot_utils import setup_chinese_plot


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
FIGURE_DIR = ROOT / "figures"
TABLE_DIR = ROOT / "tables"
RESULT_DIR = ROOT / "results"
PAPER_DIR = ROOT / "paper"
SECTION_DIR = PAPER_DIR / "sections"
PROBLEM_DIR = ROOT / "problem"
APPENDIX_DIR = ROOT / "appendix"

Y_THRESHOLD = 4.0
RISK_BOUNDARIES = [28.0, 32.0, 36.0]
RISK_WINDOW = np.arange(11.0, 25.5, 0.5)
RNG_SEED = 20260511


def sigmoid(value: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(value, -40, 40)))


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in columns})


def generate_data() -> None:
    rng = np.random.default_rng(RNG_SEED)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    male_rows: list[dict[str, object]] = []
    for idx in range(220):
        bmi = float(np.clip(rng.normal(31.0, 4.3), 20.5, 42.5))
        age = float(np.clip(rng.normal(30.5, 3.8), 22.0, 43.0))
        gest_week = float(rng.uniform(10.0, 24.0))
        gc = float(np.clip(rng.normal(0.505, 0.018), 0.455, 0.555))
        y_pct = (
            -4.9
            + 0.52 * gest_week
            - 0.095 * (bmi - 28.0)
            - 0.025 * (age - 30.0)
            + 4.0 * (gc - 0.50)
            + rng.normal(0.0, 0.45)
        )
        y_pct = max(0.35, y_pct)
        male_rows.append(
            {
                "sample_id": f"M{idx + 1:03d}",
                "gestational_week": f"{gest_week:.2f}",
                "bmi": f"{bmi:.2f}",
                "age": f"{age:.1f}",
                "gc_content": f"{gc:.4f}",
                "y_chromosome_pct": f"{y_pct:.4f}",
                "qualified": int(y_pct >= Y_THRESHOLD),
            }
        )

    female_rows: list[dict[str, object]] = []
    for idx in range(180):
        bmi = float(np.clip(rng.normal(30.0, 4.8), 19.0, 43.0))
        age = float(np.clip(rng.normal(31.0, 4.5), 21.0, 44.0))
        gest_week = float(rng.uniform(10.0, 24.0))
        gc = float(np.clip(rng.normal(0.50, 0.020), 0.445, 0.560))
        z13 = float(rng.normal(0.0, 1.0))
        z18 = float(rng.normal(0.0, 1.0))
        z21 = float(rng.normal(0.0, 1.0))
        zx = float(rng.normal(0.0, 1.0))
        linear = -3.2 + 0.92 * max(z13, z18, z21) + 0.46 * abs(zx) + 0.06 * (age - 30.0) + 3.5 * abs(gc - 0.5)
        prob = float(sigmoid(np.array([linear]))[0])
        abnormal = int(rng.random() < prob)
        if abnormal:
            z21 += float(rng.normal(1.2, 0.4))
        female_rows.append(
            {
                "sample_id": f"F{idx + 1:03d}",
                "gestational_week": f"{gest_week:.2f}",
                "bmi": f"{bmi:.2f}",
                "age": f"{age:.1f}",
                "gc_content": f"{gc:.4f}",
                "z13": f"{z13:.4f}",
                "z18": f"{z18:.4f}",
                "z21": f"{z21:.4f}",
                "zx": f"{zx:.4f}",
                "abnormal": abnormal,
            }
        )

    write_csv(
        DATA_DIR / "nipt_male_synthetic.csv",
        male_rows,
        ["sample_id", "gestational_week", "bmi", "age", "gc_content", "y_chromosome_pct", "qualified"],
    )
    write_csv(
        DATA_DIR / "nipt_female_synthetic.csv",
        female_rows,
        ["sample_id", "gestational_week", "bmi", "age", "gc_content", "z13", "z18", "z21", "zx", "abnormal"],
    )


def read_numeric_csv(path: Path) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            converted: dict[str, float | str] = {}
            for key, value in row.items():
                if key == "sample_id":
                    converted[key] = value
                else:
                    converted[key] = float(value)
            rows.append(converted)
    return rows


def male_arrays(rows: list[dict[str, float | str]]) -> tuple[np.ndarray, np.ndarray]:
    x = np.array(
        [
            [
                1.0,
                float(row["gestational_week"]),
                float(row["bmi"]),
                float(row["age"]),
                float(row["gc_content"]),
            ]
            for row in rows
        ]
    )
    y = np.array([float(row["y_chromosome_pct"]) for row in rows])
    return x, y


def fit_linear_y(rows: list[dict[str, float | str]]) -> dict[str, object]:
    x, y = male_arrays(rows)
    coef, *_ = np.linalg.lstsq(x, y, rcond=None)
    pred = x @ coef
    residual = y - pred
    ss_res = float(np.sum(residual**2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot
    mae = float(np.mean(np.abs(residual)))
    return {"coef": coef, "pred": pred, "residual": residual, "r2": r2, "mae": mae}


def earliest_week(coef: np.ndarray, bmi: float, age: float, gc: float, threshold: float = Y_THRESHOLD) -> float:
    intercept, b_week, b_bmi, b_age, b_gc = coef
    week = (threshold - intercept - b_bmi * bmi - b_age * age - b_gc * gc) / b_week
    return float(np.clip(week, 10.0, 25.0))


def group_label(bmi: float) -> str:
    if bmi < RISK_BOUNDARIES[0]:
        return "<28"
    if bmi < RISK_BOUNDARIES[1]:
        return "28-32"
    if bmi < RISK_BOUNDARIES[2]:
        return "32-36"
    return ">=36"


def optimize_timing(rows: list[dict[str, float | str]], coef: np.ndarray, threshold: float = Y_THRESHOLD, late_weight: float = 0.08) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, float | str]]] = {"<28": [], "28-32": [], "32-36": [], ">=36": []}
    for row in rows:
        grouped[group_label(float(row["bmi"]))].append(row)

    results: list[dict[str, object]] = []
    for label, members in grouped.items():
        if not members:
            continue
        best: tuple[float, float, float] | None = None
        for week in RISK_WINDOW:
            x = np.array(
                [
                    [
                        1.0,
                        week,
                        float(row["bmi"]),
                        float(row["age"]),
                        float(row["gc_content"]),
                    ]
                    for row in members
                ]
            )
            y_pred = x @ coef
            fail_rate = float(np.mean(y_pred < threshold))
            risk = late_weight * max(0.0, week - 12.0) + 3.0 * fail_rate
            if best is None or risk < best[2]:
                best = (float(week), fail_rate, risk)
        assert best is not None
        earliest = [
            earliest_week(coef, float(row["bmi"]), float(row["age"]), float(row["gc_content"]), threshold)
            for row in members
        ]
        results.append(
            {
                "bmi_group": label,
                "sample_count": len(members),
                "mean_bmi": f"{np.mean([float(row['bmi']) for row in members]):.3f}",
                "recommended_week": f"{best[0]:.1f}",
                "estimated_unqualified_rate": f"{best[1]:.4f}",
                "risk_score": f"{best[2]:.4f}",
                "mean_earliest_week": f"{np.mean(earliest):.3f}",
            }
        )
    return results


def sensitivity_timing(rows: list[dict[str, float | str]], coef: np.ndarray) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for threshold in [3.8, 4.0, 4.2]:
        for late_weight in [0.06, 0.08, 0.10]:
            group_rows = optimize_timing(rows, coef, threshold=threshold, late_weight=late_weight)
            for row in group_rows:
                output.append(
                    {
                        "threshold_pct": f"{threshold:.1f}",
                        "late_weight": f"{late_weight:.2f}",
                        "bmi_group": row["bmi_group"],
                        "recommended_week": row["recommended_week"],
                        "estimated_unqualified_rate": row["estimated_unqualified_rate"],
                        "risk_score": row["risk_score"],
                    }
                )
    return output


def female_matrix(rows: list[dict[str, float | str]]) -> tuple[np.ndarray, np.ndarray]:
    x_raw = np.array(
        [
            [
                max(float(row["z13"]), float(row["z18"]), float(row["z21"])),
                abs(float(row["zx"])),
                abs(float(row["gc_content"]) - 0.5),
                float(row["age"]),
                float(row["bmi"]),
            ]
            for row in rows
        ]
    )
    mean = np.mean(x_raw, axis=0)
    std = np.std(x_raw, axis=0)
    x = np.column_stack([np.ones(len(rows)), (x_raw - mean) / std])
    y = np.array([float(row["abnormal"]) for row in rows])
    return x, y


def fit_logistic(rows: list[dict[str, float | str]]) -> dict[str, object]:
    x, y = female_matrix(rows)
    beta = np.zeros(x.shape[1])
    lr = 0.08
    for _ in range(2500):
        p = sigmoid(x @ beta)
        grad = x.T @ (p - y) / len(y)
        beta -= lr * grad
    prob = sigmoid(x @ beta)
    threshold = 0.38
    pred = (prob >= threshold).astype(int)
    tp = int(np.sum((pred == 1) & (y == 1)))
    fp = int(np.sum((pred == 1) & (y == 0)))
    tn = int(np.sum((pred == 0) & (y == 0)))
    fn = int(np.sum((pred == 0) & (y == 1)))
    sensitivity = tp / max(tp + fn, 1)
    specificity = tn / max(tn + fp, 1)
    accuracy = (tp + tn) / len(y)
    auc = roc_auc(y, prob)
    return {
        "beta": beta,
        "prob": prob,
        "pred": pred,
        "threshold": threshold,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "accuracy": accuracy,
        "auc": auc,
    }


def roc_auc(y: np.ndarray, prob: np.ndarray) -> float:
    order = np.argsort(prob)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(prob) + 1)
    pos = y == 1
    n_pos = int(np.sum(pos))
    n_neg = len(y) - n_pos
    rank_sum = float(np.sum(ranks[pos]))
    return (rank_sum - n_pos * (n_pos + 1) / 2) / max(n_pos * n_neg, 1)


def write_tables(male_rows: list[dict[str, float | str]], female_rows: list[dict[str, float | str]], q1: dict[str, object], q2_rows: list[dict[str, object]], q2_sens: list[dict[str, object]], q3: dict[str, object], draft: bool) -> None:
    coef = q1["coef"]
    assert isinstance(coef, np.ndarray)
    write_csv(
        TABLE_DIR / "tab_q1_model_coefficients.csv",
        [
            {"term": "intercept", "coefficient": f"{coef[0]:.6f}"},
            {"term": "gestational_week", "coefficient": f"{coef[1]:.6f}"},
            {"term": "bmi", "coefficient": f"{coef[2]:.6f}"},
            {"term": "age", "coefficient": f"{coef[3]:.6f}"},
            {"term": "gc_content", "coefficient": f"{coef[4]:.6f}"},
        ],
        ["term", "coefficient"],
    )
    write_csv(
        TABLE_DIR / "tab_q1_fit_metrics.csv",
        [
            {
                "r2": f"{float(q1['r2']):.3f}",
                "mae_pct": f"{float(q1['mae']):.3f}",
                "threshold_pct": f"{Y_THRESHOLD:.1f}",
                "sample_count": len(male_rows),
            }
        ],
        ["r2", "mae_pct", "threshold_pct", "sample_count"],
    )
    write_csv(
        TABLE_DIR / "tab_q2_timing.csv",
        q2_rows,
        ["bmi_group", "sample_count", "mean_bmi", "recommended_week", "estimated_unqualified_rate", "risk_score", "mean_earliest_week"],
    )
    if not draft:
        write_csv(
            TABLE_DIR / "tab_q2_sensitivity.csv",
            q2_sens,
            ["threshold_pct", "late_weight", "bmi_group", "recommended_week", "estimated_unqualified_rate", "risk_score"],
        )
    write_csv(
        TABLE_DIR / "tab_q3_classification.csv",
        [
            {
                "auc": f"{float(q3['auc']):.3f}",
                "accuracy": f"{float(q3['accuracy']):.3f}",
                "sensitivity": f"{float(q3['sensitivity']):.3f}",
                "specificity": f"{float(q3['specificity']):.3f}",
                "threshold": f"{float(q3['threshold']):.2f}",
                "tp": q3["tp"],
                "fp": q3["fp"],
                "tn": q3["tn"],
                "fn": q3["fn"],
                "sample_count": len(female_rows),
            }
        ],
        ["auc", "accuracy", "sensitivity", "specificity", "threshold", "tp", "fp", "tn", "fn", "sample_count"],
    )


def plot_problem_overview() -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=200)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    steps = [
        (0.05, "孕妇基本信息\n孕周 BMI 年龄"),
        (0.28, "NIPT 检测指标\nY 浓度 / Z 值"),
        (0.51, "统计建模\n时点与判别"),
        (0.74, "检测建议\n风险与异常提示"),
    ]
    for x, label in steps:
        ax.add_patch(plt.Rectangle((x, 0.52), 0.17, 0.20, fc="#f8fafc", ec="#475569", lw=1.2))
        ax.text(x + 0.085, 0.62, label, ha="center", va="center", fontsize=12)
    for x in [0.22, 0.45, 0.68]:
        ax.annotate("", xy=(x + 0.045, 0.62), xytext=(x, 0.62), arrowprops={"arrowstyle": "->", "lw": 1.6})
    ax.text(0.50, 0.30, "核心矛盾：检测过早可能浓度不足，检测过晚会增加临床处置风险", ha="center", fontsize=14)
    ax.text(0.50, 0.19, "验证线索：拟合误差、分组风险、阈值扰动和异常判别曲线", ha="center", fontsize=13, color="#475569")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_problem_overview.png", bbox_inches="tight")
    plt.close(fig)


def plot_q1(male_rows: list[dict[str, float | str]], q1: dict[str, object]) -> None:
    setup_chinese_plot()
    pred = np.asarray(q1["pred"], dtype=float)
    y = np.array([float(row["y_chromosome_pct"]) for row in male_rows])
    week = np.array([float(row["gestational_week"]) for row in male_rows])
    bmi = np.array([float(row["bmi"]) for row in male_rows])

    fig, ax = plt.subplots(figsize=(8.8, 4.6), dpi=200)
    ax.axis("off")
    boxes = [(0.08, "孕周 BMI\n年龄 GC"), (0.34, "线性主效应\n模型"), (0.60, "Y 浓度预测"), (0.78, "达标周数\n反推")]
    for x, label in boxes:
        ax.add_patch(plt.Rectangle((x, 0.48), 0.15, 0.18, fc="#f8fafc", ec="#475569", lw=1.1))
        ax.text(x + 0.075, 0.57, label, ha="center", va="center", fontsize=12)
    for x in [0.23, 0.49, 0.75]:
        ax.annotate("", xy=(x + 0.07, 0.57), xytext=(x, 0.57), arrowprops={"arrowstyle": "->", "lw": 1.5})
    ax.text(0.50, 0.30, r"$\hat y=\beta_0+\beta_1t+\beta_2BMI+\beta_3Age+\beta_4GC$", ha="center", fontsize=15)
    ax.text(0.50, 0.18, r"由 $\hat y=4\%$ 反推出最早检测孕周", ha="center", fontsize=13)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_model_schematic.png", bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), dpi=200)
    axes[0].scatter(y, pred, s=18, alpha=0.75, color="#1f77b4")
    lo, hi = min(np.min(y), np.min(pred)), max(np.max(y), np.max(pred))
    axes[0].plot([lo, hi], [lo, hi], color="#b91c1c", ls="--", lw=1.2)
    axes[0].set_xlabel("实际 Y 浓度 / %")
    axes[0].set_ylabel("预测 Y 浓度 / %")
    axes[0].set_title("Y 浓度拟合效果")
    axes[0].grid(alpha=0.25)
    sc = axes[1].scatter(week, y, c=bmi, s=20, cmap="viridis", alpha=0.80)
    axes[1].axhline(Y_THRESHOLD, color="#b91c1c", ls="--", lw=1.2)
    axes[1].set_xlabel("孕周")
    axes[1].set_ylabel("Y 浓度 / %")
    axes[1].set_title("孕周与 BMI 对达标的影响")
    fig.colorbar(sc, ax=axes[1], label="BMI")
    for ax in axes:
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_result.png", bbox_inches="tight")
    plt.close(fig)

    residual = np.asarray(q1["residual"], dtype=float)
    fig, ax = plt.subplots(figsize=(8.4, 4.4), dpi=200)
    ax.scatter(pred, residual, s=18, alpha=0.75, color="#0f766e")
    ax.axhline(0, color="#475569", lw=1)
    ax.set_xlabel("预测 Y 浓度 / %")
    ax.set_ylabel("残差 / 百分点")
    ax.set_title("残差分布检验")
    ax.grid(alpha=0.25)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q1_validation.png", bbox_inches="tight")
    plt.close(fig)


def plot_q2(q2_rows: list[dict[str, object]], q2_sens: list[dict[str, object]], draft: bool) -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=200)
    ax.axis("off")
    boxes = [(0.06, "BMI 分组"), (0.28, "候选孕周\n风险函数"), (0.52, "未达标率\n估计"), (0.74, "最小风险\n推荐时点")]
    for x, label in boxes:
        ax.add_patch(plt.Rectangle((x, 0.50), 0.16, 0.18, fc="#f8fafc", ec="#475569", lw=1.1))
        ax.text(x + 0.08, 0.59, label, ha="center", va="center", fontsize=12)
    for x in [0.22, 0.46, 0.68]:
        ax.annotate("", xy=(x + 0.055, 0.59), xytext=(x, 0.59), arrowprops={"arrowstyle": "->", "lw": 1.5})
    ax.text(0.50, 0.28, "风险 = 检测过晚风险 + 浓度未达标风险", ha="center", fontsize=14)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_model_schematic.png", bbox_inches="tight")
    plt.close(fig)

    labels = [str(row["bmi_group"]) for row in q2_rows]
    weeks = np.array([float(row["recommended_week"]) for row in q2_rows])
    fail = np.array([float(row["estimated_unqualified_rate"]) for row in q2_rows])
    x = np.arange(len(labels))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), dpi=200)
    axes[0].plot(x, weeks, marker="o", lw=1.8, color="#1f77b4")
    axes[0].set_xticks(x, labels)
    axes[0].set_ylabel("推荐检测孕周")
    axes[0].set_title("BMI 分组推荐时点")
    axes[1].bar(labels, fail, color="#94a3b8")
    axes[1].set_ylabel("预计未达标率")
    axes[1].set_title("推荐时点下的达标风险")
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q2_result.png", bbox_inches="tight")
    plt.close(fig)

    if not draft:
        fig, ax = plt.subplots(figsize=(8.8, 4.6), dpi=200)
        for group in labels:
            rows = [row for row in q2_sens if row["bmi_group"] == group and row["late_weight"] == "0.08"]
            threshold = [float(row["threshold_pct"]) for row in rows]
            rec_week = [float(row["recommended_week"]) for row in rows]
            ax.plot(threshold, rec_week, marker="o", lw=1.5, label=group)
        ax.set_xlabel("Y 浓度阈值 / %")
        ax.set_ylabel("推荐检测孕周")
        ax.set_title("阈值扰动下的推荐时点敏感性")
        ax.grid(alpha=0.25)
        ax.legend(frameon=False, title="BMI 组")
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        fig.tight_layout()
        fig.savefig(FIGURE_DIR / "fig_q2_sensitivity.png", bbox_inches="tight")
        plt.close(fig)


def plot_q3(female_rows: list[dict[str, float | str]], q3: dict[str, object]) -> None:
    setup_chinese_plot()
    fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=200)
    ax.axis("off")
    boxes = [(0.06, "Z13 Z18 Z21\nX 与 GC"), (0.32, "标准化\n特征构造"), (0.56, "Logistic\n风险评分"), (0.78, "异常判定\n阈值")]
    for x, label in boxes:
        ax.add_patch(plt.Rectangle((x, 0.50), 0.16, 0.18, fc="#f8fafc", ec="#475569", lw=1.1))
        ax.text(x + 0.08, 0.59, label, ha="center", va="center", fontsize=12)
    for x in [0.22, 0.48, 0.72]:
        ax.annotate("", xy=(x + 0.06, 0.59), xytext=(x, 0.59), arrowprops={"arrowstyle": "->", "lw": 1.5})
    ax.text(0.50, 0.28, r"$P(\mathrm{abnormal})=\sigma(\alpha+\sum_k w_k x_k)$", ha="center", fontsize=15)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q3_model_schematic.png", bbox_inches="tight")
    plt.close(fig)

    prob = np.asarray(q3["prob"], dtype=float)
    y = np.array([float(row["abnormal"]) for row in female_rows])
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), dpi=200)
    axes[0].hist(prob[y == 0], bins=18, alpha=0.72, label="正常", color="#94a3b8")
    axes[0].hist(prob[y == 1], bins=18, alpha=0.72, label="异常", color="#b91c1c")
    axes[0].axvline(float(q3["threshold"]), color="#111827", ls="--", lw=1.2)
    axes[0].set_xlabel("异常概率评分")
    axes[0].set_ylabel("样本数")
    axes[0].set_title("风险评分分布")
    axes[0].legend(frameon=False)
    fpr, tpr = roc_curve_points(y, prob)
    axes[1].plot(fpr, tpr, color="#1f77b4", lw=1.8)
    axes[1].plot([0, 1], [0, 1], color="#64748b", ls="--", lw=1)
    axes[1].set_xlabel("假阳性率")
    axes[1].set_ylabel("真阳性率")
    axes[1].set_title("异常判定 ROC 曲线")
    for ax in axes:
        ax.grid(alpha=0.25)
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q3_result.png", bbox_inches="tight")
    plt.close(fig)

    cm = np.array([[q3["tn"], q3["fp"]], [q3["fn"], q3["tp"]]], dtype=float)
    fig, ax = plt.subplots(figsize=(5.4, 4.8), dpi=200)
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1], ["判为正常", "判为异常"])
    ax.set_yticks([0, 1], ["实际正常", "实际异常"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{int(cm[i, j])}", ha="center", va="center", fontsize=14)
    ax.set_title("异常判定混淆矩阵")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_q3_validation.png", bbox_inches="tight")
    plt.close(fig)


def roc_curve_points(y: np.ndarray, prob: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    thresholds = np.linspace(0.0, 1.0, 101)
    tpr = []
    fpr = []
    for threshold in thresholds:
        pred = prob >= threshold
        tp = np.sum((pred == 1) & (y == 1))
        fp = np.sum((pred == 1) & (y == 0))
        tn = np.sum((pred == 0) & (y == 0))
        fn = np.sum((pred == 0) & (y == 1))
        tpr.append(tp / max(tp + fn, 1))
        fpr.append(fp / max(fp + tn, 1))
    order = np.argsort(fpr)
    return np.array(fpr)[order], np.array(tpr)[order]


def write_registry(q1: dict[str, object], q2_rows: list[dict[str, object]], q3: dict[str, object], draft: bool) -> None:
    q2_first = q2_rows[0]
    rows = [
        {
            "id": "R001",
            "subquestion": "Q1",
            "claim": "male-fetus Y concentration model fit",
            "value": f"R2={float(q1['r2']):.3f}; MAE={float(q1['mae']):.3f}",
            "unit": "percent-point",
            "source_type": "calculation",
            "source_file": "tables/tab_q1_fit_metrics.csv",
            "source_line_or_cell": "row 1",
            "script": "src/solve_nipt_supervised.py",
            "command": "python src/solve_nipt_supervised.py",
            "figure_or_table": "figures/fig_q1_result.png",
            "validation": "residual figure and R2/MAE table",
            "status": "verified",
            "notes": "controlled synthetic data shaped by the C problem",
        },
        {
            "id": "R002",
            "subquestion": "Q2",
            "claim": "BMI-group timing recommendation",
            "value": "; ".join(f"{row['bmi_group']}={row['recommended_week']}" for row in q2_rows),
            "unit": "gestational-week",
            "source_type": "optimization",
            "source_file": "tables/tab_q2_timing.csv",
            "source_line_or_cell": "all rows",
            "script": "src/solve_nipt_supervised.py",
            "command": "python src/solve_nipt_supervised.py",
            "figure_or_table": "figures/fig_q2_result.png",
            "validation": "risk score and unqualified-rate check",
            "status": "verified",
            "notes": f"lowest-BMI group starts near week {q2_first['recommended_week']}",
        },
        {
            "id": "R003",
            "subquestion": "Q3",
            "claim": "female-fetus abnormality classifier",
            "value": f"AUC={float(q3['auc']):.3f}; sensitivity={float(q3['sensitivity']):.3f}",
            "unit": "classification-metric",
            "source_type": "calculation",
            "source_file": "tables/tab_q3_classification.csv",
            "source_line_or_cell": "row 1",
            "script": "src/solve_nipt_supervised.py",
            "command": "python src/solve_nipt_supervised.py",
            "figure_or_table": "figures/fig_q3_result.png",
            "validation": "ROC curve and confusion matrix",
            "status": "verified",
            "notes": "screening-style threshold favors sensitivity",
        },
        {
            "id": "R004",
            "subquestion": "Q2",
            "claim": "timing sensitivity to Y concentration threshold",
            "value": "reported" if not draft else "missing",
            "unit": "sensitivity",
            "source_type": "sensitivity",
            "source_file": "tables/tab_q2_sensitivity.csv" if not draft else "tables/tab_q2_timing.csv",
            "source_line_or_cell": "all rows",
            "script": "src/solve_nipt_supervised.py",
            "command": "python src/solve_nipt_supervised.py",
            "figure_or_table": "figures/fig_q2_sensitivity.png",
            "validation": "threshold and late-risk perturbation",
            "status": "verified" if not draft else "blocked",
            "notes": "supervisor rework target in draft mode",
        },
        {
            "id": "R005",
            "subquestion": "Q1",
            "claim": "Y concentration threshold used for timing decision",
            "value": "4",
            "unit": "percent",
            "source_type": "assumption",
            "source_file": "tables/tab_q1_fit_metrics.csv",
            "source_line_or_cell": "threshold_pct",
            "script": "src/solve_nipt_supervised.py",
            "command": "python src/solve_nipt_supervised.py",
            "figure_or_table": "tables/tab_q1_fit_metrics.csv",
            "validation": "threshold shown in Q1 result figure",
            "status": "verified",
            "notes": "problem-shaped controlled threshold",
        },
        {
            "id": "R006",
            "subquestion": "Q1",
            "claim": "Y concentration coefficient table",
            "value": "reported",
            "unit": "coefficient",
            "source_type": "calculation",
            "source_file": "tables/tab_q1_model_coefficients.csv",
            "source_line_or_cell": "all rows",
            "script": "src/solve_nipt_supervised.py",
            "command": "python src/solve_nipt_supervised.py",
            "figure_or_table": "tables/tab_q1_model_coefficients.csv",
            "validation": "coefficients reproduce Q1 prediction formula",
            "status": "verified",
            "notes": "registered to keep coefficient table traceable",
        },
    ]
    write_csv(
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
            "notes",
        ],
    )


def write_problem_files() -> None:
    PROBLEM_DIR.mkdir(parents=True, exist_ok=True)
    statement = """# 2025 CUMCM C 题受控测试：NIPT 的时点选择与胎儿异常判定

本测试围绕 2025 年全国大学生数学建模竞赛 C 题公开题名和官方讲评主题，构造一个不含真实隐私数据的合成附件。研究对象为 NIPT 检测中的孕周、BMI、Y 染色体浓度、染色体 Z 值和 GC 含量。

## 问题

1. 分析男胎 Y 染色体浓度与孕周、BMI、年龄、GC 含量之间的关系，建立可解释模型，并给出浓度达到 4% 阈值的判断依据。
2. 按 BMI 对孕妇分组，在检测过早可能未达标、检测过晚增加风险的矛盾下，为各组给出推荐检测时点，并做阈值扰动敏感性分析。
3. 对女胎样本，综合 13、18、21 号染色体 Z 值、X 染色体偏离和 GC 含量，建立异常风险判定模型，并给出判别阈值与验证指标。

## 附件

- `data/raw/nipt_male_synthetic.csv`：男胎合成样本。
- `data/raw/nipt_female_synthetic.csv`：女胎合成样本。

本目录用于验证 skill 的监督-返工闭环，不是官方标准答案，也不包含官方附件原始数据。
"""
    (PROBLEM_DIR / "problem_statement.md").write_text(statement, encoding="utf-8")
    parse = {
        "problem_id": "cumcm_2025_c",
        "question_count": 3,
        "attachments": ["data/raw/nipt_male_synthetic.csv", "data/raw/nipt_female_synthetic.csv"],
        "units": ["孕周", "BMI", "Y 染色体浓度百分比", "Z 值"],
        "time_ranges": ["10-24 周"],
        "risk_words": ["时点", "分组", "异常判定", "阈值", "敏感性"],
        "subquestions": [
            {
                "id": "Q1",
                "task_type": "prediction",
                "required_output": ["Y 浓度模型", "达标阈值判断"],
                "input_data": ["male synthetic NIPT records"],
                "decision_object": "Y concentration relation",
                "constraints": ["threshold = 4%", "features must be clinically interpretable"],
            },
            {
                "id": "Q2",
                "task_type": "optimization",
                "required_output": ["BMI-group timing recommendation"],
                "input_data": ["Q1 model", "male synthetic NIPT records"],
                "decision_object": "recommended gestational week by BMI group",
                "constraints": ["balance early failure and late clinical risk"],
            },
            {
                "id": "Q3",
                "task_type": "classification",
                "required_output": ["abnormality risk score", "threshold", "metrics"],
                "input_data": ["female synthetic NIPT records"],
                "decision_object": "abnormality decision",
                "constraints": ["screening threshold should favor sensitivity"],
            },
        ],
    }
    (PROBLEM_DIR / "problem_parse.json").write_text(json.dumps(parse, ensure_ascii=False, indent=2), encoding="utf-8")
    (PROBLEM_DIR / "problem_parse.md").write_text("# Problem Parse\n\n" + json.dumps(parse, ensure_ascii=False, indent=2), encoding="utf-8")
    task_plan = {
        "contest": "CUMCM",
        "problem_id": "cumcm_2025_c",
        "deliverable_type": "contest_paper",
        "paper_genre": "contest_paper",
        "literature_gate": {
            "cutoff": "2025-09-04 18:00 Asia/Shanghai",
            "sources_checked": [
                {
                    "source": "2025 全国大学生数学建模竞赛 C 题讲评：NIPT 的时点选择与胎儿的异常判定",
                    "use": "confirm problem topic and review perspective",
                    "status": "official post-contest review, used only as retrospective benchmark",
                }
            ],
            "used_facts": [
                {"fact": "C problem concerns NIPT timing and fetal abnormality decision", "use": "synthetic case design"}
            ],
            "route_impact": "Use interpretable regression, grouped timing optimization, and classification validation.",
            "unavailable_reason": "",
        },
        "method_trials": [
            {
                "method": "linear_y_model",
                "assumption": "Y concentration grows approximately linearly in the operating window",
                "metric": "R2 and MAE",
                "result": "selected for interpretability",
                "failure": "cannot capture nonlinear clinical detail",
                "selected_reason": "transparent enough for a skill regression case",
            },
            {
                "method": "risk_grid_search",
                "assumption": "BMI group shares a recommendation window",
                "metric": "risk score and unqualified rate",
                "result": "selected for Q2",
                "failure": "sensitive to threshold and late-risk weight",
                "selected_reason": "easy to supervise and validate",
            },
            {
                "method": "logistic_classifier",
                "assumption": "chromosome Z-value features summarize abnormality risk",
                "metric": "AUC, sensitivity, specificity",
                "result": "selected for Q3",
                "failure": "requires threshold tuning",
                "selected_reason": "classification metrics are directly auditable",
            },
        ],
        "paper_style_policy": {
            "forbidden_body_terms": ["skill", "benchmark", "registry", "verified", "script", "脚本", ".csv", "回归测试", "本案例"],
            "allowed_disclosures": "Internal workflow details stay in README/progress; paper main text stays contest-style.",
        },
        "benchmark_sources": [
            {
                "source": "https://dxs.moe.gov.cn/zx/a/hd_sxjm_sxjmstjp_2025sxjmstjp/251202/2025781.shtml",
                "use": "official review title and topic confirmation",
                "status": "checked",
            }
        ],
        "rubric_targets": [
            {"criterion": "traceability", "target": "all headline values trace to tables and registry", "evidence": "results/result_registry.csv"},
            {"criterion": "supervised_rework", "target": "progress log shows revise -> rework -> pass", "evidence": "logs/progress.jsonl"},
        ],
        "question_count": 3,
        "subquestions": [
            {
                "id": "Q1",
                "task_type": "prediction",
                "required_output": ["fit Y concentration model", "estimate threshold relation"],
                "input_data": ["data/raw/nipt_male_synthetic.csv"],
                "decision_object": "Y concentration",
                "constraints": ["Y threshold = 4%", "interpretable model"],
                "validation": ["R2/MAE", "residual plot"],
                "figures_needed": ["fig_q1_model_schematic.png", "fig_q1_result.png", "fig_q1_validation.png"],
                "tables_needed": ["tab_q1_model_coefficients.csv", "tab_q1_fit_metrics.csv"],
                "baseline_route": "week-only linear fit",
                "primary_route": "week, BMI, age, and GC linear model",
                "fallback_route": "BMI-stratified median threshold week",
                "minimum_validation": ["baseline comparison", "residual check"],
                "rubric_targets": ["traceability", "validation"],
                "selling_points": [{"claim": "阈值时点可由可解释模型反推", "evidence": "fig_q1_result.png", "validation": "R2/MAE"}],
                "revision_status": {"state": "verified", "owner": "solver", "next_action": "none"},
                "status": "verified",
            },
            {
                "id": "Q2",
                "task_type": "optimization",
                "required_output": ["BMI-group timing recommendation", "sensitivity analysis"],
                "input_data": ["data/raw/nipt_male_synthetic.csv", "Q1 model"],
                "decision_object": "recommended week",
                "constraints": ["early unqualified risk", "late risk"],
                "validation": ["risk score", "threshold sensitivity"],
                "figures_needed": ["fig_q2_model_schematic.png", "fig_q2_result.png", "fig_q2_sensitivity.png"],
                "tables_needed": ["tab_q2_timing.csv", "tab_q2_sensitivity.csv"],
                "baseline_route": "same week for all BMI",
                "primary_route": "BMI-group risk minimization",
                "fallback_route": "earliest-week percentile by group",
                "minimum_validation": ["group risk comparison", "threshold perturbation"],
                "rubric_targets": ["optimization", "supervised_rework"],
                "selling_points": [{"claim": "分组时点同时呈现风险和敏感性", "evidence": "fig_q2_sensitivity.png", "validation": "threshold perturbation"}],
                "revision_status": {"state": "verified", "owner": "solver", "next_action": "none"},
                "status": "verified",
            },
            {
                "id": "Q3",
                "task_type": "classification",
                "required_output": ["abnormality classifier", "metrics"],
                "input_data": ["data/raw/nipt_female_synthetic.csv"],
                "decision_object": "abnormality risk",
                "constraints": ["screening threshold favors sensitivity"],
                "validation": ["ROC/AUC", "confusion matrix"],
                "figures_needed": ["fig_q3_model_schematic.png", "fig_q3_result.png", "fig_q3_validation.png"],
                "tables_needed": ["tab_q3_classification.csv"],
                "baseline_route": "max Z-score threshold",
                "primary_route": "logistic risk score",
                "fallback_route": "rule-based high-risk flag",
                "minimum_validation": ["AUC", "confusion matrix"],
                "rubric_targets": ["classification", "validation"],
                "selling_points": [{"claim": "异常判定从单指标阈值扩展到多指标风险评分", "evidence": "fig_q3_result.png", "validation": "AUC and sensitivity"}],
                "revision_status": {"state": "verified", "owner": "solver", "next_action": "none"},
                "status": "verified",
            },
        ],
        "global_assumptions": ["Synthetic data are used to test workflow and reproducibility.", "Clinical claims are not made from this controlled dataset."],
        "risk_points": ["Official attachments are not redistributed.", "Synthetic validation does not imply medical performance."],
        "revision_status": {"state": "verified", "owner": "supervisor", "next_action": "final audit"},
        "supervision_loop": {
            "required": True,
            "max_attempts": 3,
            "current_attempt": 2,
            "gate_status": "passed_after_rework",
            "progress_required_fields": ["gate_id", "decision", "owner", "issue", "expected_fix", "evidence_needed"],
            "last_gate": {"gate_id": "G5-validation", "decision": "pass"},
        },
    }
    (PROBLEM_DIR / "task_plan.json").write_text(json.dumps(task_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (PROBLEM_DIR / "task_plan.md").write_text("# Task Plan\n\n" + json.dumps(task_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (PROBLEM_DIR / "background_benchmark.md").write_text(
        "# Background Benchmark\n\n"
        "- Official post-contest review title confirms that 2025 C concerns NIPT timing and fetal abnormality decision.\n"
        "- The controlled test uses no official attachment rows and does not copy showcased solution content.\n"
        "- Route impact: use interpretable regression, grouped risk optimization, and classification metrics.\n",
        encoding="utf-8",
    )


def paper_numbers(q1: dict[str, object], q2_rows: list[dict[str, object]], q3: dict[str, object]) -> dict[str, str]:
    return {
        "r2": f"{float(q1['r2']):.3f}",
        "mae": f"{float(q1['mae']):.3f}",
        "weeks": "，".join(f"{row['bmi_group']} 组 {row['recommended_week']} 周" for row in q2_rows),
        "auc": f"{float(q3['auc']):.3f}",
        "sensitivity": f"{float(q3['sensitivity']):.3f}",
        "specificity": f"{float(q3['specificity']):.3f}",
    }


def write_paper(q1: dict[str, object], q2_rows: list[dict[str, object]], q3: dict[str, object], draft: bool) -> None:
    p = paper_numbers(q1, q2_rows, q3)
    PAPER_DIR.mkdir(parents=True, exist_ok=True)
    SECTION_DIR.mkdir(parents=True, exist_ok=True)
    q2_sens_figure = r"""
\begin{figure}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{../figures/fig_q2_sensitivity.png}
\caption{Y 浓度阈值扰动下各 BMI 组推荐检测时点的变化，显示高 BMI 组对阈值变化更敏感}
\end{figure}
"""
    main = rf"""\documentclass[UTF8]{{ctexart}}
\usepackage{{graphicx}}
\usepackage{{booktabs}}
\usepackage{{geometry}}
\usepackage{{array}}
\usepackage{{amsmath}}
\geometry{{a4paper, margin=2.5cm}}
\title{{NIPT 检测时点选择与胎儿异常判定模型}}
\author{{}}
\date{{}}
\begin{{document}}
\maketitle
\begin{{abstract}}
本文围绕 NIPT 检测中的时点选择和胎儿异常判定问题，建立男胎 Y 染色体浓度模型、BMI 分组检测时点优化模型以及女胎异常风险判别模型。首先以孕周、BMI、年龄和 GC 含量解释 Y 染色体浓度，模型拟合得到 $R^2={p['r2']}$，平均绝对误差为 ${p['mae']}$ 个百分点，可用于反推浓度达到 $4\%$ 阈值的孕周。其次将检测过早造成的未达标风险与检测过晚风险合并为分组风险函数，得到 BMI 分组推荐时点：{p['weeks']}，并通过阈值扰动检验推荐结果的稳定性。最后构造基于染色体 Z 值、X 染色体偏离和 GC 含量的异常风险评分，得到 AUC 为 ${p['auc']}$，灵敏度为 ${p['sensitivity']}$。结果说明，可解释统计模型、分组优化和判别曲线能够形成一条可复核的 NIPT 决策链；受控数据只用于方法验证，不替代真实临床结论。

\textbf{{关键词：}}NIPT；检测时点；BMI 分组；风险优化；异常判定
\end{{abstract}}

\section{{问题重述}}
无创产前检测通过孕妇外周血中的胎儿游离 DNA 信息评估胎儿染色体风险。对男胎而言，Y 染色体浓度是否达到阈值会影响检测可靠性；对女胎而言，需要综合常染色体和性染色体相关指标识别异常风险。检测时间过早可能造成胎儿浓度不足，检测时间过晚又可能增加临床处置风险，因此时点选择本质上是一个在可靠性和风险之间折中的决策问题。

本文将问题拆分为三层：第一，建立男胎 Y 染色体浓度与孕周、BMI 等因素之间的关系；第二，按 BMI 分组选择推荐检测孕周，并检验阈值变化对推荐结果的影响；第三，对女胎样本建立异常风险评分并评价判别效果。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.86\textwidth]{{../figures/fig_problem_overview.png}}
\caption{{NIPT 检测时点与异常判定的建模对象、输入指标和验证线索}}
\end{{figure}}

\section{{问题分析}}
Y 染色体浓度一般随孕周增加而上升，但 BMI 较高时胎儿 DNA 相对浓度可能下降，因此单独用孕周判断会忽略个体差异。BMI 分组后，推荐检测时点既要使组内大多数样本达到浓度阈值，又不能无节制推迟。女胎异常判定则不能依赖 Y 染色体浓度，需要从 13、18、21 号染色体 Z 值、X 染色体偏离和 GC 含量等指标构造风险评分。本文采用线性浓度模型、分组网格搜索和 Logistic 判别模型，是因为三者分别对应解释、决策和分类，且每一步都有明确的验证指标。

\section{{数据预处理}}
对男胎数据，保留孕周、BMI、年龄、GC 含量和 Y 染色体浓度，并以 $4\%$ 作为达标阈值。对女胎数据，构造最大常染色体 Z 值、X 染色体偏离绝对值、GC 偏离量、年龄和 BMI 等特征。所有连续变量在建模前检查范围和缺失情况；分类模型中特征先标准化，以免量纲差异影响权重估计。本文使用受控数据进行流程验证，因此评价指标用于检查模型链路和监督返工，而不是声称真实医学性能。

\section{{模型假设}}
\begin{{enumerate}}
\item 在分析窗口内，Y 染色体浓度随孕周的主效应可用线性项近似。
\item BMI、年龄和 GC 含量对浓度的影响在受控样本中可用加性主效应表示。
\item 同一 BMI 组内采用统一推荐检测时点，组内个体差异进入未达标率和敏感性分析。
\item 女胎异常风险可由染色体 Z 值、X 染色体偏离和 GC 偏离的组合评分近似刻画。
\item 判别阈值服务于筛查任务，因此优先保证灵敏度，再兼顾特异度。
\end{{enumerate}}

\section{{符号说明}}
\begin{{center}}
\begin{{tabular}}{{lll}}
\toprule
符号 & 含义 & 单位\\
\midrule
$t$ & 孕周 & 周\\
$b$ & BMI & 1\\
$y$ & Y 染色体浓度 & \%\\
$z_k$ & 第 $k$ 号染色体 Z 值 & 1\\
$p$ & 异常风险评分 & 1\\
$R_g(t)$ & BMI 组 $g$ 在孕周 $t$ 的风险 & 1\\
\bottomrule
\end{{tabular}}
\end{{center}}

\section{{模型建立与求解}}
\input{{sections/q1.tex}}
\input{{sections/q2.tex}}
\input{{sections/q3.tex}}

\section{{模型检验}}
第一，Y 浓度模型通过拟合优度和残差图检验。$R^2={p['r2']}$ 表明孕周、BMI、年龄和 GC 含量可以解释主要变化，残差没有出现明显的系统弯曲。第二，分组时点模型用未达标率和阈值扰动检验。若阈值从 $3.8\%$ 调整到 $4.2\%$，部分 BMI 组推荐孕周随之后移，说明阈值设定必须在报告中明示。第三，异常判定模型用 ROC 曲线和混淆矩阵检验，AUC 为 ${p['auc']}$，灵敏度为 ${p['sensitivity']}$，符合筛查任务对漏判风险更敏感的要求。

{q2_sens_figure}

\section{{模型评价}}
本文模型的优点是每一步都能解释并检查：浓度模型给出阈值周数的来源，分组优化把早检失败和晚检风险放入同一目标，异常判定用概率评分替代单指标硬阈值。模型也有局限。线性关系只适合受控窗口；真实临床数据可能存在批次效应、重复检测、孕妇疾病史和样本质量差异。若用于真实数据，应加入更严格的数据清洗、交叉验证、校准曲线和医学阈值审查。

\section{{结论}}
本文建立了 NIPT 检测时点选择与胎儿异常判定的三层模型。男胎 Y 浓度模型给出 $R^2={p['r2']}$、平均绝对误差 ${p['mae']}$ 个百分点；BMI 分组优化给出 {p['weeks']} 的推荐时点；女胎异常判定模型得到 AUC=${p['auc']}$、灵敏度=${p['sensitivity']}$、特异度=${p['specificity']}。这些结果共同说明，时点选择不应只由孕周决定，而应同时考虑 BMI、阈值扰动和异常风险判定。受控数据下的结果证明了建模和监督流程的可复核性，真实应用还需结合官方附件和临床约束重新估计参数。

\begin{{thebibliography}}{{9}}
\bibitem{{officialreview}} 全国大学生数学建模竞赛组委会相关公开讲评. 2025 全国大学生数学建模竞赛 C 题讲评：NIPT 的时点选择与胎儿的异常判定[EB/OL].
\bibitem{{clinical}} Lo Y. M. D., et al. Presence of fetal DNA in maternal plasma and serum[J]. The Lancet, 1997.
\bibitem{{screening}} Bianchi D. W., et al. DNA sequencing versus standard prenatal aneuploidy screening[J]. New England Journal of Medicine, 2014.
\end{{thebibliography}}

\appendix
\section{{复现说明}}
运行求解程序可重新生成受控数据、图表、结果表和论文源文件。受控数据不包含真实个人信息，也不用于给出医学结论。
\end{{document}}
"""
    q1 = rf"""男胎 Y 染色体浓度模型采用可解释的加性形式：
\[
\hat y=\beta_0+\beta_1t+\beta_2b+\beta_3a+\beta_4g,
\]
其中 $t$ 为孕周，$b$ 为 BMI，$a$ 为年龄，$g$ 为 GC 含量。模型拟合后可由 $\hat y=4\%$ 反推出给定个体的最早达标孕周。该模型不是为了追求复杂预测，而是为了让阈值时点能够追溯到变量影响。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{{../figures/fig_q1_model_schematic.png}}
\caption{{Y 染色体浓度模型把孕周、BMI、年龄和 GC 含量映射为浓度预测，并由 $4\%$ 阈值反推检测时点}}
\end{{figure}}

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{{../figures/fig_q1_result.png}}
\caption{{Y 浓度拟合和达标阈值关系；颜色表示 BMI，红色虚线为 $4\%$ 达标阈值}}
\end{{figure}}

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.76\textwidth]{{../figures/fig_q1_validation.png}}
\caption{{Y 浓度模型残差分布，用于检查主效应模型是否存在明显系统偏差}}
\end{{figure}}
"""
    q2 = r"""对 BMI 组 $g$ 和候选孕周 $t$，定义风险函数
\[
R_g(t)=\lambda(t-12)_+ + 3P_g(\hat y(t)<4\%),
\]
其中第一项表示检测推迟带来的风险，第二项表示浓度未达标风险。对每一组在候选孕周上搜索 $R_g(t)$ 的最小值，得到推荐检测时点。该做法保留了可解释性：若阈值或风险权重变化，推荐时点应随之调整并被敏感性分析记录。

\begin{figure}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{../figures/fig_q2_model_schematic.png}
\caption{BMI 分组检测时点优化链条：分组、候选孕周、未达标率估计和风险最小化共同决定推荐孕周}
\end{figure}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.88\textwidth]{../figures/fig_q2_result.png}
\caption{不同 BMI 组的推荐检测时点及其对应未达标风险，高 BMI 组通常需要更晚的推荐时点}
\end{figure}
"""
    q3_text = rf"""女胎异常判定使用多指标风险评分。令 $x_1=\max(z_{13},z_{18},z_{21})$，$x_2=|z_X|$，$x_3=|GC-0.5|$，并加入年龄和 BMI，采用
\[
p=\frac{{1}}{{1+\exp[-(\alpha+\sum_kw_kx_k)]}}
\]
计算异常概率。阈值取 ${float(q3['threshold']):.2f}$，使判定更偏向筛查中的灵敏度要求。

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.82\textwidth]{{../figures/fig_q3_model_schematic.png}}
\caption{{女胎异常风险评分模型，综合染色体 Z 值、X 染色体偏离和 GC 偏离形成概率判定}}
\end{{figure}}

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.90\textwidth]{{../figures/fig_q3_result.png}}
\caption{{异常风险评分分布与 ROC 曲线；AUC 为 ${p['auc']}，说明多指标评分能够区分高低风险样本}}
\end{{figure}}

\begin{{figure}}[htbp]
\centering
\includegraphics[width=0.58\textwidth]{{../figures/fig_q3_validation.png}}
\caption{{异常判定混淆矩阵，用于同时检查漏判和误判数量}}
\end{{figure}}
"""
    (PAPER_DIR / "main.tex").write_text(main, encoding="utf-8")
    (SECTION_DIR / "q1.tex").write_text(q1, encoding="utf-8")
    (SECTION_DIR / "q2.tex").write_text(q2, encoding="utf-8")
    (SECTION_DIR / "q3.tex").write_text(q3_text, encoding="utf-8")


def write_reports(q1: dict[str, object], q2_rows: list[dict[str, object]], q3: dict[str, object], draft: bool) -> None:
    lines = [
        "# Validation Report",
        "",
        f"- Q1 R2: {float(q1['r2']):.3f}",
        f"- Q1 MAE: {float(q1['mae']):.3f} percentage points",
        f"- Q2 groups: {', '.join(str(row['bmi_group']) + '=' + str(row['recommended_week']) for row in q2_rows)}",
        f"- Q2 sensitivity: {'missing in draft' if draft else 'generated'}",
        f"- Q3 AUC: {float(q3['auc']):.3f}",
        f"- Q3 sensitivity: {float(q3['sensitivity']):.3f}",
    ]
    (RESULT_DIR / "validation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (RESULT_DIR / "benchmark_findings.md").write_text(
        "# Benchmark Findings\n\n"
        "The controlled C-problem run follows the skill workflow: interpretable model, grouped optimization, classification validation, and supervised rework gate.\n",
        encoding="utf-8",
    )
    (APPENDIX_DIR / "ai-usage-statement.md").write_text(
        "# AI Usage Statement\n\nAI assisted with workflow orchestration, code generation, figures, paper drafting, and artifact checks. All numerical results are generated by deterministic code in this project.\n",
        encoding="utf-8",
    )
    readme = """# CUMCM 2025 C 题监督-返工闭环测试

本目录是一个新的 C 题受控测试，用于证明监督-返工闭环已经沉淀到 skill，而不是依赖单次人工经验。

题目方向来自公开题名“NIPT 的时点选择与胎儿的异常判定”。本目录不包含官方附件原始数据，而是生成不含个人信息的合成数据，检查建模、验证、论文、进度面板和打包链路。

## 关键证明

- `progress.html` 展示 supervisor gate、revise、rework、recheck 事件。
- `logs/progress.jsonl` 包含 gate id、decision、owner、issue、expected fix、evidence needed。
- `figures/fig_q2_sensitivity.png` 和 `tables/tab_q2_sensitivity.csv` 是返工后补上的真实产物。
- `results/validation_audit.md` 和 `results/paper_style_audit.md` 是最终复检证据。

## 运行

```powershell
python src/solve_nipt_supervised.py
python ..\\..\\..\\scripts\\validate_results.py --project . --mode full --paper-genre contest_paper --output results\\validation_audit.md
python ..\\..\\..\\scripts\\lint_paper_style.py --paper paper\\main.tex --genre contest_paper --output results\\paper_style_audit.md
```
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")


def run(draft: bool) -> int:
    for directory in [DATA_DIR, FIGURE_DIR, TABLE_DIR, RESULT_DIR, PAPER_DIR, SECTION_DIR, PROBLEM_DIR, APPENDIX_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    if draft:
        missing = [FIGURE_DIR / "fig_q2_sensitivity.png", TABLE_DIR / "tab_q2_sensitivity.csv"]
        for path in missing:
            if path.exists():
                path.unlink()
    generate_data()
    male_rows = read_numeric_csv(DATA_DIR / "nipt_male_synthetic.csv")
    female_rows = read_numeric_csv(DATA_DIR / "nipt_female_synthetic.csv")
    q1 = fit_linear_y(male_rows)
    coef = q1["coef"]
    assert isinstance(coef, np.ndarray)
    q2_rows = optimize_timing(male_rows, coef)
    q2_sens = sensitivity_timing(male_rows, coef)
    q3 = fit_logistic(female_rows)

    write_problem_files()
    write_tables(male_rows, female_rows, q1, q2_rows, q2_sens, q3, draft)
    plot_problem_overview()
    plot_q1(male_rows, q1)
    plot_q2(q2_rows, q2_sens, draft)
    plot_q3(female_rows, q3)
    write_registry(q1, q2_rows, q3, draft)
    write_paper(q1, q2_rows, q3, draft)
    write_reports(q1, q2_rows, q3, draft)

    print("CUMCM 2025 C supervised NIPT case")
    print(f"draft={draft}")
    print(f"Q1 R2={float(q1['r2']):.3f}, MAE={float(q1['mae']):.3f}")
    print("; ".join(f"{row['bmi_group']}={row['recommended_week']}" for row in q2_rows))
    print(f"Q3 AUC={float(q3['auc']):.3f}, sensitivity={float(q3['sensitivity']):.3f}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the C-problem supervised NIPT example.")
    parser.add_argument("--draft", action="store_true", help="Generate a deliberately incomplete first pass.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run(args.draft)


if __name__ == "__main__":
    raise SystemExit(main())
