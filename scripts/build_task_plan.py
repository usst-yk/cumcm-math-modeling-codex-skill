#!/usr/bin/env python3
"""Create a reusable CUMCM task_plan.json/task_plan.md template."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def infer_question_count(text: str, default: int) -> int:
    patterns = [r"第[一二三四五六七八九十\d]+问", r"问题[一二三四五六七八九十\d]+", r"Q\d+"]
    hits: set[str] = set()
    for pattern in patterns:
        hits.update(re.findall(pattern, text, flags=re.IGNORECASE))
    return max(default, len(hits) or default)


def build_plan(problem_text: str, question_count: int, problem_id: str) -> dict:
    subquestions = []
    for idx in range(1, question_count + 1):
        subquestions.append(
            {
                "id": f"Q{idx}",
                "task_type": "unknown",
                "required_output": [],
                "input_data": [],
                "decision_object": "",
                "constraints": [],
                "validation": ["baseline comparison"],
                "figures_needed": [f"fig_q{idx}_result.png"],
                "tables_needed": [f"tab_q{idx}_result.csv"],
                "status": "draft",
            }
        )
    return {
        "contest": "CUMCM",
        "problem_id": problem_id,
        "question_count": question_count,
        "subquestions": subquestions,
        "global_assumptions": [],
        "risk_points": [],
        "source_excerpt": problem_text[:1000],
    }


def write_markdown(plan: dict, path: Path) -> None:
    lines = ["# Task Plan", "", f"- Contest: {plan['contest']}", f"- Problem: {plan.get('problem_id', '')}", ""]
    lines.append("| ID | Type | Input | Model object | Output | Validation |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for q in plan["subquestions"]:
        lines.append(
            "| {id} | {task_type} | {input_data} | {decision_object} | {required_output} | {validation} |".format(
                id=q["id"],
                task_type=q["task_type"],
                input_data="; ".join(q["input_data"]),
                decision_object=q["decision_object"],
                required_output="; ".join(q["required_output"]),
                validation="; ".join(q["validation"]),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build CUMCM task_plan.json and task_plan.md templates.")
    parser.add_argument("--problem", help="Problem statement markdown/text file.")
    parser.add_argument("--output-dir", default="problem", help="Output directory.")
    parser.add_argument("--question-count", type=int, default=3, help="Default question count.")
    parser.add_argument("--problem-id", default="", help="Problem id, e.g. 2026A.")
    args = parser.parse_args()

    text = ""
    if args.problem:
        text = Path(args.problem).expanduser().read_text(encoding="utf-8")
    question_count = infer_question_count(text, args.question_count)
    plan = build_plan(text, question_count, args.problem_id)

    outdir = Path(args.output_dir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "task_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(plan, outdir / "task_plan.md")
    print(f"Wrote {outdir / 'task_plan.json'}")
    print(f"Wrote {outdir / 'task_plan.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
