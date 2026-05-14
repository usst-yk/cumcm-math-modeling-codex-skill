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
MIN_FULL_PAPER_CHARS = 12000
MIN_FULL_QUESTION_CHARS = 2000
MIN_SINGLE_QUESTION_CHARS = 2500
MIN_CHARS_PER_VISUAL = 700
MIN_SECTION_CHARS_PER_VISUAL = 500
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
CODE_MODELING_PROCESS_TERMS = [
    "代码建模流程",
    "数据到代码变量",
    "清洗",
    "单位",
    "公式",
    "约束",
    "循环",
    "中间输出",
    "保存路径",
    "新手",
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
FIRST_PRIZE_GATES = [
    "Core mechanism",
    "Validation",
    "Traceability",
    "Paper readiness",
]
FIRST_PRIZE_PAPER_TERM_GROUPS = {
    "benchmark comparison": ["benchmark", "官方", "赛题讲评", "论文展示", "基准"],
    "model selection": ["路线", "比较", "选择", "基线", "主模型"],
    "validation": ["验证", "检验", "敏感性", "灵敏度", "可行性", "误差"],
    "limitation": ["局限", "不足", "风险", "限制"],
}
FIRST_PRIZE_MODELING_TERM_GROUPS = {
    "first-prize contribution": ["一等奖", "国一", "高水平", "冲奖", "增益点"],
    "benchmark comparison": ["benchmark", "官方", "赛题讲评", "论文展示", "基准"],
    "route comparison": ["路线", "比较"],
}
QUESTION_DENSITY_TERM_GROUPS = {
    "model": ["模型"],
    "variables": ["变量", "参数", "符号"],
    "constraint_or_assumption": ["约束", "假设"],
    "algorithm_or_solution": ["算法", "求解", "步骤", "流程"],
    "result": ["结果", "方案", "排序", "预测", "得分", "结论"],
    "validation": ["验证", "检验", "误差", "可行性", "敏感性", "灵敏度", "稳定性", "边界"],
    "limitation": ["局限", "不足", "风险", "限制"],
    "derivation": ["推导", "构造", "建立"],
    "interpretation": ["解释", "说明", "含义", "回答"],
}
CHINESE_NUMERALS = "一二三四五六七八九十"


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


def question_number(question: str) -> int | None:
    match = re.match(r"q(\d+)", question, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def question_title_pattern(question: str) -> str:
    number = question_number(question)
    if number is None:
        return re.escape(question)
    chinese = CHINESE_NUMERALS[number - 1] if 1 <= number <= len(CHINESE_NUMERALS) else str(number)
    return rf"(?:问题\s*(?:{number}|{chinese})|Q\s*{number})"


def tex_headings(text: str) -> list[tuple[str, str, int]]:
    pattern = re.compile(r"\\(section|subsection|subsubsection)\{([^}]+)\}")
    return [(match.group(1), match.group(2), match.start()) for match in pattern.finditer(text)]


def extract_question_section(text: str, question: str) -> str:
    target_re = re.compile(question_title_pattern(question), flags=re.IGNORECASE)
    headings = tex_headings(text)
    start_index = None
    for index, (_, title, start) in enumerate(headings):
        if target_re.search(title):
            start_index = index
            start_pos = start
            break
    if start_index is None:
        return ""

    end_pos = len(text)
    any_question_re = re.compile(r"问题\s*[一二三四五六七八九十\d]+|Q\s*\d+", flags=re.IGNORECASE)
    for level, title, start in headings[start_index + 1 :]:
        if any_question_re.search(title) or level == "section":
            end_pos = start
            break
    return text[start_pos:end_pos]


def has_math_expression(text: str) -> bool:
    return bool(
        re.search(r"\\begin\{equation\}|\\\[|\\\(|\$\$|目标函数|评价函数|决策规则|递推|状态转移|判据", text)
    )


def has_table_or_figure_reference(text: str) -> bool:
    return bool(
        FIG_RE.search(text)
        or TAB_RE.search(text)
        or re.search(r"\\(?:includegraphics|begin\{figure\}|begin\{table\}|ref\{(?:fig|tab|table)", text)
    )


def visual_count(text: str) -> int:
    figure_files = len(set(FIG_RE.findall(text)))
    included_figures = len(re.findall(r"\\includegraphics", text))
    figure_envs = len(re.findall(r"\\begin\{figure\}", text))
    table_files = len(set(TAB_RE.findall(text)))
    table_float_envs = len(re.findall(r"\\begin\{(?:table|longtable)\}", text))
    inline_table_envs = len(re.findall(r"\\begin\{(?:tabularx|tabular)\}", text))
    table_count = table_float_envs if table_float_envs else inline_table_envs
    return max(figure_files, included_figures, figure_envs) + max(table_files, table_count)


def audit_paper_density(root: Path, mode: str) -> list[str]:
    issues: list[str] = []
    if mode != "full":
        return issues
    paper = root / "paper" / "main.tex"
    if not paper.exists():
        return issues
    full_text = paper.read_text(encoding="utf-8", errors="ignore")
    cleaned_full = strip_tex_commands(full_text)
    questions = first_prize_subquestions(root)

    if len(cleaned_full) < MIN_FULL_PAPER_CHARS:
        issues.append(
            "P1: full paper is too thin; expected at least "
            f"{MIN_FULL_PAPER_CHARS} cleaned characters with derivation, result interpretation, validation, and limitations."
        )
    full_visuals = visual_count(full_text)
    if full_visuals and len(cleaned_full) < full_visuals * MIN_CHARS_PER_VISUAL:
        issues.append(
            "P1: full paper is too figure/table dominated; expected more explanatory prose "
            f"around {full_visuals} visual/table artifact(s)."
        )

    for question in questions:
        section_text = extract_question_section(full_text, question)
        if not section_text:
            continue
        cleaned_section = strip_tex_commands(section_text)
        min_chars = MIN_SINGLE_QUESTION_CHARS if len(questions) == 1 else MIN_FULL_QUESTION_CHARS
        if len(cleaned_section) < min_chars:
            issues.append(
                f"P1: solved {question.upper()} paper section is too thin; "
                f"expected at least {min_chars} cleaned characters."
            )
        section_visuals = visual_count(section_text)
        if section_visuals and len(cleaned_section) < section_visuals * MIN_SECTION_CHARS_PER_VISUAL:
            issues.append(
                f"P1: solved {question.upper()} paper section is too figure/table dominated; "
                "expand the prose explanation or move secondary visuals/tables out of the body."
            )
        for label, terms in QUESTION_DENSITY_TERM_GROUPS.items():
            if not any(term in cleaned_section for term in terms):
                severity = "P1" if label in {"validation", "limitation", "derivation", "interpretation"} else "P2"
                issues.append(f"{severity}: solved {question.upper()} paper section lacks {label} content.")
        if not has_math_expression(section_text):
            issues.append(
                f"P1: solved {question.upper()} paper section lacks a formula or explicit mathematical criterion."
            )
        if not has_table_or_figure_reference(section_text):
            issues.append(
                f"P1: solved {question.upper()} paper section lacks a table or figure reference."
            )
    return issues


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
        missing_code_process = [
            term for term in CODE_MODELING_PROCESS_TERMS if term not in text
        ]
        if missing_code_process:
            issues.append(
                f"P2: modeling idea for {question.upper()} lacks detailed code modeling process terms: "
                + ", ".join(missing_code_process)
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


def first_prize_subquestions(root: Path) -> list[str]:
    questions = set(solved_subquestions_from_figures(root))
    modeling = root / "modeling"
    if modeling.exists():
        for path in modeling.glob("q*_modeling_idea.md"):
            match = re.match(r"q(\d+)_modeling_idea\.md", path.name, flags=re.IGNORECASE)
            if match:
                questions.add(f"q{match.group(1)}")
    return sorted(questions)


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def audit_first_prize_gate(root: Path) -> list[str]:
    issues: list[str] = []
    report = root / "results" / "validation_report.md"
    if not report.exists():
        return ["P1: CUMCM validation requires results/validation_report.md with First-prize gate."]

    text = report.read_text(encoding="utf-8", errors="ignore")
    if "First-prize gate" not in text:
        issues.append("P1: validation report is missing the First-prize gate section.")

    for gate in FIRST_PRIZE_GATES:
        row = next(
            (
                line
                for line in text.splitlines()
                if line.strip().startswith("|")
                and table_cells(line)
                and table_cells(line)[0].lower() == gate.lower()
            ),
            "",
        )
        if not row:
            issues.append(f"P1: First-prize gate is missing row: {gate}.")
            continue
        cells = table_cells(row)
        if len(cells) < 5:
            issues.append(f"P1: First-prize gate row is incomplete: {gate}.")
            continue
        score, evidence, status, action = cells[1:5]
        if not score or score == "0":
            issues.append(f"P1: First-prize gate {gate} lacks a passing score.")
        if not evidence:
            issues.append(f"P1: First-prize gate {gate} lacks evidence file.")
        elif not rel_exists(root, evidence):
            issues.append(f"P2: First-prize gate {gate} evidence path may not exist: {evidence}.")
        blocking_terms = ["blocker", "fail", "p1", "不通过", "阻断", "缺失", "未通过"]
        passing_terms = ["pass", "通过", "ok", "无阻断"]
        status_lower = status.lower()
        if any(term in status_lower for term in blocking_terms):
            issues.append(f"P1: First-prize gate {gate} is still blocking: {status}.")
        if not any(term in status_lower for term in passing_terms) and not action:
            issues.append(f"P1: First-prize gate {gate} needs status or rework action.")
    return issues


def audit_first_prize_paper(root: Path) -> list[str]:
    issues: list[str] = []
    paper = root / "paper" / "main.tex"
    if not paper.exists():
        return ["P1: CUMCM validation requires paper/main.tex."]
    text = paper.read_text(encoding="utf-8", errors="ignore")
    for label, terms in FIRST_PRIZE_PAPER_TERM_GROUPS.items():
        if not any(term in text for term in terms):
            issues.append(f"P1: first-prize paper lacks {label} content.")
    return issues


def audit_first_prize_modeling_ideas(root: Path) -> list[str]:
    issues: list[str] = []
    questions = first_prize_subquestions(root)
    if not questions:
        issues.append("P1: CUMCM validation found no solved subquestion or modeling idea file.")
    for question in questions:
        path = root / "modeling" / f"{question}_modeling_idea.md"
        if not path.exists():
            issues.append(
                f"P1: CUMCM validation requires modeling/{question}_modeling_idea.md."
            )
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, terms in FIRST_PRIZE_MODELING_TERM_GROUPS.items():
            matched = all(term in text for term in terms)
            if label in {"first-prize contribution", "benchmark comparison"}:
                matched = any(term in text for term in terms)
            if not matched:
                issues.append(
                    f"P1: {path.relative_to(root)} lacks first-prize {label} terms."
                )
        if not any(term in text for term in MODELING_REVERSE_CHECK_TERMS):
            issues.append(
                f"P1: {path.relative_to(root)} lacks code reverse-check/final-idea notes."
            )
        missing_code_process = [
            term for term in CODE_MODELING_PROCESS_TERMS if term not in text
        ]
        if missing_code_process:
            issues.append(
                f"P1: {path.relative_to(root)} lacks detailed code modeling process terms: "
                + ", ".join(missing_code_process)
            )
    return issues


def audit_first_prize(root: Path) -> list[str]:
    issues: list[str] = []
    issues.extend(audit_first_prize_gate(root))
    issues.extend(audit_first_prize_paper(root))
    issues.extend(audit_first_prize_modeling_ideas(root))
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
    parser.add_argument(
        "--first-prize",
        action="store_true",
        default=True,
        help="enforce first-prize critical gates, benchmark comparison, and modeling contribution checks (default).",
    )
    parser.add_argument(
        "--no-first-prize",
        dest="first_prize",
        action="store_false",
        help="skip first-prize gate checks for lightweight compatibility audits.",
    )
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    issues = []
    issues.extend(audit_tables(root))
    issues.extend(audit_paper(root, args.mode))
    issues.extend(audit_paper_structure(root, args.mode))
    issues.extend(audit_paper_density(root, args.mode))
    issues.extend(audit_modeling_ideas(root, args.mode))
    issues.extend(audit_figure_coverage(root, args.mode))
    if args.mode == "full":
        issues.extend(audit_unreferenced(root))
    if args.first_prize:
        issues.extend(audit_first_prize(root))

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
