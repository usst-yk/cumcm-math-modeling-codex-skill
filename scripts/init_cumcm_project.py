#!/usr/bin/env python3
"""Create a CUMCM project workspace.

Default mode is paper-first: create the core directories plus `paper/main.tex`
and `results/result_registry.csv`, because all useful work should flow back to
the TeX paper. The project layout is intentionally fixed; this script does not
create logs, appendix, presentation, notebook, or dashboard folders.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


STANDARD_DIRS = [
    "problem",
    "modeling",
    "data",
    "src",
    "figures",
    "tables",
    "results",
    "paper",
]


def copy_file(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists() and not overwrite:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_text(path: Path, text: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a CUMCM math modeling project skeleton.")
    parser.add_argument("project_dir", nargs="?", help="Directory to create or update.")
    parser.add_argument("--name", help="Project directory name, e.g. cumcm_2026_A.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing template files.")
    args = parser.parse_args()

    if not args.project_dir and not args.name:
        parser.error("provide project_dir or --name")

    project_dir = Path(args.project_dir or args.name).expanduser().resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    for name in STANDARD_DIRS:
        (project_dir / name).mkdir(parents=True, exist_ok=True)

    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "templates"

    copy_file(templates / "result_registry.csv", project_dir / "results" / "result_registry.csv", args.overwrite)
    copy_file(templates / "paper_main.tex", project_dir / "paper" / "main.tex", args.overwrite)
    write_text(
        project_dir / "problem" / "problem_statement.md",
        "# Problem Statement\n\nPaste the official problem statement here.",
        args.overwrite,
    )

    print(f"Created CUMCM workspace at: {project_dir}")
    for name in STANDARD_DIRS:
        print(f"- {name}/")
    print("Created paper/main.tex and results/result_registry.csv.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
