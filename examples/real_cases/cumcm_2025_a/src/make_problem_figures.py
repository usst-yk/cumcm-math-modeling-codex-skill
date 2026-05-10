#!/usr/bin/env python3
"""Create Chinese schematic figures for the 2025 A problem statement."""

from __future__ import annotations

from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from plot_utils import setup_chinese_plot


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"

DECOY = np.array([0.0, 0.0, 0.0])
TRUE_TARGET_CENTER = np.array([0.0, 200.0, 0.0])

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


def write_overview_xy() -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9.5, 5.8), dpi=180)
    ax.scatter([DECOY[0]], [DECOY[1]], marker="*", s=180, color="#7f7f7f", label="假目标")
    ax.scatter(
        [TRUE_TARGET_CENTER[0]],
        [TRUE_TARGET_CENTER[1]],
        marker="o",
        s=90,
        color="#c00000",
        label="真目标中心",
    )

    for name, pos in MISSILES.items():
        ax.scatter(pos[0], pos[1], marker="^", s=82, color="#7030a0")
        ax.text(pos[0] + 300, pos[1] + 120, f"{name} 导弹", fontsize=13)
        ax.annotate(
            "",
            xy=(DECOY[0], DECOY[1]),
            xytext=(pos[0], pos[1]),
            arrowprops={"arrowstyle": "->", "color": "#7030a0", "alpha": 0.32, "linewidth": 1.1},
        )

    for name, pos in UAVS.items():
        ax.scatter(pos[0], pos[1], marker="s", s=58, color="#548235")
        ax.text(pos[0] + 220, pos[1] - 180, f"{name} 无人机", fontsize=13)

    ax.add_patch(
        patches.Circle(
            (TRUE_TARGET_CENTER[0], TRUE_TARGET_CENTER[1]),
            radius=180,
            fill=False,
            edgecolor="#c00000",
            linewidth=1.2,
            linestyle="--",
            alpha=0.75,
        )
    )
    ax.text(350, 320, "真目标投影\n(示意放大)", fontsize=13, color="#c00000")

    ax.set_title("2025 A 题：导弹、无人机与目标的平面位置示意")
    ax.set_xlabel("x 坐标 / m")
    ax.set_ylabel("y 坐标 / m")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", frameon=False)
    ax.set_xlim(-900, 21000)
    ax.set_ylim(-3500, 2600)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_problem_overview_xy.png", bbox_inches="tight")
    plt.close(fig)


def write_question_scope() -> None:
    setup_chinese_plot()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    rows = [
        ["问题一", "FY1", "1 枚", "M1", "给定策略\n计算遮蔽时长"],
        ["问题二", "FY1", "1 枚", "M1", "优化方向/速度\n投放点/起爆点"],
        ["问题三", "FY1", "3 枚", "M1", "多弹协同\n写入 result1.xlsx"],
        ["问题四", "FY1-FY3", "各 1 枚", "M1", "多机协同\n写入 result2.xlsx"],
        ["问题五", "FY1-FY5", "每机至多 3 枚", "M1-M3", "多机多弹多导弹\n写入 result3.xlsx"],
    ]
    columns = ["子问题", "可用无人机", "烟幕弹数量", "干扰对象", "核心输出"]

    fig, ax = plt.subplots(figsize=(12, 5.2), dpi=180)
    ax.axis("off")
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        cellLoc="center",
        bbox=[0.02, 0.06, 0.96, 0.76],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1.0, 1.55)

    for (row, _col), cell in table.get_celld().items():
        cell.set_edgecolor("#bfbfbf")
        if row == 0:
            cell.set_facecolor("#d9eaf7")
            cell.set_text_props(weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#f7f7f7")

    ax.set_title("2025 A 题：五个子问题的资源范围和输出要求", pad=16)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig_problem_question_scope.png", bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    write_overview_xy()
    write_question_scope()
    print("wrote figures/fig_problem_overview_xy.png")
    print("wrote figures/fig_problem_question_scope.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
