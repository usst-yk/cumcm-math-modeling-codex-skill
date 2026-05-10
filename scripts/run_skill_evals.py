#!/usr/bin/env python3
"""Lightweight repository checks for the CUMCM skill examples and eval prompts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "full_problem_demo"


def require(path: Path, issues: list[str]) -> None:
    if not path.exists():
        issues.append(f"missing: {path.relative_to(ROOT)}")


def check_demo(issues: list[str]) -> None:
    required = [
        "README.md",
        "prompt_full_problem.md",
        "prompt_single_question.md",
        "prompt_code_to_paper.md",
        "prompt_roadmap.md",
        "prompt_final_review.md",
    ]
    for rel in required:
        require(ROOT / "examples" / rel, issues)

    demo_required = [
        "problem/problem_statement.md",
        "problem/task_plan.json",
        "data/raw/station_demand.csv",
        "src/solve_demo.py",
        "tables/tab_q1_daily_forecast.csv",
        "tables/tab_q2_allocation.csv",
        "tables/tab_q3_priority_ranking.csv",
        "figures/fig_q1_demand_forecast.png",
        "figures/fig_q3_priority_ranking.png",
        "figures/roadmap.svg",
        "results/result_registry.csv",
        "results/validation_report.md",
        "paper/main.tex",
        "paper/sections/q1.tex",
    ]
    for rel in demo_required:
        require(DEMO / rel, issues)

    task_plan = DEMO / "problem" / "task_plan.json"
    if task_plan.exists():
        data = json.loads(task_plan.read_text(encoding="utf-8"))
        subquestions = data.get("subquestions", [])
        ids = {item.get("id") for item in subquestions}
        if not {"Q1", "Q2", "Q3"}.issubset(ids):
            issues.append("demo task_plan.json should contain Q1, Q2, and Q3")

    registry = DEMO / "results" / "result_registry.csv"
    if registry.exists():
        with registry.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        ids = {row.get("id") for row in rows}
        if not {"R001", "R002", "R003"}.issubset(ids):
            issues.append("demo result_registry.csv should contain R001-R003")
        for row in rows:
            source = row.get("source_file", "")
            if source and not (DEMO / source).exists():
                issues.append(f"registry source not found: {source}")


def check_folder_indexes(issues: list[str]) -> None:
    expected = [
        "agents/README.md",
        "assets/README.md",
        "evals/README.md",
        "examples/README.md",
        "references/README.md",
        "scripts/README.md",
        "templates/README.md",
    ]
    for rel in expected:
        require(ROOT / rel, issues)


def check_reference_names(issues: list[str]) -> None:
    expected = [
        "references/task-modes.md",
        "references/method-library.md",
        "references/paper-section-flow.md",
        "references/external-agent-patterns.md",
    ]
    for rel in expected:
        require(ROOT / rel, issues)
    deprecated = [
        "references/" + "contest" + "-" + "modes.md",
        "references/" + "modeling" + "-" + "toolbox.md",
    ]
    for rel in deprecated:
        if (ROOT / rel).exists():
            issues.append(f"deprecated reference name still exists: {rel}")


def check_eval_prompts(issues: list[str]) -> None:
    expected = [
        "evals/expected_outputs.md",
        "evals/toy_prediction_problem/prompt.md",
        "evals/toy_optimization_problem/prompt.md",
        "evals/toy_evaluation_problem/prompt.md",
    ]
    for rel in expected:
        require(ROOT / rel, issues)


def main() -> int:
    issues: list[str] = []
    check_folder_indexes(issues)
    check_reference_names(issues)
    check_demo(issues)
    check_eval_prompts(issues)
    if issues:
        print("Skill eval checks failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Skill eval checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
