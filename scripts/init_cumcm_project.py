#!/usr/bin/env python3
"""Create a CUMCM project workspace.

Default mode is paper-first: create the core directories plus `paper/main.tex`
and `results/result_registry.csv`, because all useful work should flow back to
the TeX paper. Use --full when every auxiliary template and log is explicitly
needed.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from update_progress import now_iso, open_file, render_html


STANDARD_DIRS = [
    "problem",
    "modeling",
    "modeling/flowcharts",
    "data/raw",
    "data/processed",
    "src",
    "figures",
    "tables",
    "results",
    "paper",
]

FULL_DIRS = [
    "problem",
    "modeling",
    "data/raw",
    "data/processed",
    "src",
    "notebooks",
    "results/sensitivity",
    "figures",
    "figures/ai_briefs",
    "presentation",
    "presentation/figures",
    "tables",
    "tables/data_profile",
    "paper",
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


def initialize_progress(project_dir: Path, overwrite: bool) -> None:
    log_path = project_dir / "logs" / "progress.jsonl"
    html_path = project_dir / "progress.html"
    event = {
        "time": now_iso(),
        "stage": "init",
        "current_stage": "init",
        "status": "working",
        "worker": "init_cumcm_project.py",
        "message": "Full CUMCM project skeleton initialization started.",
        "files": [],
        "generated_files": ["logs/progress.jsonl", "progress.html"],
        "blocker": "",
        "retry_reason": "",
        "score": "",
        "rubric_status": "not reviewed",
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if overwrite or not log_path.exists() else "a"
    with log_path.open(mode, encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    events = [event] if mode == "w" else []
    if not events:
        from update_progress import read_jsonl

        events = read_jsonl(log_path)
    render_html(events, html_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a CUMCM math modeling project skeleton.")
    parser.add_argument("project_dir", nargs="?", help="Directory to create or update.")
    parser.add_argument("--name", help="Project directory name, e.g. cumcm_2026_A.")
    parser.add_argument("--full", action="store_true", help="Copy full templates and logs.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing template files.")
    parser.add_argument("--open", action="store_true", help="Open progress.html after full project initialization.")
    args = parser.parse_args()

    if not args.project_dir and not args.name:
        parser.error("provide project_dir or --name")

    project_dir = Path(args.project_dir or args.name).expanduser().resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    dirs = FULL_DIRS if args.full else STANDARD_DIRS
    for name in dirs:
        (project_dir / name).mkdir(parents=True, exist_ok=True)

    skill_root = Path(__file__).resolve().parents[1]
    templates = skill_root / "templates"

    if not args.full:
        copy_file(templates / "paper_main.tex", project_dir / "paper" / "main.tex", args.overwrite)
        copy_file(templates / "result_registry.csv", project_dir / "results" / "result_registry.csv", args.overwrite)
        write_text(
            project_dir / "problem" / "problem_statement.md",
            "# Problem Statement\n\nPaste the official problem statement here.",
            args.overwrite,
        )
        print(f"Created paper-first CUMCM workspace at: {project_dir}")
        for name in dirs:
            print(f"- {name}/")
        print("Created paper/main.tex and results/result_registry.csv for paper-first work.")
        return 0

    initialize_progress(project_dir, args.overwrite)

    copy_file(templates / "problem_parse.schema.json", project_dir / "problem" / "problem_parse.schema.json", args.overwrite)
    copy_file(templates / "task_plan.schema.json", project_dir / "problem" / "task_plan.schema.json", args.overwrite)
    copy_file(templates / "task_plan.json", project_dir / "problem" / "task_plan.json", args.overwrite)
    copy_file(templates / "model_card.md", project_dir / "problem" / "model_card_template.md", args.overwrite)
    copy_file(templates / "modeling_idea.md", project_dir / "modeling" / "modeling_idea_template.md", args.overwrite)
    copy_file(templates / "assumptions_symbols.md", project_dir / "problem" / "assumptions.md", args.overwrite)
    copy_file(templates / "result_registry.csv", project_dir / "results" / "result_registry.csv", args.overwrite)
    copy_file(templates / "validation_report.md", project_dir / "results" / "validation_report.md", args.overwrite)
    copy_file(templates / "paper_main.tex", project_dir / "paper" / "main.tex", args.overwrite)
    copy_file(templates / "refs.bib", project_dir / "paper" / "refs.bib", args.overwrite)
    copy_file(templates / "appendix_code.md", project_dir / "appendix" / "code-template.md", args.overwrite)
    copy_file(templates / "run_log.md", project_dir / "logs" / "run_log.md", args.overwrite)
    copy_file(templates / "ai_usage_statement.md", project_dir / "appendix" / "ai-usage-statement.md", args.overwrite)
    copy_file(templates / "ai_figure_brief.md", project_dir / "figures" / "ai_briefs" / "ai_figure_brief_template.md", args.overwrite)

    write_text(project_dir / "logs" / "error_log.md", "# Error Log\n\nNo errors recorded yet.", args.overwrite)
    write_text(
        project_dir / "problem" / "problem_statement.md",
        "# Problem Statement\n\nPaste the official problem statement here.",
        args.overwrite,
    )
    write_text(
        project_dir / "project-structure.md",
        "\n".join(
            [
                "# CUMCM Project Structure",
                "",
                "- `problem/`: problem statement, problem parse, assumptions, and task plan.",
                "- `modeling/`: per-question modeling ideas written before solving.",
                "- `data/raw/`: untouched attachments.",
                "- `data/processed/`: cleaned or reconstructed data.",
                "- `src/`: deterministic scripts, named by subquestion when possible.",
                "- `notebooks/`: optional exploration notebooks.",
                "- `results/`: result registry, validation report, and sensitivity outputs.",
                "- `figures/`: code-generated paper figures, GPT-image outputs, and editable roadmap exports.",
                "- `figures/ai_briefs/`: AI figure briefs that require human review.",
                "- `presentation/`: optional HTML/PPT-style presentation assets for final sharing.",
                "- `presentation/figures/`: presentation-specific figure copies or exports.",
                "- `tables/`: generated result tables and data audit tables.",
                "- `paper/`: single TeX paper entry `main.tex`, references, and compiled PDF.",
                "- `appendix/`: appendix code and supplemental material.",
                "- `logs/`: run log and error recovery log.",
                "",
                "All headline values must be registered in `results/result_registry.csv` before final writing.",
            ]
        ),
        args.overwrite,
    )

    print(f"Created full CUMCM project skeleton at: {project_dir}")
    for name in dirs:
        print(f"- {name}/")
    print("- logs/progress.jsonl")
    print("- progress.html")
    if args.open:
        open_file(project_dir / "progress.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
