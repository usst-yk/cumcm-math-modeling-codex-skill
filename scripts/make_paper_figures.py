#!/usr/bin/env python3
"""Shared matplotlib settings and a small demo for CUMCM paper figures."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd


def available_font(candidates: list[str]) -> str:
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return "DejaVu Sans"


def apply_cumcm_style(font_size: int = 18) -> None:
    font = available_font(["Songti SC", "PingFang SC", "Heiti SC", "Microsoft YaHei", "Noto Sans CJK SC", "SimHei", "SimSun"])
    plt.rcParams.update(
        {
            "font.family": font,
            "font.size": font_size,
            "axes.titlesize": font_size + 2,
            "axes.labelsize": font_size,
            "xtick.labelsize": font_size - 2,
            "ytick.labelsize": font_size - 2,
            "legend.fontsize": font_size - 2,
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def demo_figure(output: Path) -> None:
    apply_cumcm_style()
    df = pd.DataFrame({"方案": ["基线", "主模型", "稳健方案"], "指标值": [1.0, 0.78, 0.82]})
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(df["方案"], df["指标值"], color=["#6B7280", "#2563EB", "#059669"])
    ax.set_ylabel("归一化指标")
    ax.set_title("示例：方案对比")
    ax.set_ylim(0, max(df["指标值"]) * 1.25)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply CUMCM plotting style or create a demo figure.")
    parser.add_argument("--demo", action="store_true", help="Create a demo bar chart.")
    parser.add_argument("--output", default="figures/fig_q1_demo.png", help="Output path for demo chart.")
    args = parser.parse_args()

    if args.demo:
        demo_figure(Path(args.output).expanduser().resolve())
        print(f"Demo figure written to: {Path(args.output).expanduser().resolve()}")
    else:
        print("Import apply_cumcm_style() in plotting scripts, or run with --demo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
