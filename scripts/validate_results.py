#!/usr/bin/env python3
"""Audit CUMCM project artifacts for traceability and consistency."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


NUM_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")
FIG_RE = re.compile(r"(fig_[A-Za-z0-9_./-]+\.(?:png|jpg|jpeg|pdf|svg))")
TAB_RE = re.compile(r"(tab_[A-Za-z0-9_./-]+\.(?:csv|xlsx|xls))")
FIGURE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf", ".svg"}
DATA_AUDIT_TABLE_NAMES = {
    "data_inventory.xlsx",
    "tab_categorical_profile.xlsx",
    "tab_data_inventory.xlsx",
    "tab_duplicate_summary.xlsx",
    "tab_excluded_sheets.xlsx",
    "tab_merge_candidates.xlsx",
    "tab_missing_summary.xlsx",
    "tab_numeric_profile.xlsx",
    "tab_sheet_coverage.xlsx",
    "tab_time_range_summary.xlsx",
    "tab_unit_guess.xlsx",
}
REQUIRED_FULL_PAPER_SECTIONS = [
    r"问题重述",
    r"问题分析",
    r"模型假设",
    r"符号说明",
    r"数据(?:审计|预处理|处理)",
    r"模型建立",
    r"模型检验|灵敏度|敏感性",
    r"模型评价",
    r"结论",
    r"附录|复现说明",
]
QUALITY_REQUIRED_TERMS = [
    "变量",
    "约束",
    "算法",
    "验证",
    "假设",
    "基线",
    "图",
    "表",
]
QUALITY_MODEL_TERMS = [
    "目标函数",
    "评价函数",
    "决策规则",
    "递推",
    "状态转移",
    "几何判据",
    "遮蔽判据",
    "判据",
    "误差函数",
]
MODELING_REVERSE_CHECK_TERMS = [
    "代码反向验证",
    "最终思路",
    "代码实际",
    "实现一致",
    "差异",
]
QUALITY_PROCESS_TERMS = [
    "路线",
    "比较",
    "选择",
    "可行",
    "灵敏度",
    "敏感性",
    "局限",
]


def rel_exists(root: Path, value: str) -> bool:
    if not value or str(value).lower() == "nan":
        return False
    path = Path(str(value))
    return path.exists() or (root / path).exists()


def audit_tables(root: Path) -> list[str]:
    issues: list[str] = []
    for path in list((root / "tables").rglob("*.csv")) + list((root / "tables").rglob("*.xlsx")):
        if "data_profile" in path.parts or path.name in DATA_AUDIT_TABLE_NAMES:
            continue
        try:
            df = pd.read_csv(path) if path.suffix == ".csv" else pd.read_excel(path)
        except Exception as exc:  # pragma: no cover
            issues.append(f"P1: cannot read table {path.relative_to(root)}: {exc}")
            continue
        if df.empty:
            issues.append(f"P2: empty table: {path.relative_to(root)}")
        if df.isna().any().any():
            issues.append(f"P2: table contains NaN/blank cells: {path.relative_to(root)}")
        numeric = df.select_dtypes(include="number")
        if not numeric.empty:
            bad = numeric.isin([float("inf"), float("-inf")]).any().any()
            if bad:
                issues.append(f"P1: table contains inf: {path.relative_to(root)}")
    return issues


def audit_paper(root: Path, mode: str) -> list[str]:
    issues: list[str] = []
    paper = root / "paper" / "main.tex"
    if not paper.exists():
        if (root / "paper" / "main.md").exists():
            return ["P1: full paper exists only as paper/main.md; final benchmark papers must be TeX."]
        return ["P1: paper/main.tex not found."]
    text = paper.read_text(encoding="utf-8", errors="ignore")
    for match in FIG_RE.findall(text):
        if not rel_exists(root, match) and not rel_exists(root, f"figures/{Path(match).name}"):
            issues.append(f"P1: paper references missing figure: {match}")
    for match in TAB_RE.findall(text):
        if not rel_exists(root, match) and not rel_exists(root, f"tables/{Path(match).name}"):
            issues.append(f"P1: paper references missing table: {match}")

    return issues


def read_full_paper_text(root: Path) -> str:
    paper = root / "paper" / "main.tex"
    if not paper.exists():
        return ""
    return paper.read_text(encoding="utf-8", errors="ignore")


def strip_tex_commands(text: str) -> str:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", text)
    text = re.sub(r"[{}$^_\\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def audit_paper_structure(root: Path, mode: str) -> list[str]:
    issues: list[str] = []
    if mode != "full":
        return issues
    if (root / "paper" / "main.md").exists():
        issues.append("P1: full-mode paper should not use paper/main.md; use paper/main.tex.")
    section_fragments = list((root / "paper" / "sections").glob("*.tex"))
    if section_fragments:
        issues.append(
            "P1: paper deliverable must be a single paper/main.tex; "
            "merge and remove paper/sections/*.tex."
        )
    paper = root / "paper" / "main.tex"
    if not paper.exists():
        return issues

    main_text = paper.read_text(encoding="utf-8", errors="ignore")
    full_text = read_full_paper_text(root)
    missing = [
        pattern
        for pattern in REQUIRED_FULL_PAPER_SECTIONS
        if not re.search(pattern, main_text)
    ]
    if missing:
        issues.append(
            "P1: full paper is missing required global section(s): "
            + ", ".join(missing)
        )

    top_sections = re.findall(r"\\section\{([^}]+)\}", main_text)
    if len(top_sections) < 8:
        issues.append(
            "P1: full paper has too few top-level sections; it may be a concatenation of Qx fragments."
        )
    if top_sections and all(re.search(r"问题\s*[一二三四五六七八九十\d]+|Q\s*\d+", title) for title in top_sections[: min(3, len(top_sections))]):
        issues.append("P1: full paper starts with per-question sections instead of global paper sections.")

    cleaned = strip_tex_commands(full_text)
    if len(cleaned) < 6500:
        issues.append(
            "P1: full paper is too thin; expected richer modeling prose, equations, result explanation, validation, and conclusion."
        )

    questions = solved_subquestions_from_figures(root)
    for question in questions:
        q_num = question[1:]
        q_pattern = rf"问题\s*{q_num}|问题\s*{'一二三四五六七八九十'[int(q_num)-1] if q_num.isdigit() and 1 <= int(q_num) <= 10 else q_num}|Q\s*{q_num}"
        if not re.search(q_pattern, full_text, flags=re.IGNORECASE):
            issues.append(f"P1: solved {question.upper()} is not discussed in the paper body.")

    for word in QUALITY_REQUIRED_TERMS:
        if word not in full_text:
            issues.append(f"P2: full paper does not explicitly discuss {word}.")
    if not any(word in full_text for word in QUALITY_MODEL_TERMS):
        issues.append("P1: full paper lacks a clear mathematical objective, decision rule, recurrence, or criterion.")
    missing_process = [word for word in QUALITY_PROCESS_TERMS if word not in full_text]
    if len(missing_process) >= 4:
        issues.append(
            "P2: full paper may be rushed; it lacks enough route comparison, feasibility, sensitivity, or limitation discussion."
        )
    formula_count = len(re.findall(r"\\begin\{equation\}|\\\[", full_text))
    if formula_count < 2:
        issues.append("P1: full paper has too few displayed mathematical expressions for a modeling paper.")
    figure_count = len(FIG_RE.findall(full_text))
    if figure_count < max(2, len(questions) * 2):
        issues.append("P2: full paper references too few figures for the solved subquestions.")
    return issues


def audit_modeling_ideas(root: Path, mode: str) -> list[str]:
    issues: list[str] = []
    questions = solved_subquestions_from_figures(root)
    for question in questions:
        path = root / "modeling" / f"{question}_modeling_idea.md"
        if not path.exists():
            issues.append(
                f"P1: solved {question.upper()} is missing modeling idea file: "
                f"modeling/{question}_modeling_idea.md"
            )
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        required = ["模型", "求解", "验证"]
        missing = [word for word in required if word not in text]
        if missing:
            issues.append(
                f"P2: modeling idea for {question.upper()} is too thin; missing "
                + ", ".join(missing)
            )
        if not any(term in text for term in MODELING_REVERSE_CHECK_TERMS):
            issues.append(
                f"P2: modeling idea for {question.upper()} lacks code reverse-check/final-idea notes."
            )
    return issues


def solved_subquestions_from_figures(root: Path) -> list[str]:
    figures = root / "figures"
    if not figures.exists():
        return []
    questions: set[str] = set()
    for path in figures.glob("fig_q*_*.*"):
        match = re.match(r"fig_q(\d+)_", path.name, flags=re.IGNORECASE)
        if match:
            questions.add(f"q{match.group(1)}")
    return sorted(questions)


def figure_files_for_question(root: Path, question: str) -> list[Path]:
    figures = root / "figures"
    if not figures.exists():
        return []
    return sorted(
        path
        for path in figures.glob(f"fig_{question}_*.*")
        if path.suffix.lower() in FIGURE_EXTENSIONS
    )


def audit_figure_coverage(root: Path, mode: str) -> list[str]:
    issues: list[str] = []
    questions = solved_subquestions_from_figures(root)
    for question in questions:
        figures = figure_files_for_question(root, question)
        names = [path.name for path in figures]
        if len(figures) < 2:
            issues.append(
                f"P1: solved {question.upper()} has fewer than two figures; "
                "expected a model flowchart plus a result figure."
            )
        if not any("model_flow" in name or "flowchart" in name or "流程" in name for name in names):
            issues.append(f"P1: solved {question.upper()} is missing a final model flowchart figure.")

        has_check_figure = any(
            "validation" in name or "sensitivity" in name or "feasibility" in name for name in names
        )
        has_validation_note = (root / "results" / "validation_report.md").exists()
        if len(figures) >= 2 and not has_check_figure and not has_validation_note:
            issues.append(
                f"P2: solved {question.upper()} likely needs a validation/sensitivity figure; "
                "do not omit checking figures or validation work."
            )
    return issues


def audit_unreferenced(root: Path) -> list[str]:
    issues: list[str] = []
    paper_text = ""
    for paper in (root / "paper").rglob("*.tex"):
        paper_text += paper.read_text(encoding="utf-8", errors="ignore") + "\n"
    for fig in (root / "figures").glob("fig_*.*"):
        if fig.name not in paper_text:
            issues.append(f"P2: generated figure not referenced in TeX: {fig.relative_to(root)}")
    for tab in (root / "tables").glob("tab_*.*"):
        if tab.name not in paper_text:
            issues.append(f"P2: generated table not referenced in TeX: {tab.relative_to(root)}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CUMCM project traceability.")
    parser.add_argument("--project", default=".", help="Project root.")
    parser.add_argument(
        "--mode",
        choices=["standard", "full"],
        default="standard",
        help="standard checks single-question or staged work; full additionally enforces complete-paper structure and unreferenced artifact checks.",
    )
    parser.add_argument(
        "--output",
        default="results/validation_audit.md",
        help="Audit report path relative to project.",
    )
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    issues = []
    issues.extend(audit_tables(root))
    issues.extend(audit_paper(root, args.mode))
    issues.extend(audit_paper_structure(root, args.mode))
    issues.extend(audit_modeling_ideas(root, args.mode))
    issues.extend(audit_figure_coverage(root, args.mode))
    if args.mode == "full":
        issues.extend(audit_unreferenced(root))

    out = root / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Validation Audit", "", "## Findings", ""]
    if issues:
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.append("No blocking artifact issue found by automated checks.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")
    print(f"Findings: {len(issues)}")
    return 1 if any(issue.startswith("P1") for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
