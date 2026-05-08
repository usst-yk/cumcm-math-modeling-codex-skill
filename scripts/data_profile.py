#!/usr/bin/env python3
"""Profile CSV/XLSX files and draft a Chinese data preprocessing section."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pandas. Install with `python3 -m pip install pandas openpyxl`.") from exc


CSV_SUFFIXES = {".csv", ".txt"}
XLSX_SUFFIXES = {".xlsx", ".xls"}


def discover_inputs(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            for suffix in sorted(CSV_SUFFIXES | XLSX_SUFFIXES):
                files.extend(sorted(path.glob(f"*{suffix}")))
        elif path.suffix.lower() in CSV_SUFFIXES | XLSX_SUFFIXES:
            files.append(path)
    return files


def read_csv(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path)


def load_frames(path: Path) -> dict[str, pd.DataFrame]:
    suffix = path.suffix.lower()
    if suffix in CSV_SUFFIXES:
        return {path.stem: read_csv(path)}
    if suffix in XLSX_SUFFIXES:
        sheets = pd.read_excel(path, sheet_name=None)
        return {f"{path.stem}__{name}": df for name, df in sheets.items()}
    return {}


def iqr_outlier_count(series: pd.Series) -> int:
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if numeric.empty:
        return 0
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        return 0
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return int(((numeric < lower) | (numeric > upper)).sum())


def profile_frame(name: str, df: pd.DataFrame) -> dict:
    numeric_cols = list(df.select_dtypes(include="number").columns)
    missing = df.isna().sum().sort_values(ascending=False)
    outliers = {col: iqr_outlier_count(df[col]) for col in numeric_cols}
    stats = df[numeric_cols].describe().round(6).to_dict() if numeric_cols else {}
    corr = df[numeric_cols].corr().round(6) if len(numeric_cols) >= 2 else pd.DataFrame()
    return {
        "name": name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": [str(c) for c in df.columns],
        "numeric_columns": [str(c) for c in numeric_cols],
        "missing": {str(k): int(v) for k, v in missing.items() if int(v) > 0},
        "outliers_iqr": {str(k): int(v) for k, v in outliers.items() if int(v) > 0},
        "stats": stats,
        "correlation": corr.to_dict() if not corr.empty else {},
    }


def md_table(rows: list[list[object]], headers: list[str]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(lines)


def write_report(profiles: list[dict], outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    summary_lines = ["# 数据检查报告", ""]
    draft_lines = ["# 数据预处理论文段落草稿", ""]

    overview_rows = [[p["name"], p["rows"], p["columns"], len(p["numeric_columns"])] for p in profiles]
    summary_lines += ["## 数据表概览", "", md_table(overview_rows, ["数据表", "行数", "列数", "数值列数"]), ""]

    for p in profiles:
        summary_lines += [f"## {p['name']}", ""]
        summary_lines += [f"- 字段：{', '.join(p['column_names'])}", ""]
        if p["missing"]:
            rows = [[k, v, f"{v / max(p['rows'], 1):.2%}"] for k, v in p["missing"].items()]
            summary_lines += ["### 缺失值", "", md_table(rows, ["字段", "缺失数", "缺失比例"]), ""]
        else:
            summary_lines += ["### 缺失值", "", "未发现缺失值。", ""]

        if p["outliers_iqr"]:
            rows = [[k, v] for k, v in p["outliers_iqr"].items()]
            summary_lines += ["### IQR 异常值", "", md_table(rows, ["字段", "异常值数量"]), ""]
        else:
            summary_lines += ["### IQR 异常值", "", "数值字段未发现明显 IQR 异常值。", ""]

        if p["stats"]:
            stat_rows = []
            for col, values in p["stats"].items():
                stat_rows.append(
                    [
                        col,
                        values.get("count", ""),
                        values.get("mean", ""),
                        values.get("std", ""),
                        values.get("min", ""),
                        values.get("50%", ""),
                        values.get("max", ""),
                    ]
                )
            summary_lines += [
                "### 基础统计",
                "",
                md_table(stat_rows, ["字段", "count", "mean", "std", "min", "median", "max"]),
                "",
            ]

        if p["correlation"]:
            corr_path = outdir / f"{p['name']}_correlation.csv"
            pd.DataFrame(p["correlation"]).to_csv(corr_path, encoding="utf-8-sig")
            summary_lines += [f"### 相关性", "", f"数值字段相关系数矩阵已保存至 `{corr_path.name}`。", ""]

        missing_text = "未发现缺失值" if not p["missing"] else "存在缺失值，主要集中在 " + "、".join(list(p["missing"].keys())[:5])
        outlier_text = "未发现明显异常值" if not p["outliers_iqr"] else "部分数值字段存在 IQR 异常值，主要包括 " + "、".join(list(p["outliers_iqr"].keys())[:5])
        draft_lines += [
            f"## {p['name']}",
            "",
            f"数据表 `{p['name']}` 共包含 {p['rows']} 条记录、{p['columns']} 个字段，其中数值型字段 {len(p['numeric_columns'])} 个。经初步检查，{missing_text}；{outlier_text}。后续建模中，应结合题意对缺失字段采用删除、插值、均值/中位数填补或模型估计等方式处理，并对异常值进行来源核查。对于量纲不同的指标，建议在评价、聚类或回归建模前进行标准化处理，以避免量纲差异对模型结果造成不合理影响。",
            "",
        ]

    (outdir / "data_profile_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")
    (outdir / "data_preprocessing_draft.md").write_text("\n".join(draft_lines), encoding="utf-8")
    (outdir / "data_profile.json").write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile CSV/XLSX files for CUMCM modeling.")
    parser.add_argument("inputs", nargs="+", help="CSV/XLSX files or directories containing data files.")
    parser.add_argument("--outdir", default="tables/data_profile", help="Output directory.")
    args = parser.parse_args()

    files = discover_inputs(args.inputs)
    if not files:
        print("No CSV/XLSX files found.", file=sys.stderr)
        return 2

    profiles: list[dict] = []
    for file in files:
        for name, df in load_frames(file).items():
            profiles.append(profile_frame(name, df))

    write_report(profiles, Path(args.outdir).expanduser().resolve())
    print(f"Profiled {len(profiles)} data table(s).")
    print(f"Reports written to: {Path(args.outdir).expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
