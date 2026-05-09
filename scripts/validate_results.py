#!/usr/bin/env python3
"""Audit CUMCM project artifacts for traceability and consistency."""

from __future__ import annotations

import argparse
import math
import re
from pathlib import Path

import pandas as pd


NUM_RE = re.compile(r"(?<![A-Za-z])\d+(?:\.\d+)?%?")
FIG_RE = re.compile(r"(fig_[A-Za-z0-9_./-]+\.(?:png|jpg|jpeg|pdf|svg))")
TAB_RE = re.compile(r"(tab_[A-Za-z0-9_./-]+\.(?:csv|xlsx|xls))")


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
    source_col = "source_file" if "source_file" in registry.columns else "source_path" if "source_path" in registry.columns else ""
    if source_col:
        for idx, row in registry.iterrows():
            source = str(row.get(source_col, "")).strip()
            if source and source.lower() != "nan" and not rel_exists(root, source):
                issues.append(f"P1: registry row {idx + 1} source file not found: {source}")
    status_col = "status" if "status" in registry.columns else ""
    if status_col:
        blocked = registry[registry[status_col].astype(str).str.lower().isin(["blocked", "failed"])]
        if not blocked.empty:
            issues.append(f"P1: registry contains {len(blocked)} blocked/failed result row(s).")
    return issues


def audit_tables(root: Path) -> list[str]:
    issues: list[str] = []
    for path in list((root / "tables").rglob("*.csv")) + list((root / "tables").rglob("*.xlsx")):
        try:
            df = pd.read_csv(path) if path.suffix == ".csv" else pd.read_excel(path)
        except Exception as exc:  # pragma: no cover
            issues.append(f"P1: cannot read table {path.relative_to(root)}: {exc}")
            continue
        if df.empty:
            issues.append(f"P2: empty table: {path.relative_to(root)}")
        numeric = df.select_dtypes(include="number")
        if not numeric.empty:
            bad = numeric.applymap(lambda x: isinstance(x, float) and (math.isnan(x) or math.isinf(x))).any().any()
            if bad:
                issues.append(f"P1: table contains NaN or inf: {path.relative_to(root)}")
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
    parser.add_argument("--registry", default="results/result_registry.csv", help="Registry path relative to project.")
    parser.add_argument("--output", default="results/validation_audit.md", help="Audit report path relative to project.")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    registry = read_registry(root / args.registry)
    issues = []
    issues.extend(audit_registry(root, registry))
    issues.extend(audit_tables(root))
    issues.extend(audit_paper(root, registry))
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
