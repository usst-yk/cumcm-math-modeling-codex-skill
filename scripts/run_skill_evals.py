#!/usr/bin/env python3
"""Lightweight repository checks for the CUMCM skill examples and eval prompts."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "examples" / "full_problem_demo"
REAL_CASE_2025_A = ROOT / "examples" / "real_cases" / "cumcm_2025_a"
REAL_CASE_HUADONG_A = ROOT / "examples" / "real_cases" / "huadong_cup_a"
CHECK_FIGURE_TYPES = {"prediction", "optimization", "evaluation", "simulation", "scheduling"}
MODELING_IDEA_TERMS = [
    "变量",
    "公式",
    "约束",
    "验证",
    "图表",
    "代码反向验证",
    "最终思路",
]
MODELING_TEMPLATE_TERMS = ["逐步推导", "GPT-image", "论文写法", "代码反向验证"]

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


def check_modeling_idea(path: Path, label: str, issues: list[str]) -> None:
    require(path, issues)
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    for term in MODELING_IDEA_TERMS:
        if term not in text:
            issues.append(f"{label} should mention modeling idea item: {term}")


def check_demo(issues: list[str]) -> None:
    required = [
        "README.md",
    ]
    for rel in required:
        require(ROOT / "examples" / rel, issues)

    demo_required = [
        "../single_question_minimal/README.md",
        "../single_question_minimal/problem.md",
        "../single_question_minimal/modeling/q1_modeling_idea.md",
        "../single_question_minimal/src/solve_q1.py",
        "../single_question_minimal/tables/tab_q1_result.csv",
        "../single_question_minimal/modeling/q1_model_flow_prompt.md",
        "../single_question_minimal/figures/fig_q1_model_flow.png",
        "../single_question_minimal/figures/fig_q1_result.png",
        "../single_question_minimal/results/result_registry.csv",
        "../single_question_minimal/paper/main.tex",
        "problem/problem_statement.md",
        "problem/task_plan.json",
        "modeling/q1_modeling_idea.md",
        "modeling/q2_modeling_idea.md",
        "modeling/q3_modeling_idea.md",
        "modeling/route_comparison.md",
        "data/raw/station_demand.csv",
        "src/solve_demo.py",
        "tables/tab_q1_daily_forecast.csv",
        "tables/tab_q2_allocation.csv",
        "tables/tab_q3_priority_ranking.csv",
        "figures/fig_q1_model_schematic.svg",
        "figures/fig_q1_demand_forecast.png",
        "figures/fig_q1_validation.svg",
        "figures/fig_q2_model_schematic.svg",
        "figures/fig_q2_result.svg",
        "figures/fig_q2_sensitivity.svg",
        "figures/fig_q3_model_schematic.svg",
        "figures/fig_q3_priority_ranking.png",
        "figures/fig_q3_validation.svg",
        "figures/roadmap.svg",
        "results/result_registry.csv",
        "results/validation_report.md",
        "paper/main.tex",
    ]
    for rel in demo_required:
        require((DEMO / rel).resolve(), issues)

    check_modeling_idea(
        ROOT / "examples" / "single_question_minimal" / "modeling" / "q1_modeling_idea.md",
        "single question modeling idea",
        issues,
    )
    for qid in ("q1", "q2", "q3"):
        check_modeling_idea(
            DEMO / "modeling" / f"{qid}_modeling_idea.md",
            f"full demo {qid.upper()} modeling idea",
            issues,
        )

    task_plan = DEMO / "problem" / "task_plan.json"
    if task_plan.exists():
        data = json.loads(task_plan.read_text(encoding="utf-8"))
        score_task_plan_quality(data, "full_problem_demo task_plan.json", issues, min_score=11)
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
        "modeling/route_comparison.md",
        "modeling/q1_modeling_idea.md",
        "modeling/q2_modeling_idea.md",
        "modeling/q3_modeling_idea.md",
        "modeling/q4_modeling_idea.md",
        "modeling/q5_modeling_idea.md",
        "src/make_problem_figures.py",
        "src/plot_utils.py",
        "src/solve_q1.py",
        "src/solve_q2.py",
        "src/solve_q3_q5.py",
        "tables/tab_q1_key_points.csv",
        "tables/tab_q1_intervals.csv",
        "tables/tab_q2_strategy.csv",
        "tables/tab_q2_intervals.csv",
        "tables/tab_q3_strategy.csv",
        "tables/tab_q3_intervals.csv",
        "tables/tab_q4_strategy.csv",
        "tables/tab_q4_intervals.csv",
        "tables/tab_q5_strategy.csv",
        "tables/tab_q5_intervals.csv",
        "tables/result1_benchmark.xlsx",
        "tables/result2_benchmark.xlsx",
        "tables/result3_benchmark.xlsx",
        "figures/fig_problem_overview_xy.png",
        "figures/fig_problem_question_scope.png",
        "figures/fig_q1_model_schematic.png",
        "figures/fig_q1_distance_geometry.png",
        "figures/fig_q1_validation_margin.png",
        "figures/fig_q2_model_schematic.png",
        "figures/fig_q2_optimized_distance_geometry.png",
        "figures/fig_q2_sensitivity.png",
        "figures/fig_q3_model_schematic.png",
        "figures/fig_q3_result.png",
        "figures/fig_q3_validation.png",
        "figures/fig_q4_model_schematic.png",
        "figures/fig_q4_result.png",
        "figures/fig_q4_validation.png",
        "figures/fig_q5_model_schematic.png",
        "figures/fig_q5_result.png",
        "figures/fig_q5_validation.png",
        "results/result_registry.csv",
        "results/validation_report.md",
        "results/validation_audit.md",
        "results/benchmark_findings.md",
        "paper/main.tex",
    ]
    for rel in required:
        require(REAL_CASE_2025_A / rel, issues)

    for qid in ("q1", "q2", "q3", "q4", "q5"):
        check_modeling_idea(
            REAL_CASE_2025_A / "modeling" / f"{qid}_modeling_idea.md",
            f"2025 A {qid.upper()} modeling idea",
            issues,
        )

    registry = REAL_CASE_2025_A / "results" / "result_registry.csv"
    task_plan = REAL_CASE_2025_A / "problem" / "task_plan.json"
    if task_plan.exists():
        score_task_plan_quality(
            json.loads(task_plan.read_text(encoding="utf-8")),
            "2025 A real case task_plan.json",
            issues,
            min_score=11,
        )
    if registry.exists():
        with registry.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        ids = {row.get("id") for row in rows}
        if "R001" not in ids:
            issues.append("2025 A real case result_registry.csv should contain R001")
        if "R002" not in ids:
            issues.append("2025 A real case result_registry.csv should contain R002")
        for expected_id in ("R003", "R004", "R005"):
            if expected_id not in ids:
                issues.append(f"2025 A real case result_registry.csv should contain {expected_id}")
        values = {row.get("value") for row in rows}
        if "1.405510" not in values:
            issues.append("2025 A real case Q1 duration should stay traceable as 1.405510")
        if "4.723893" not in values:
            issues.append("2025 A real case Q2 duration should stay traceable as 4.723893")
        if "4.740000" not in values:
            issues.append("2025 A real case Q3 duration should stay traceable as 4.740000")
        if "14.520000" not in values:
            issues.append("2025 A real case Q4 duration should stay traceable as 14.520000")
        if "M1=22.980000; M2=18.360000; M3=6.400000" not in values:
            issues.append("2025 A real case Q5 durations should stay traceable")
        solved = {row.get("subquestion", "").lower() for row in rows}
        for question in sorted(q for q in solved if q.startswith("q")):
            figures = list((REAL_CASE_2025_A / "figures").glob(f"fig_{question}_*.*"))
            if len(figures) < 3:
                issues.append(f"2025 A real case solved {question.upper()} should keep at least 3 figures")
            if not any("schematic" in fig.name or "model_flow" in fig.name for fig in figures):
                issues.append(f"2025 A real case solved {question.upper()} should include a model flowchart or schematic figure")
    check_full_paper_structure(REAL_CASE_2025_A, "2025 A benchmark paper", issues, min_chars=7000)


def clean_tex_text(text: str) -> str:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", text)
    text = re.sub(r"[{}$^_\\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def check_full_paper_structure(root: Path, label: str, issues: list[str], min_chars: int = 4000) -> None:
    paper = root / "paper" / "main.tex"
    markdown_paper = root / "paper" / "main.md"
    if markdown_paper.exists():
        issues.append(f"{label} should use paper/main.tex for final papers, not paper/main.md")
    if not paper.exists():
        issues.append(f"{label} missing paper/main.tex")
        return
    main_text = paper.read_text(encoding="utf-8", errors="ignore")
    full_text = main_text
    section_fragments = list((root / "paper" / "sections").glob("*.tex"))
    if section_fragments:
        issues.append(f"{label} should be a single paper/main.tex and must not use paper/sections/*.tex")
    required = [
        "问题重述",
        "问题分析",
        "模型假设",
        "符号说明",
        "数据",
        "模型建立",
        "模型检验",
        "模型评价",
        "结论",
        "附录",
    ]
    for item in required:
        if item == "附录" and "\\appendix" in main_text:
            continue
        if item not in main_text:
            issues.append(f"{label} should contain global section: {item}")
    cleaned = clean_tex_text(full_text)
    if len(cleaned) < min_chars:
        issues.append(f"{label} is too thin; expected richer modeling prose and validation")
    top_sections = re.findall(r"\\section\{([^}]+)\}", main_text)
    if len(top_sections) < 8:
        issues.append(f"{label} should have a complete paper structure, not only per-question fragments")
    if "代码反向验证" not in main_text or "最终建模思路" not in main_text:
        issues.append(
            f"{label} should explain code reverse-check and the final code-verified modeling idea"
        )


def check_real_case_huadong_a(issues: list[str]) -> None:
    required = [
        "README.md",
        "problem/problem_statement.pdf",
        "problem/problem_statement.md",
        "problem/problem_parse.json",
        "problem/problem_parse.md",
        "problem/task_plan.json",
        "problem/task_plan.md",
        "modeling/route_comparison.md",
        "modeling/q1_modeling_idea.md",
        "modeling/q2_modeling_idea.md",
        "data/raw/benchmark_activities.csv",
        "data/raw/realtime_wait_updates.csv",
        "src/plot_utils.py",
        "src/solve_routes.py",
        "tables/tab_q1_summary.csv",
        "tables/tab_q1_routes.csv",
        "tables/tab_q1_baseline_comparison.csv",
        "tables/tab_q2_realtime_waits.csv",
        "tables/tab_q2_adjustment_summary.csv",
        "tables/tab_q2_adjusted_routes.csv",
        "figures/fig_problem_overview.png",
        "figures/fig_q1_model_schematic.png",
        "figures/fig_q1_result.png",
        "figures/fig_q1_validation.png",
        "figures/fig_q2_model_schematic.png",
        "figures/fig_q2_result.png",
        "figures/fig_q2_validation.png",
        "results/result_registry.csv",
        "results/validation_report.md",
        "paper/main.tex",
    ]
    for rel in required:
        require(REAL_CASE_HUADONG_A / rel, issues)

    for qid in ("q1", "q2"):
        check_modeling_idea(
            REAL_CASE_HUADONG_A / "modeling" / f"{qid}_modeling_idea.md",
            f"Huadong Cup A {qid.upper()} modeling idea",
            issues,
        )

    task_plan = REAL_CASE_HUADONG_A / "problem" / "task_plan.json"
    if task_plan.exists():
        plan = json.loads(task_plan.read_text(encoding="utf-8"))
        if plan.get("question_count") != 2:
            issues.append("Huadong Cup A benchmark should contain exactly 2 subquestions")
        score_task_plan_quality(plan, "Huadong Cup A benchmark task_plan.json", issues, min_score=11)

    q1_summary = REAL_CASE_HUADONG_A / "tables" / "tab_q1_summary.csv"
    q2_summary = REAL_CASE_HUADONG_A / "tables" / "tab_q2_adjustment_summary.csv"
    if q1_summary.exists():
        with q1_summary.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 9:
            issues.append("Huadong Cup A Q1 summary should contain 9 visitor-date scenarios")
        if not any(row.get("persona") == "家庭亲子游" and row.get("day_type") == "节假日" and row.get("activity_count_without_rest") == "9" for row in rows):
            issues.append("Huadong Cup A holiday family benchmark should keep 9 non-rest experiences")
    if q2_summary.exists():
        with q2_summary.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != 9:
            issues.append("Huadong Cup A Q2 summary should contain 9 visitor-date scenarios")
        changed = sum(1 for row in rows if int(float(row.get("changed_activity_count", 0))) > 0)
        if changed != 6:
            issues.append("Huadong Cup A Q2 should keep 6 changed scenarios")

    registry = REAL_CASE_HUADONG_A / "results" / "result_registry.csv"
    if registry.exists():
        with registry.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        values = {row.get("id"): row.get("value") for row in rows}
        expected = {"R001": "16.74", "R002": "9", "R003": "19.67", "R004": "6"}
        for key, value in expected.items():
            if values.get(key) != value:
                issues.append(f"Huadong Cup A registry {key} should stay traceable as {value}")
    check_full_paper_structure(REAL_CASE_HUADONG_A, "Huadong Cup A benchmark paper", issues, min_chars=7000)


def check_folder_indexes(issues: list[str]) -> None:
    expected = [
        "agents/README.md",
        "agents/abstract_writer.md",
        "agents/paper_assembler.md",
        "evals/README.md",
        "examples/README.md",
        "references/README.md",
        "scripts/README.md",
        "templates/README.md",
    ]
    for rel in expected:
        require(ROOT / rel, issues)


def check_font_assets(issues: list[str]) -> None:
    for rel in [
        "assets/fonts/NotoSansCJKsc-Regular.otf",
        "assets/fonts/NotoSansCJKsc-Bold.otf",
        "assets/fonts/OFL.txt",
    ]:
        require(ROOT / rel, issues)
    style = ROOT / "scripts" / "make_paper_figures.py"
    if style.exists():
        text = style.read_text(encoding="utf-8", errors="ignore")
        for term in ["NotoSansCJKsc-Regular.otf", "NotoSansCJKsc-Bold.otf", "Times New Roman"]:
            if term not in text:
                issues.append(f"make_paper_figures.py should configure bundled font item: {term}")


def check_reference_names(issues: list[str]) -> None:
    expected = [
        "references/problem-parsing.md",
        "references/task-modes.md",
        "references/cumcm-a-problem-patterns.md",
        "references/official-benchmark.md",
        "references/first-prize-rubric.md",
        "references/output-policy.md",
        "references/method-library.md",
        "references/method-cards.json",
        "references/paper-assembly.md",
        "references/paper-quality-standard.md",
        "references/benchmark-rebuild.md",
        "references/paper-section-flow.md",
        "references/external-agent-patterns.md",
        "references/figure-plan.md",
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
        "evals/modeling_quality_rubric.json",
        "evals/official_cases/README.md",
        "evals/official_cases/official_case_index.json",
        "evals/parser_cases/prediction/problem.md",
        "evals/parser_cases/prediction/expected_problem_parse.json",
        "evals/parser_cases/optimization/problem.md",
        "evals/parser_cases/optimization/expected_problem_parse.json",
        "evals/parser_cases/evaluation/problem.md",
        "evals/parser_cases/evaluation/expected_problem_parse.json",
        "evals/parser_cases/hybrid_prediction_optimization/problem.md",
        "evals/parser_cases/hybrid_prediction_optimization/expected_problem_parse.json",
        "evals/parser_cases/bracket_inline/problem.md",
        "evals/parser_cases/bracket_inline/expected_problem_parse.json",
        "evals/parser_cases/trajectory_coverage/problem.md",
        "evals/parser_cases/trajectory_coverage/expected_problem_parse.json",
        "evals/parser_cases/engineering_process_control/problem.md",
        "evals/parser_cases/engineering_process_control/expected_problem_parse.json",
        "evals/parser_cases/geometry_optics_design/problem.md",
        "evals/parser_cases/geometry_optics_design/expected_problem_parse.json",
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
    modeling_template = ROOT / "templates" / "modeling_idea.md"
    require(modeling_template, issues)
    if modeling_template.exists():
        text = modeling_template.read_text(encoding="utf-8", errors="ignore")
        for term in MODELING_TEMPLATE_TERMS:
            if term not in text:
                issues.append(f"modeling_idea.md template should mention: {term}")


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
        if "minItems" in schema and len(value) < schema["minItems"]:
            issues.append(f"{label} should contain at least {schema['minItems']} item(s)")
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


def parser_golden_summary(parsed: dict) -> dict:
    return {
        "question_count": parsed.get("question_count"),
        "attachments": parsed.get("attachments", []),
        "units": parsed.get("units", []),
        "time_ranges": parsed.get("time_ranges", []),
        "risk_words": parsed.get("risk_words", []),
        "subquestions": [
            {
                "id": item.get("id"),
                "task_type": item.get("task_type"),
                "required_output": item.get("required_output", []),
                "input_data": item.get("input_data", []),
                "decision_object": item.get("decision_object", ""),
                "constraints": item.get("constraints", []),
            }
            for item in parsed.get("subquestions", [])
        ],
    }


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
        for field in [
            "use_when",
            "avoid_when",
            "primary_methods",
            "validation",
            "minimum_validation",
            "common_failures",
            "paper_outputs",
        ]:
            if not card.get(field):
                issues.append(f"method card {label} should have non-empty {field}")
        if len(card.get("avoid_when", [])) < 2:
            issues.append(f"method card {label} should have at least two avoid_when items")
        if len(card.get("minimum_validation", [])) < 2:
            issues.append(f"method card {label} should have at least two minimum_validation items")


def check_quality_rubric(issues: list[str]) -> None:
    path = ROOT / "evals" / "modeling_quality_rubric.json"
    if not path.exists():
        issues.append("missing modeling quality rubric")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"invalid modeling_quality_rubric.json: {exc}")
        return

    criteria = data.get("criteria", [])
    if len(criteria) < 8:
        issues.append("modeling_quality_rubric.json should contain at least 8 criteria")
    required_ids = {
        "problem_coverage",
        "route_comparison",
        "baseline",
        "data_and_units",
        "model_formulation",
        "validation",
        "figures",
        "traceability",
        "paper_readiness",
    }
    ids = {item.get("id") for item in criteria}
    missing = sorted(required_ids - ids)
    if missing:
        issues.append(f"modeling_quality_rubric.json missing criteria: {', '.join(missing)}")
    for item in criteria:
        if item.get("max_score") != 2:
            issues.append(f"rubric criterion {item.get('id', 'unknown')} should use 0-2 scoring")
        if not item.get("pass_condition"):
            issues.append(f"rubric criterion {item.get('id', 'unknown')} missing pass_condition")
        if not item.get("beginner_visible_check"):
            issues.append(f"rubric criterion {item.get('id', 'unknown')} missing beginner_visible_check")


def check_official_cases(issues: list[str]) -> None:
    script = ROOT / "scripts" / "build_official_case_index.py"
    require(script, issues)
    index = ROOT / "evals" / "official_cases" / "official_case_index.json"
    if not script.exists() or not index.exists():
        return
    result = subprocess.run(
        ["python3", str(script), "--index", str(index)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        issues.append(f"official case index validation failed:\n{result.stdout}{result.stderr}")


def score_task_plan_quality(plan: dict, label: str, issues: list[str], min_score: int = 10) -> None:
    subquestions = plan.get("subquestions", [])
    if not subquestions:
        issues.append(f"{label} has no subquestions for quality scoring")
        return

    for item in subquestions:
        qid = str(item.get("id", "Q?"))
        task_type = str(item.get("task_type", "unknown")).lower()
        q_label = f"{label} {qid}"
        score = 0
        checks = [
            bool(task_type and task_type != "unknown"),
            bool(item.get("required_output")),
            bool(item.get("input_data")),
            bool(str(item.get("decision_object", "")).strip()),
            bool(item.get("constraints")),
            len(item.get("validation", [])) >= 2,
            bool(str(item.get("baseline_route", "")).strip()),
            bool(str(item.get("primary_route", "")).strip()),
            bool(str(item.get("fallback_route", "")).strip()),
            len(item.get("minimum_validation", [])) >= 2,
            bool(item.get("tables_needed")),
        ]
        score += sum(1 for passed in checks if passed)

        figures = [str(fig).lower() for fig in item.get("figures_needed", [])]
        if any("model_flow" in fig or "flow" in fig or "schematic" in fig for fig in figures):
            score += 1
        else:
            issues.append(f"{q_label} should include a model flowchart figure")
        if any("result" in fig or "forecast" in fig or "ranking" in fig or "geometry" in fig for fig in figures):
            score += 1
        else:
            issues.append(f"{q_label} should include a core result figure")
        if task_type in CHECK_FIGURE_TYPES:
            if any("validation" in fig or "sensitivity" in fig or "feasibility" in fig for fig in figures):
                score += 1
            else:
                issues.append(f"{q_label} should include a validation/sensitivity/feasibility figure")
        else:
            score += 1

        if score < min_score:
            issues.append(f"{q_label} modeling quality score {score}/14 is below {min_score}")


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
            for q in plan.get("subquestions", []):
                figures = q.get("figures_needed", [])
                qid = str(q.get("id", "")).lower()
                if f"fig_{qid}_model_flow.png" not in figures:
                    issues.append(f"parser case {case} {qid.upper()} plan missing model flowchart figure")
                if f"fig_{qid}_result.png" not in figures:
                    issues.append(f"parser case {case} {qid.upper()} plan missing result figure")
                for field in ["baseline_route", "primary_route", "fallback_route"]:
                    if not q.get(field):
                        issues.append(f"parser case {case} {qid.upper()} plan missing {field}")
                if len(q.get("minimum_validation", [])) < 2:
                    issues.append(f"parser case {case} {qid.upper()} plan missing minimum validation")
            golden_path = problem.parent / "expected_problem_parse.json"
            if not golden_path.exists():
                issues.append(f"parser case {case} missing golden output: {golden_path.relative_to(ROOT)}")
                continue
            expected_golden = json.loads(golden_path.read_text(encoding="utf-8"))
            actual_golden = parser_golden_summary(parsed)
            if actual_golden != expected_golden:
                issues.append(f"parser case {case} problem_parse golden output changed")


def main() -> int:
    issues: list[str] = []
    check_folder_indexes(issues)
    check_font_assets(issues)
    check_reference_names(issues)
    check_templates(issues)
    check_method_cards(issues)
    check_quality_rubric(issues)
    check_official_cases(issues)
    check_demo(issues)
    check_real_case_2025_a(issues)
    check_real_case_huadong_a(issues)
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
