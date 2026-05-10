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


def setup_chinese_plot(base_font_size: int = 18) -> None:
    """Configure matplotlib so paper-inserted figures remain readable.

    The source figure is usually scaled down when inserted into a paper, so the
    source font size should be larger than body text. After insertion, labels
    should look close to body text, with titles slightly larger.
    """
    installed = {font.name for font in font_manager.fontManager.ttflist}
    selected = next((font for font in CHINESE_FONT_CANDIDATES if font in installed), "DejaVu Sans")
    plt.rcParams.update(
        {
            "font.sans-serif": [selected, "DejaVu Sans"],
            "axes.unicode_minus": False,
            "figure.dpi": 180,
            "font.size": base_font_size,
            "axes.titlesize": base_font_size + 2,
            "axes.labelsize": base_font_size,
            "xtick.labelsize": base_font_size - 3,
            "ytick.labelsize": base_font_size - 3,
            "legend.fontsize": base_font_size - 3,
        }
    )
