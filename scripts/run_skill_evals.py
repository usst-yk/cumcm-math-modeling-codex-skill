#!/usr/bin/env python3
"""Lightweight checks for the slim CUMCM skill package."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
REAL_CASES = EXAMPLES / "real_cases"
CASE_A = REAL_CASES / "cumcm_2025_a"
CASE_HUADONG = REAL_CASES / "huadong_cup_a"

STANDARD_DIRS = {"problem", "data", "modeling", "src", "tables", "figures", "results", "paper"}
FORBIDDEN_CASE_DIRS = {"logs", "build", "appendix", "presentation", "notebooks", "references"}
MODELING_TERMS = [
    "变量",
    "公式",
    "约束",
    "验证",
    "图表",
    "代码反向验证",
    "最终思路",
]
PAPER_SECTIONS = ["问题重述", "问题分析", "模型假设", "符号说明", "模型建立", "模型检验", "模型评价", "结论"]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def require(path: Path, issues: list[str]) -> None:
    if not path.exists():
        issues.append(f"missing: {rel(path)}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def check_examples_are_slim(issues: list[str]) -> None:
    require(EXAMPLES / "README.md", issues)
    require(REAL_CASES / "README.md", issues)
    allowed_top = {"README.md", "real_cases"}
    for item in EXAMPLES.iterdir():
        if item.name not in allowed_top:
            issues.append(f"examples should only keep README.md and real_cases/: {rel(item)}")

    allowed_cases = {"README.md", "cumcm_2025_a", "huadong_cup_a"}
    for item in REAL_CASES.iterdir():
        if item.name not in allowed_cases:
            issues.append(f"real_cases should only keep CUMCM A and Huadong A: {rel(item)}")


def check_case_layout(root: Path, label: str, qids: tuple[str, ...], issues: list[str]) -> None:
    require(root / "README.md", issues)
    for dirname in STANDARD_DIRS:
        require(root / dirname, issues)
    for dirname in FORBIDDEN_CASE_DIRS:
        if (root / dirname).exists():
            issues.append(f"{label} should not contain non-standard folder: {dirname}")

    require(root / "paper" / "main.tex", issues)
    require(root / "problem" / "problem_parse.json", issues)
    require(root / "problem" / "task_plan.json", issues)
    require(root / "results" / "result_registry.csv", issues)
    require(root / "results" / "validation_report.md", issues)

    for qid in qids:
        check_modeling_idea(root / "modeling" / f"{qid}_modeling_idea.md", f"{label} {qid.upper()}", issues)
        figures = list((root / "figures").glob(f"fig_{qid}_*.*"))
        if len(figures) < 2:
            issues.append(f"{label} {qid.upper()} should keep at least model/result figures")
        if not any("model_flow" in fig.name for fig in figures):
            issues.append(f"{label} {qid.upper()} should keep a model flow figure")

    check_registry(root, label, issues)
    check_paper(root, label, issues)


def check_modeling_idea(path: Path, label: str, issues: list[str]) -> None:
    require(path, issues)
    if not path.exists():
        return
    text = read(path)
    for term in MODELING_TERMS:
        if term not in text:
            issues.append(f"{label} modeling idea should mention: {term}")


def check_registry(root: Path, label: str, issues: list[str]) -> None:
    registry = root / "results" / "result_registry.csv"
    if not registry.exists():
        return
    with registry.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        issues.append(f"{label} result registry should not be empty")
        return
    for idx, row in enumerate(rows, start=1):
        source = str(row.get("source_file", "")).strip()
        if source and not (root / source).exists():
            issues.append(f"{label} registry row {idx} source not found: {source}")
        status = str(row.get("status", "")).lower()
        if status in {"blocked", "failed"}:
            issues.append(f"{label} registry row {idx} has blocked/failed status")


def clean_tex(text: str) -> str:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", text)
    text = re.sub(r"[{}$^_\\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def check_paper(root: Path, label: str, issues: list[str]) -> None:
    paper = root / "paper" / "main.tex"
    if not paper.exists():
        return
    text = read(paper)
    if list((root / "paper" / "sections").glob("*.tex")):
        issues.append(f"{label} should keep a single paper/main.tex, not paper/sections/*.tex")
    for section in PAPER_SECTIONS:
        if section not in text:
            issues.append(f"{label} paper should contain section: {section}")
    if "\\appendix" not in text and "附录" not in text:
        issues.append(f"{label} paper should contain an appendix or appendix-equivalent note")
    if len(clean_tex(text)) < 5000:
        issues.append(f"{label} paper looks too thin for a benchmark case")


def check_prompt_router(issues: list[str]) -> None:
    router = ROOT / "references" / "prompt-router.md"
    require(router, issues)
    if not router.exists():
        return
    text = read(router)
    for term in ["examples/README.md", "Step 13", "Per-Question Agent Pattern", "Output Contract"]:
        if term not in text:
            issues.append(f"prompt-router.md should mention: {term}")
    skill = read(ROOT / "SKILL.md")
    if "references/prompt-router.md" not in skill:
        issues.append("SKILL.md should route broad requests through references/prompt-router.md")


def check_task_plans(issues: list[str]) -> None:
    for root, label, expected_count in [(CASE_A, "CUMCM 2025 A", 5), (CASE_HUADONG, "Huadong Cup A", 2)]:
        path = root / "problem" / "task_plan.json"
        if not path.exists():
            continue
        plan = json.loads(read(path))
        if len(plan.get("subquestions", [])) < expected_count:
            issues.append(f"{label} task_plan should contain at least {expected_count} subquestions")


def main() -> int:
    issues: list[str] = []
    check_examples_are_slim(issues)
    check_case_layout(CASE_A, "CUMCM 2025 A", ("q1", "q2", "q3", "q4", "q5"), issues)
    check_case_layout(CASE_HUADONG, "Huadong Cup A", ("q1", "q2"), issues)
    check_prompt_router(issues)
    check_task_plans(issues)
    if issues:
        print("Skill eval checks failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Skill eval checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
