#!/usr/bin/env python3
"""Build CUMCM task_plan.json/task_plan.md from problem_parse.json first."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SPARSE_FIELDS = ["required_output", "input_data", "decision_object", "constraints"]
CHECK_FIGURE_TYPES = {"prediction", "optimization", "evaluation", "simulation"}


def infer_question_count(text: str, default: int) -> int:
    patterns = [r"第[一二三四五六七八九十\d]+问", r"问题[一二三四五六七八九十\d]+", r"Q\s*\d+", r"[（(]\s*\d+\s*[）)]"]
    hits: set[str] = set()
    for pattern in patterns:
        hits.update(re.findall(pattern, text, flags=re.IGNORECASE))
    return max(default, len(hits) or default)


def empty_value(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, list):
        return len(value) == 0
    return False


def infer_validation(task_type: str, scoring_points: list[str]) -> list[str]:
    validation = list(scoring_points)
    defaults = {
        "prediction": ["baseline comparison", "error metric"],
        "optimization": ["feasibility check", "baseline scheme comparison"],
        "evaluation": ["ranking stability", "weight perturbation"],
        "simulation": ["parameter sensitivity", "boundary case"],
        "classification": ["confusion matrix", "F1 score"],
        "clustering": ["cluster stability", "cluster interpretation"],
    }
    validation.extend(defaults.get(task_type, ["baseline comparison"]))
    return list(dict.fromkeys(validation))


def infer_figures(qid: str, task_type: str) -> list[str]:
    qid_lower = qid.lower()
    figures = [
        f"fig_{qid_lower}_model_schematic.png",
        f"fig_{qid_lower}_result.png",
    ]
    if task_type in CHECK_FIGURE_TYPES:
        check_name = "sensitivity" if task_type == "optimization" else "validation"
        figures.append(f"fig_{qid_lower}_{check_name}.png")
    return figures


def build_empty_plan(problem_text: str, question_count: int, problem_id: str) -> dict:
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
                "figures_needed": infer_figures(f"Q{idx}", "unknown"),
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
        "warnings": ["No problem_parse.json found; generated a sparse draft plan."],
    }


def build_plan_from_parse(parsed: dict, problem_id: str) -> dict:
    warnings = list(parsed.get("warnings", []))
    subquestions = []
    for idx, item in enumerate(parsed.get("subquestions", []), start=1):
        qid = item.get("id") or f"Q{idx}"
        task_type = item.get("task_type") or "unknown"
        subq = {
            "id": qid,
            "task_type": task_type,
            "required_output": item.get("required_output", []),
            "input_data": item.get("input_data", []),
            "decision_object": item.get("decision_object", ""),
            "constraints": item.get("constraints", []),
            "validation": infer_validation(task_type, item.get("implicit_scoring_points", [])),
            "figures_needed": infer_figures(qid, task_type),
            "tables_needed": [f"tab_{qid.lower()}_result.csv"],
            "status": "draft",
            "parse_source": "problem_parse.json",
            "parse_warnings": item.get("warnings", []),
        }
        empty_count = sum(1 for field in SPARSE_FIELDS if empty_value(subq[field]))
        if empty_count >= 2:
            warnings.append(f"{qid}: task plan fields are sparse; confirm required output, input data, decision object, and constraints.")
            subq["status"] = "needs_review"
        subquestions.append(subq)

    if not subquestions:
        warnings.append("problem_parse.json contains no subquestions; generated one draft Q1 item.")
        subquestions = build_empty_plan("", 1, problem_id).get("subquestions", [])

    return {
        "contest": parsed.get("contest", "CUMCM"),
        "problem_id": problem_id or parsed.get("problem_id", ""),
        "question_count": len(subquestions),
        "subquestions": subquestions,
        "global_assumptions": [],
        "risk_points": parsed.get("risk_words", []) + parsed.get("warnings", []),
        "source_excerpt": "",
        "warnings": warnings,
    }


def write_markdown(plan: dict, path: Path) -> None:
    lines = [
        "# Task Plan",
        "",
        f"- Contest: {plan['contest']}",
        f"- Problem: {plan.get('problem_id', '')}",
        f"- Question count: {plan.get('question_count', 0)}",
        "",
    ]
    if plan.get("warnings"):
        lines.append("## Warnings")
        lines.extend(f"- {warning}" for warning in plan["warnings"])
        lines.append("")
    lines.append("| ID | Type | Input | Model object | Output | Validation | Status |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")
    for q in plan["subquestions"]:
        lines.append(
            "| {id} | {task_type} | {input_data} | {decision_object} | {required_output} | {validation} | {status} |".format(
                id=q["id"],
                task_type=q["task_type"],
                input_data="; ".join(q.get("input_data", [])),
                decision_object=q.get("decision_object", ""),
                required_output="; ".join(q.get("required_output", [])),
                validation="; ".join(q.get("validation", [])),
                status=q.get("status", ""),
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build CUMCM task_plan.json and task_plan.md.")
    parser.add_argument("--problem", help="Problem statement markdown/text file.")
    parser.add_argument("--parse", help="problem_parse.json path. Defaults to <output-dir>/problem_parse.json.")
    parser.add_argument("--output-dir", default="problem", help="Output directory.")
    parser.add_argument("--question-count", type=int, default=3, help="Fallback question count.")
    parser.add_argument("--problem-id", default="", help="Problem id, e.g. 2026A.")
    args = parser.parse_args()

    outdir = Path(args.output_dir).expanduser().resolve()
    parse_path = Path(args.parse).expanduser() if args.parse else outdir / "problem_parse.json"

    if parse_path.exists():
        parsed = json.loads(parse_path.read_text(encoding="utf-8"))
        plan = build_plan_from_parse(parsed, args.problem_id)
    else:
        text = ""
        if args.problem:
            text = Path(args.problem).expanduser().read_text(encoding="utf-8")
        question_count = infer_question_count(text, args.question_count)
        plan = build_empty_plan(text, question_count, args.problem_id)

    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "task_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(plan, outdir / "task_plan.md")
    print(f"Wrote {outdir / 'task_plan.json'}")
    print(f"Wrote {outdir / 'task_plan.md'}")
    if plan.get("warnings"):
        print("Warnings:")
        for warning in plan["warnings"]:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
