#!/usr/bin/env python3
"""Shared matplotlib settings and a small demo for CUMCM paper figures."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "assets" / "fonts"
CHINESE_REGULAR = FONT_DIR / "NotoSansCJKsc-Regular.otf"
CHINESE_BOLD = FONT_DIR / "NotoSansCJKsc-Bold.otf"
ENGLISH_SERIF = ["Times New Roman", "Times", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"]


def register_bundled_fonts() -> str:
    """Register bundled fonts and return the Chinese family name."""
    for font_path in [CHINESE_REGULAR, CHINESE_BOLD]:
        if font_path.exists():
            font_manager.fontManager.addfont(str(font_path))
    if CHINESE_REGULAR.exists():
        return font_manager.FontProperties(fname=str(CHINESE_REGULAR)).get_name()
    return available_font(["Noto Sans CJK SC", "Microsoft YaHei", "SimHei"])


def available_font(candidates: list[str]) -> str:
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return "DejaVu Sans"


def apply_cumcm_style(font_size: int = 18) -> None:
    chinese_font = register_bundled_fonts()
    english_font = available_font(ENGLISH_SERIF)
    plt.rcParams.update(
        {
            "font.family": [english_font, chinese_font],
            "font.serif": ENGLISH_SERIF,
            "font.sans-serif": [chinese_font, "Noto Sans CJK SC", "Microsoft YaHei", "SimHei"],
            "font.size": font_size,
            "axes.titlesize": font_size + 2,
            "axes.labelsize": font_size,
            "xtick.labelsize": font_size - 2,
            "ytick.labelsize": font_size - 2,
            "legend.fontsize": font_size - 2,
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
            "figure.dpi": 160,
            "savefig.dpi": 360,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "grid.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 1.0,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "savefig.bbox": "tight",
            "legend.frameon": False,
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
