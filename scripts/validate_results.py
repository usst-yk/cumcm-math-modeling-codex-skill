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


def read_registry(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    return pd.read_csv(path)


def rel_exists(root: Path, value: str) -> bool:
    if not value or str(value).lower() == "nan":
        return False
    path = Path(str(value))
    return path.exists() or (root / path).exists()


def audit_registry(root: Path, registry: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    if registry.empty:
        return ["P1: result registry missing or empty."]
    source_col = (
        "source_file"
        if "source_file" in registry.columns
        else "source_path"
        if "source_path" in registry.columns
        else ""
    )
    if source_col:
        for idx, row in registry.iterrows():
            source = str(row.get(source_col, "")).strip()
            if source and source.lower() != "nan" and not rel_exists(root, source):
                issues.append(f"P1: registry row {idx + 1} source file not found: {source}")
    if "figure_or_table" in registry.columns:
        for idx, row in registry.iterrows():
            artifact = str(row.get("figure_or_table", "")).strip()
            if artifact and artifact.lower() != "nan" and not rel_exists(root, artifact):
                if not rel_exists(root, f"figures/{Path(artifact).name}") and not rel_exists(
                    root,
                    f"tables/{Path(artifact).name}",
                ):
                    issues.append(f"P1: registry row {idx + 1} linked figure/table not found: {artifact}")
    if "source_type" in registry.columns:
        missing_type = registry[registry["source_type"].astype(str).str.strip().isin(["", "nan"])]
        if not missing_type.empty:
            issues.append(f"P2: registry has {len(missing_type)} row(s) without source_type.")
    status_col = "status" if "status" in registry.columns else ""
    if status_col:
        blocked = registry[registry[status_col].astype(str).str.lower().isin(["blocked", "failed"])]
        if not blocked.empty:
            issues.append(f"P1: registry contains {len(blocked)} blocked/failed result row(s).")
    if "claim" in registry.columns:
        evidence_cols = [col for col in ["solver_status", "validation", "notes"] if col in registry.columns]
        for idx, row in registry.iterrows():
            claim = str(row.get("claim", ""))
            if not re.search(r"最优|最小|最大|optimal|optimum", claim, flags=re.IGNORECASE):
                continue
            evidence = " ".join(str(row.get(col, "")) for col in evidence_cols)
            if not re.search(r"solver|status|可行|feasible|约束|violation", evidence, flags=re.IGNORECASE):
                issues.append(f"P2: registry row {idx + 1} claims optimality without solver/feasibility evidence.")
    return issues


def audit_tables(root: Path) -> list[str]:
    issues: list[str] = []
    for path in list((root / "tables").rglob("*.csv")) + list((root / "tables").rglob("*.xlsx")):
        if "data_profile" in path.parts:
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


def audit_paper(root: Path, registry: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    paper = root / "paper" / "main.tex"
    if not paper.exists():
        return ["P2: paper/main.tex not found."]
    text = paper.read_text(encoding="utf-8", errors="ignore")
    for match in FIG_RE.findall(text):
        if not rel_exists(root, match) and not rel_exists(root, f"figures/{Path(match).name}"):
            issues.append(f"P1: paper references missing figure: {match}")
    for match in TAB_RE.findall(text):
        if not rel_exists(root, match) and not rel_exists(root, f"tables/{Path(match).name}"):
            issues.append(f"P1: paper references missing table: {match}")

    if not registry.empty:
        values = set()
        for col in ["value", "claim"]:
            if col in registry.columns:
                values.update(str(v) for v in registry[col].dropna().tolist())
        abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", text, flags=re.S)
        if abstract:
            numbers = [n for n in NUM_RE.findall(abstract.group(1)) if n not in {"1", "2", "3"}]
            missing = [n for n in numbers if not any(n in v for v in values)]
            if missing:
                issues.append(f"P1: abstract number(s) not found in result registry: {', '.join(sorted(set(missing)))}")
    return issues


def registry_artifact_names(registry: pd.DataFrame) -> set[str]:
    names: set[str] = set()
    if registry.empty:
        return names
    for col in ["source_file", "source_path", "figure_or_table"]:
        if col in registry.columns:
            for value in registry[col].dropna().astype(str):
                if value and value.lower() != "nan":
                    names.add(Path(value).name)
    return names


def solved_subquestions(registry: pd.DataFrame) -> list[str]:
    if registry.empty or "subquestion" not in registry.columns:
        return []
    questions: set[str] = set()
    for value in registry["subquestion"].dropna().astype(str):
        match = re.search(r"q\s*(\d+)", value, flags=re.IGNORECASE)
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


def audit_figure_coverage(root: Path, registry: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    for question in solved_subquestions(registry):
        figures = figure_files_for_question(root, question)
        names = [path.name for path in figures]
        if len(figures) < 2:
            issues.append(
                f"P1: solved {question.upper()} has fewer than two figures; "
                "expected a model/problem schematic plus a result figure."
            )
        if not any("schematic" in name or "示意" in name for name in names):
            issues.append(f"P1: solved {question.upper()} is missing a model/problem schematic figure.")

        if "subquestion" not in registry.columns:
            continue
        q_rows = registry[registry["subquestion"].astype(str).str.lower().str.replace(" ", "") == question]
        q_text = " ".join(
            str(row.get(col, ""))
            for _, row in q_rows.iterrows()
            for col in ["claim", "validation", "notes"]
        )
        needs_check_figure = re.search(
            r"优化|最优|搜索|best-found|可行|约束|敏感|扰动|边界|validation|feasibility|sensitivity",
            q_text,
            flags=re.IGNORECASE,
        )
        has_check_figure = any(
            "validation" in name or "sensitivity" in name or "feasibility" in name for name in names
        )
        if needs_check_figure and len(figures) < 3 and not has_check_figure:
            issues.append(
                f"P2: solved {question.upper()} likely needs a validation/sensitivity figure; "
                "lean output should remove templates, not checking figures."
            )
    return issues


def audit_unreferenced(root: Path, registry: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    paper_text = ""
    for paper in (root / "paper").rglob("*.tex"):
        paper_text += paper.read_text(encoding="utf-8", errors="ignore") + "\n"
    registered = registry_artifact_names(registry)
    for fig in (root / "figures").glob("fig_*.*"):
        if fig.name not in paper_text and fig.name not in registered:
            issues.append(f"P2: generated figure not referenced in TeX: {fig.relative_to(root)}")
    for tab in (root / "tables").glob("tab_*.*"):
        if tab.name not in paper_text and tab.name not in registered:
            issues.append(f"P2: generated table not referenced in TeX: {tab.relative_to(root)}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CUMCM project traceability.")
    parser.add_argument("--project", default=".", help="Project root.")
    parser.add_argument(
        "--registry",
        default="results/result_registry.csv",
        help="Registry path relative to project.",
    )
    parser.add_argument(
        "--output",
        default="results/validation_audit.md",
        help="Audit report path relative to project.",
    )
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    registry = read_registry(root / args.registry)
    issues = []
    issues.extend(audit_registry(root, registry))
    issues.extend(audit_tables(root))
    issues.extend(audit_paper(root, registry))
    issues.extend(audit_figure_coverage(root, registry))
    issues.extend(audit_unreferenced(root, registry))

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
