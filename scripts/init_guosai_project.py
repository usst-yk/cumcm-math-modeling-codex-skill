#!/usr/bin/env python3
"""Create a CUMCM project skeleton with paper and appendix templates."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DIRS = ["data", "src", "figures", "tables", "paper", "appendix"]


def copy_file(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists() and not overwrite:
        return
    shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a guosai math modeling project skeleton.")
    parser.add_argument("project_dir", help="Directory to create or update.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing template files.")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    for name in DIRS:
        (project_dir / name).mkdir(exist_ok=True)

    skill_root = Path(__file__).resolve().parents[1]
    assets = skill_root / "assets"
    copy_file(assets / "paper-template.md", project_dir / "paper" / "main.md", args.overwrite)
    copy_file(assets / "assumptions-symbols-template.md", project_dir / "paper" / "assumptions-symbols.md", args.overwrite)
    copy_file(assets / "appendix-code-template.md", project_dir / "appendix" / "code-template.md", args.overwrite)

    readme = project_dir / "project-structure.md"
    if args.overwrite or not readme.exists():
        readme.write_text(
            "\n".join(
                [
                    "# 国赛项目结构",
                    "",
                    "- `data/`: 原始数据和清洗后的数据。",
                    "- `src/`: 数据处理、建模、求解和绘图代码。",
                    "- `figures/`: 代码生成的论文图片。",
                    "- `tables/`: 代码生成的统计表和结果表。",
                    "- `paper/`: 论文正文、假设、符号说明和数据预处理草稿。",
                    "- `appendix/`: 附录代码、补充图表和参数说明。",
                    "",
                    "所有正文图表应由 `src/` 中代码生成，避免手工改数。",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    print(f"Created guosai project skeleton at: {project_dir}")
    for name in DIRS:
        print(f"- {name}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
