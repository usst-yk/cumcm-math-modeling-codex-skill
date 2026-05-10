"""Shared plotting helpers for the 2025 A real-case example."""

from __future__ import annotations

from matplotlib import font_manager
import matplotlib.pyplot as plt


CHINESE_FONT_CANDIDATES = [
    "PingFang SC",
    "Hiragino Sans GB",
    "Arial Unicode MS",
    "Heiti SC",
    "STHeiti",
    "SimHei",
    "Songti SC",
    "SimSong",
]


def setup_chinese_plot() -> None:
    """Configure matplotlib so contest figures prefer Chinese labels."""
    installed = {font.name for font in font_manager.fontManager.ttflist}
    selected = next((font for font in CHINESE_FONT_CANDIDATES if font in installed), "DejaVu Sans")
    plt.rcParams["font.sans-serif"] = [selected, "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 180
