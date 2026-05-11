"""Shared plotting helpers for the 2025 C NIPT supervised example."""

from __future__ import annotations

from pathlib import Path

from matplotlib import font_manager
import matplotlib.pyplot as plt


CHINESE_FONT_CANDIDATES = [
    "Microsoft YaHei",
    "Microsoft YaHei UI",
    "SimSun",
    "DengXian",
    "SimHei",
    "PingFang SC",
    "Hiragino Sans GB",
    "Arial Unicode MS",
    "DejaVu Sans",
]

WINDOWS_FONT_FILES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simsun.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
]


def setup_chinese_plot(base_font_size: int = 14) -> None:
    for font_path in WINDOWS_FONT_FILES:
        path = Path(font_path)
        if path.exists():
            font_manager.fontManager.addfont(str(path))
    installed = {font.name for font in font_manager.fontManager.ttflist}
    selected = next((font for font in CHINESE_FONT_CANDIDATES if font in installed), "DejaVu Sans")
    plt.rcParams.update(
        {
            "font.sans-serif": [selected, "DejaVu Sans"],
            "axes.unicode_minus": False,
            "figure.dpi": 180,
            "font.size": base_font_size,
            "axes.titlesize": base_font_size + 1,
            "axes.labelsize": base_font_size,
            "xtick.labelsize": base_font_size - 2,
            "ytick.labelsize": base_font_size - 2,
            "legend.fontsize": base_font_size - 2,
        }
    )
