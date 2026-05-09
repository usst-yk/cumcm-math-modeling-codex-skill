#!/usr/bin/env python3
"""Create a CUMCM project skeleton with reproducible workflow files."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DIRS = [
    "problem",
    "data/raw",
    "data/processed",
    "src",
    "notebooks",
    "results/sensitivity",
    "figures",
    "tables",
    "tables/data_profile",
    "paper/sections",
    "appendix",
    "logs",
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

    for name in DIRS:
        (project_dir / name).mkdir(parents=True, exist_ok=True)

    skill_root = Path(__file__).resolve().parents[1]
    assets = skill_root / "assets"
    templates = skill_root / "templates"

    copy_file(assets / "paper-template.md", project_dir / "paper" / "main.md", args.overwrite)
    copy_file(assets / "assumptions-symbols-template.md", project_dir / "problem" / "assumptions.md", args.overwrite)
    copy_file(assets / "appendix-code-template.md", project_dir / "appendix" / "code-template.md", args.overwrite)
    copy_file(templates / "task_plan.schema.json", project_dir / "problem" / "task_plan.schema.json", args.overwrite)
    copy_file(templates / "task_plan.json", project_dir / "problem" / "task_plan.json", args.overwrite)
    copy_file(templates / "model_card.md", project_dir / "problem" / "model_card_template.md", args.overwrite)
    copy_file(templates / "result_registry.csv", project_dir / "results" / "result_registry.csv", args.overwrite)
    copy_file(templates / "validation_report.md", project_dir / "results" / "validation_report.md", args.overwrite)
    copy_file(templates / "paper_main.tex", project_dir / "paper" / "main.tex", args.overwrite)
    copy_file(templates / "refs.bib", project_dir / "paper" / "refs.bib", args.overwrite)
    copy_file(templates / "run_log.md", project_dir / "logs" / "run_log.md", args.overwrite)

    write_text(project_dir / "logs" / "error_log.md", "# Error Log\n\nNo errors recorded yet.", args.overwrite)
    write_text(
        project_dir / "problem" / "problem_statement.md",
        "# Problem Statement\n\nPaste the official problem statement here.",
        args.overwrite,
    )
    for qid in ("q1", "q2", "q3"):
        write_text(
            project_dir / "paper" / "sections" / f"{qid}.tex",
            f"% Write {qid.upper()} section after results are registered.",
            args.overwrite,
        )
    write_text(
        project_dir / "project-structure.md",
        "\n".join(
            [
                "# CUMCM Project Structure",
                "",
                "- `problem/`: problem statement, assumptions, task plan, and model cards.",
                "- `data/raw/`: untouched attachments.",
                "- `data/processed/`: cleaned or reconstructed data.",
                "- `src/`: deterministic scripts, named by subquestion when possible.",
                "- `notebooks/`: optional exploration notebooks.",
                "- `results/`: result registry, validation report, and sensitivity outputs.",
                "- `figures/`: code-generated paper figures and editable roadmap outputs.",
                "- `tables/`: generated result tables and data audit tables.",
                "- `paper/`: TeX/Markdown paper, sections, references, and compiled PDF.",
                "- `appendix/`: appendix code and supplemental material.",
                "- `logs/`: run log and error recovery log.",
                "",
                "All headline values must be registered in `results/result_registry.csv` before final writing.",
            ]
        ),
        args.overwrite,
    )

    print(f"Created CUMCM project skeleton at: {project_dir}")
    for name in DIRS:
        print(f"- {name}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
