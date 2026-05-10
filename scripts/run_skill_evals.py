#!/usr/bin/env python3
"""Lightweight repository checks for the CUMCM skill examples and eval prompts."""

from __future__ import annotations

import csv
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "full_problem_demo"
REAL_CASE_2025_A = ROOT / "examples" / "real_cases" / "cumcm_2025_a"

PARSER_EXPECTATIONS = {
    "prediction": {
        "question_count": 2,
        "task_types": ["prediction"],
        "attachments": ["附件1：traffic_flow.xlsx"],
        "time_ranges": ["2023 年 1 月至 2024 年 12 月", "连续 7 天", "每小时"],
        "risk_words": ["预测", "分别", "连续"],
    },
    "optimization": {
        "question_count": 2,
        "task_types": ["optimization"],
        "attachments": ["附件A：orders.csv", "附件B：vehicles.xlsx"],
        "time_ranges": ["18:00"],
        "units": ["260 件"],
        "risk_words": ["不超过", "每个", "最小", "最优"],
    },
    "evaluation": {
        "question_count": 2,
        "task_types": ["evaluation"],
        "attachments": ["附件一：city_indicators.xlsx"],
        "time_ranges": ["2020-2024"],
        "risk_words": ["每个", "至少", "分别", "评价", "排序"],
    },
    "hybrid_prediction_optimization": {
        "question_count": 2,
        "task_types": ["prediction", "optimization"],
        "attachments": ["附件1：load_history.xlsx", "附件2：generator_limits.csv"],
        "time_ranges": ["2024年1月至2025年12月", "2026-2030 年", "每小时"],
        "units": ["1200 吨"],
        "risk_words": ["预测", "分别", "不超过", "最小", "调度"],
    },
    "bracket_inline": {
        "question_count": 2,
        "task_types": ["evaluation"],
        "attachments": ["附件1：indicator_table.xlsx"],
        "time_ranges": ["2021-2025 年"],
        "units": ["20 个"],
        "risk_words": ["评价", "分别", "排序", "每个"],
    },
    "trajectory_coverage": {
        "question_count": 2,
        "task_types": ["simulation", "optimization"],
        "attachments": ["附件1：uav_state.xlsx"],
        "time_ranges": ["20 s", "1 s"],
        "units": ["3 m/s", "10 m", "20 s", "70~140 m/s", "1 s"],
        "risk_words": ["至少", "尽可能"],
        "constraints": ["3 m/s", "70~140 m/s", "至少 1 s"],
    },
    "engineering_process_control": {
        "question_count": 2,
        "task_types": ["simulation", "optimization"],
        "attachments": ["附件1：temperature_curve.xlsx"],
        "units": ["70~90 cm/min", "250 ℃", "217 ℃"],
        "risk_words": ["不超过", "满足", "最优"],
        "constraints": ["70~90 cm/min", "250 ℃", "217 ℃"],
    },
    "geometry_optics_design": {
        "question_count": 2,
        "task_types": ["simulation", "optimization"],
        "attachments": ["附件1：nodes.csv"],
        "units": ["0.6 m"],
        "risk_words": ["不超过", "连续", "最大"],
        "constraints": ["0.6 m", "连续"],
    },
}


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


def check_real_case_2025_a(issues: list[str]) -> None:
    required = [
        "README.md",
        "problem/problem_statement.pdf",
        "problem/problem_statement.md",
        "problem/problem_parse.json",
        "problem/task_plan.json",
        "src/make_problem_figures.py",
        "src/plot_utils.py",
        "src/solve_q1.py",
        "src/solve_q2.py",
        "tables/tab_q1_key_points.csv",
        "tables/tab_q1_intervals.csv",
        "tables/tab_q2_strategy.csv",
        "tables/tab_q2_intervals.csv",
        "figures/fig_problem_overview_xy.png",
        "figures/fig_problem_question_scope.png",
        "figures/fig_q1_distance_geometry.png",
        "figures/fig_q2_optimized_distance_geometry.png",
        "results/result_registry.csv",
        "results/validation_report.md",
        "results/validation_audit.md",
        "paper/main.tex",
        "paper/sections/problem_overview.tex",
        "paper/sections/q1.tex",
        "paper/sections/q2.tex",
    ]
    for rel in required:
        require(REAL_CASE_2025_A / rel, issues)

    registry = REAL_CASE_2025_A / "results" / "result_registry.csv"
    if registry.exists():
        with registry.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        ids = {row.get("id") for row in rows}
        if "R001" not in ids:
            issues.append("2025 A real case result_registry.csv should contain R001")
        if "R002" not in ids:
            issues.append("2025 A real case result_registry.csv should contain R002")
        values = {row.get("value") for row in rows}
        if "1.405510" not in values:
            issues.append("2025 A real case Q1 duration should stay traceable as 1.405510")
        if "4.723893" not in values:
            issues.append("2025 A real case Q2 duration should stay traceable as 4.723893")


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
        "references/problem-parsing.md",
        "references/task-modes.md",
        "references/cumcm-a-problem-patterns.md",
        "references/method-library.md",
        "references/method-cards.json",
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
        "evals/parser_cases/prediction/problem.md",
        "evals/parser_cases/optimization/problem.md",
        "evals/parser_cases/evaluation/problem.md",
        "evals/parser_cases/hybrid_prediction_optimization/problem.md",
        "evals/parser_cases/bracket_inline/problem.md",
        "evals/parser_cases/trajectory_coverage/problem.md",
        "evals/parser_cases/engineering_process_control/problem.md",
        "evals/parser_cases/geometry_optics_design/problem.md",
        "evals/toy_prediction_problem/prompt.md",
        "evals/toy_optimization_problem/prompt.md",
        "evals/toy_evaluation_problem/prompt.md",
    ]
    for rel in expected:
        require(ROOT / rel, issues)


def check_templates(issues: list[str]) -> None:
    required = [
        "templates/task_plan.schema.json",
        "templates/problem_parse.schema.json",
        "templates/method_card.schema.json",
    ]
    for rel in required:
        require(ROOT / rel, issues)
    for rel in required:
        path = ROOT / rel
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                issues.append(f"invalid JSON schema {rel}: {exc}")


def type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def validate_schema_value(value: Any, schema: dict, label: str, issues: list[str]) -> None:
    expected_type = schema.get("type")
    if expected_type and not type_ok(value, expected_type):
        issues.append(f"{label} should be {expected_type}, got {type(value).__name__}")
        return
    if "minimum" in schema and isinstance(value, (int, float)) and value < schema["minimum"]:
        issues.append(f"{label} should be >= {schema['minimum']}")
    if expected_type == "object":
        for field in schema.get("required", []):
            if field not in value:
                issues.append(f"{label} missing required field: {field}")
        for key, sub_schema in schema.get("properties", {}).items():
            if key in value:
                validate_schema_value(value[key], sub_schema, f"{label}.{key}", issues)
    if expected_type == "array":
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(value, start=1):
                validate_schema_value(item, item_schema, f"{label}[{idx}]", issues)


def validate_required_fields(data: dict, schema: dict, label: str, issues: list[str]) -> None:
    validate_schema_value(data, schema, label, issues)
    for field in schema.get("required", []):
        if field not in data:
            issues.append(f"{label} missing required field: {field}")
    sub_schema = schema.get("properties", {}).get("subquestions", {}).get("items", {})
    required_sub = sub_schema.get("required", [])
    for idx, item in enumerate(data.get("subquestions", []), start=1):
        for field in required_sub:
            if field not in item:
                issues.append(f"{label} subquestion {idx} missing required field: {field}")


def require_contains(items: list[str], expected: str, label: str, issues: list[str]) -> None:
    if not any(expected in str(item) for item in items):
        issues.append(f"{label} should contain: {expected}")


def check_method_cards(issues: list[str]) -> None:
    schema_path = ROOT / "templates" / "method_card.schema.json"
    cards_path = ROOT / "references" / "method-cards.json"
    if not schema_path.exists() or not cards_path.exists():
        return

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = json.loads(cards_path.read_text(encoding="utf-8"))
    validate_required_fields(data, schema, "method-cards.json", issues)

    cards = data.get("cards", [])
    if len(cards) < 5:
        issues.append("method-cards.json should contain at least five method cards")

    ids = [card.get("id", "") for card in cards]
    if len(ids) != len(set(ids)):
        issues.append("method-cards.json contains duplicate card ids")
    required_card_ids = {
        "engineering_process_control",
        "geometry_surface_optics_design",
        "trajectory_coverage_optimization",
    }
    missing_card_ids = sorted(required_card_ids - set(ids))
    if missing_card_ids:
        issues.append(f"method-cards.json missing A-problem cards: {', '.join(missing_card_ids)}")

    covered_types = {task_type for card in cards for task_type in card.get("task_types", [])}
    required_types = {"prediction", "optimization", "evaluation", "simulation", "classification", "clustering"}
    missing_types = sorted(required_types - covered_types)
    if missing_types:
        issues.append(f"method-cards.json missing task types: {', '.join(missing_types)}")

    for card in cards:
        label = card.get("id", "unknown")
        for field in ["use_when", "avoid_when", "primary_methods", "validation", "common_failures", "paper_outputs"]:
            if not card.get(field):
                issues.append(f"method card {label} should have non-empty {field}")


def check_parser_cases(issues: list[str]) -> None:
    parser = ROOT / "scripts" / "problem_parser.py"
    planner = ROOT / "scripts" / "build_task_plan.py"
    parse_schema = json.loads((ROOT / "templates" / "problem_parse.schema.json").read_text(encoding="utf-8"))
    task_schema = json.loads((ROOT / "templates" / "task_plan.schema.json").read_text(encoding="utf-8"))
    for case, expected in PARSER_EXPECTATIONS.items():
        problem = ROOT / "evals" / "parser_cases" / case / "problem.md"
        if not problem.exists():
            issues.append(f"missing parser case: {problem.relative_to(ROOT)}")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp)
            parse_cmd = [
                "python3",
                str(parser),
                "--problem",
                str(problem),
                "--output-dir",
                str(outdir),
                "--problem-id",
                case,
            ]
            plan_cmd = [
                "python3",
                str(planner),
                "--parse",
                str(outdir / "problem_parse.json"),
                "--output-dir",
                str(outdir),
                "--problem-id",
                case,
            ]
            for cmd in (parse_cmd, plan_cmd):
                result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
                if result.returncode != 0:
                    issues.append(f"command failed for parser case {case}: {' '.join(cmd)}\n{result.stderr}")
                    break
            parse_path = outdir / "problem_parse.json"
            plan_path = outdir / "task_plan.json"
            if not parse_path.exists() or not plan_path.exists():
                issues.append(f"parser case {case} did not produce parse and plan outputs")
                continue
            parsed = json.loads(parse_path.read_text(encoding="utf-8"))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            validate_required_fields(parsed, parse_schema, f"parser case {case} problem_parse.json", issues)
            validate_required_fields(plan, task_schema, f"parser case {case} task_plan.json", issues)
            if parsed.get("question_count", 0) < 1:
                issues.append(f"parser case {case} found no subquestions")
            if parsed.get("question_count") != expected["question_count"]:
                issues.append(
                    f"parser case {case} expected {expected['question_count']} subquestions, "
                    f"got {parsed.get('question_count')}"
                )
            if not parsed.get("attachments"):
                issues.append(f"parser case {case} found no attachments")
            for value in expected.get("attachments", []):
                require_contains(parsed.get("attachments", []), value, f"parser case {case} attachments", issues)
            for value in expected.get("time_ranges", []):
                require_contains(parsed.get("time_ranges", []), value, f"parser case {case} time_ranges", issues)
            for value in expected.get("units", []):
                require_contains(parsed.get("units", []), value, f"parser case {case} units", issues)
            for value in expected.get("risk_words", []):
                require_contains(parsed.get("risk_words", []), value, f"parser case {case} risk_words", issues)
            all_constraints = [constraint for q in parsed.get("subquestions", []) for constraint in q.get("constraints", [])]
            for value in expected.get("constraints", []):
                require_contains(all_constraints, value, f"parser case {case} constraints", issues)
            if any("给出了" in item or "记录" in item for item in parsed.get("attachments", [])):
                issues.append(f"parser case {case} attachment label includes descriptive text")
            if "每小" in parsed.get("time_ranges", []):
                issues.append(f"parser case {case} truncated time range 每小时 to 每小")
            task_types = {q.get("task_type") for q in parsed.get("subquestions", [])}
            for expected_type in expected.get("task_types", []):
                if expected_type not in task_types:
                    issues.append(f"parser case {case} expected task type {expected_type}, got {sorted(task_types)}")
            if plan.get("question_count") != parsed.get("question_count"):
                issues.append(f"parser case {case} plan question_count does not match parse")


def main() -> int:
    issues: list[str] = []
    check_folder_indexes(issues)
    check_reference_names(issues)
    check_templates(issues)
    check_method_cards(issues)
    check_demo(issues)
    check_real_case_2025_a(issues)
    check_eval_prompts(issues)
    check_parser_cases(issues)
    if issues:
        print("Skill eval checks failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Skill eval checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
