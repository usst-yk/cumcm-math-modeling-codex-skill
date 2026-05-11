"""Shared plotting helpers for the 2025 A real-case example."""

from __future__ import annotations

from pathlib import Path

from matplotlib import font_manager
import matplotlib.pyplot as plt


ENGLISH_SERIF = ["Times New Roman", "Times", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"]


def bundled_font_dir() -> Path | None:
    for parent in Path(__file__).resolve().parents:
        candidate = parent / "assets" / "fonts"
        if candidate.exists():
            return candidate
    return None


def setup_chinese_plot(base_font_size: int = 18) -> None:
    """Configure matplotlib so paper-inserted figures remain readable.

    The source figure is usually scaled down when inserted into a paper, so the
    source font size should be larger than body text. After insertion, labels
    should look close to body text, with titles slightly larger.
    """
    font_dir = bundled_font_dir()
    if font_dir:
        for name in ["NotoSansCJKsc-Regular.otf", "NotoSansCJKsc-Bold.otf"]:
            path = font_dir / name
            if path.exists():
                font_manager.fontManager.addfont(str(path))
        selected = font_manager.FontProperties(fname=str(font_dir / "NotoSansCJKsc-Regular.otf")).get_name()
    else:
        installed = {font.name for font in font_manager.fontManager.ttflist}
        selected = next((font for font in ["Noto Sans CJK SC", "Microsoft YaHei", "SimHei"] if font in installed), "DejaVu Sans")
    english = next((font for font in ENGLISH_SERIF if font in {f.name for f in font_manager.fontManager.ttflist}), "DejaVu Serif")
    plt.rcParams.update(
        {
            "font.family": [english, selected],
            "font.serif": ENGLISH_SERIF,
            "font.sans-serif": [selected, "Noto Sans CJK SC", "Microsoft YaHei", "SimHei"],
            "axes.unicode_minus": False,
            "mathtext.fontset": "stix",
            "figure.dpi": 180,
            "savefig.dpi": 360,
            "font.size": base_font_size,
            "axes.titlesize": base_font_size + 2,
            "axes.labelsize": base_font_size,
            "xtick.labelsize": base_font_size - 3,
            "ytick.labelsize": base_font_size - 3,
            "legend.fontsize": base_font_size - 3,
        }
    )
