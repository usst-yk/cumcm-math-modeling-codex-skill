#!/usr/bin/env python3
"""Profile CSV/XLSX inputs for CUMCM data audits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: pandas. Install with: python3 -m pip install pandas openpyxl") from exc


CSV_SUFFIXES = {".csv", ".txt", ".tsv"}
XLSX_SUFFIXES = {".xlsx", ".xls"}
JSON_SUFFIXES = {".json"}
DATA_SUFFIXES = CSV_SUFFIXES | XLSX_SUFFIXES | JSON_SUFFIXES


def discover_inputs(inputs: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw in inputs:
        path = Path(raw).expanduser().resolve()
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in DATA_SUFFIXES and not child.name.startswith("~$"):
                    files.append(child)
        elif path.is_file() and path.suffix.lower() in DATA_SUFFIXES:
            files.append(path)
    return sorted(dict.fromkeys(files))


def read_csv(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "utf-8", "gbk", "gb18030"):
        try:
            if path.suffix.lower() == ".tsv":
                return pd.read_csv(path, encoding=encoding, sep="\t")
            return pd.read_csv(path, encoding=encoding)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path)


def load_tables(path: Path) -> list[tuple[str, str, pd.DataFrame]]:
    suffix = path.suffix.lower()
    if suffix in CSV_SUFFIXES:
        return [(path.name, path.stem, read_csv(path))]
    if suffix in JSON_SUFFIXES:
        data = pd.read_json(path)
        if isinstance(data, pd.Series):
            data = data.to_frame("value")
        return [(path.name, path.stem, data)]
    if suffix in XLSX_SUFFIXES:
        workbook = pd.ExcelFile(path)
        tables: list[tuple[str, str, pd.DataFrame]] = []
        for sheet in workbook.sheet_names:
            tables.append((path.name, sheet, pd.read_excel(workbook, sheet_name=sheet)))
        return tables
    return []


def is_numeric_like(series: pd.Series) -> bool:
    converted = pd.to_numeric(series, errors="coerce")
    return converted.notna().sum() >= max(3, int(series.notna().sum() * 0.8))


def iqr_outliers(series: pd.Series) -> int:
    numeric = pd.to_numeric(series, errors="coerce").dropna()
    if len(numeric) < 4:
        return 0
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    if iqr == 0:
        return 0
    return int(((numeric < q1 - 1.5 * iqr) | (numeric > q3 + 1.5 * iqr)).sum())


def likely_time_columns(df: pd.DataFrame) -> list[str]:
    result: list[str] = []
    keywords = ("date", "time", "year", "month", "day", "日期", "时间", "年份", "月份", "日")
    for col in df.columns:
        name = str(col)
        if any(key in name.lower() for key in keywords):
            result.append(name)
            continue
        if not pd.api.types.is_object_dtype(df[col]) and not pd.api.types.is_string_dtype(df[col]):
            continue
        sample = df[col].dropna().astype(str).head(20)
        if sample.empty or not sample.str.contains(r"[-/:年月日]", regex=True).any():
            continue
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().sum() >= max(3, int(df[col].notna().sum() * 0.7)):
            result.append(name)
    return result


def table_signature(df: pd.DataFrame) -> str:
    cols = [str(c).strip().lower() for c in df.columns]
    return "|".join(cols)


def profile_table(file_path: Path, file_name: str, sheet_name: str, df: pd.DataFrame) -> dict[str, object]:
    rows, cols = df.shape
    numeric_cols = [str(c) for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) or is_numeric_like(df[c])]
    categorical_cols = [str(c) for c in df.columns if str(c) not in numeric_cols]
    time_cols = likely_time_columns(df)
    return {
        "source_path": str(file_path),
        "file": file_name,
        "sheet": sheet_name,
        "rows": int(rows),
        "columns": int(cols),
        "column_names": [str(c) for c in df.columns],
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "time_columns": time_cols,
        "signature": table_signature(df),
        "empty": bool(rows == 0 or cols == 0),
    }


def build_outputs(files: list[Path]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict[str, object]]]:
    inventory: list[dict[str, object]] = []
    missing_rows: list[dict[str, object]] = []
    numeric_rows: list[dict[str, object]] = []
    categorical_rows: list[dict[str, object]] = []
    sheet_rows: list[dict[str, object]] = []
    time_rows: list[dict[str, object]] = []
    duplicate_rows: list[dict[str, object]] = []
    excluded_rows: list[dict[str, object]] = []
    profiles: list[dict[str, object]] = []
    signatures: dict[str, int] = {}

    for path in files:
        tables = load_tables(path)
        for file_name, sheet_name, df in tables:
            profile = profile_table(path, file_name, sheet_name, df)
            profiles.append(profile)
            signatures[profile["signature"]] = signatures.get(profile["signature"], 0) + 1

            inventory.append(
                {
                    "source_path": str(path),
                    "file": file_name,
                    "sheet": sheet_name,
                    "rows": profile["rows"],
                    "columns": profile["columns"],
                    "columns_list": "; ".join(profile["column_names"]),
                    "numeric_columns": "; ".join(profile["numeric_columns"]),
                    "categorical_columns": "; ".join(profile["categorical_columns"]),
                    "time_columns": "; ".join(profile["time_columns"]),
                    "included_status": "to_review",
                    "exclusion_reason": "",
                }
            )

            sheet_rows.append(
                {
                    "file": file_name,
                    "sheet": sheet_name,
                    "rows": profile["rows"],
                    "columns": profile["columns"],
                    "empty": profile["empty"],
                    "same_structure_sheet_count": "",
                    "included_status": "to_review",
                    "exclusion_reason": "",
                }
            )

            if profile["empty"]:
                excluded_rows.append({"file": file_name, "sheet": sheet_name, "reason": "empty sheet/table"})

            duplicate_rows.append(
                {
                    "file": file_name,
                    "sheet": sheet_name,
                    "duplicate_full_rows": int(df.duplicated().sum()) if not df.empty else 0,
                    "rows": int(len(df)),
                }
            )

            for tcol in profile["time_columns"]:
                parsed = pd.to_datetime(df[tcol], errors="coerce")
                time_rows.append(
                    {
                        "file": file_name,
                        "sheet": sheet_name,
                        "column": tcol,
                        "non_null_time_count": int(parsed.notna().sum()),
                        "min_time": "" if parsed.dropna().empty else str(parsed.min()),
                        "max_time": "" if parsed.dropna().empty else str(parsed.max()),
                    }
                )

            for col in df.columns:
                missing_count = int(df[col].isna().sum())
                missing_rows.append(
                    {
                        "file": file_name,
                        "sheet": sheet_name,
                        "column": str(col),
                        "dtype": str(df[col].dtype),
                        "non_null_count": int(df[col].notna().sum()),
                        "missing_count": missing_count,
                        "missing_ratio": missing_count / max(len(df), 1),
                    }
                )

                if str(col) in profile["numeric_columns"]:
                    numeric = pd.to_numeric(df[col], errors="coerce")
                    desc = numeric.describe(percentiles=[0.25, 0.5, 0.75])
                    numeric_rows.append(
                        {
                            "file": file_name,
                            "sheet": sheet_name,
                            "column": str(col),
                            "count": float(desc.get("count", 0)),
                            "mean": float(desc.get("mean", float("nan"))),
                            "std": float(desc.get("std", float("nan"))),
                            "min": float(desc.get("min", float("nan"))),
                            "q25": float(desc.get("25%", float("nan"))),
                            "median": float(desc.get("50%", float("nan"))),
                            "q75": float(desc.get("75%", float("nan"))),
                            "max": float(desc.get("max", float("nan"))),
                            "iqr_outliers": iqr_outliers(df[col]),
                        }
                    )
                else:
                    values = df[col].dropna().astype(str)
                    top = values.value_counts().head(5)
                    categorical_rows.append(
                        {
                            "file": file_name,
                            "sheet": sheet_name,
                            "column": str(col),
                            "unique_count": int(values.nunique()),
                            "top_values": "; ".join(f"{idx}:{val}" for idx, val in top.items()),
                        }
                    )

    for row in sheet_rows:
        matching = next((p for p in profiles if p["file"] == row["file"] and p["sheet"] == row["sheet"]), None)
        if matching:
            row["same_structure_sheet_count"] = signatures.get(matching["signature"], 1)

    return (
        pd.DataFrame(inventory),
        pd.DataFrame(missing_rows),
        pd.DataFrame(numeric_rows),
        pd.DataFrame(categorical_rows),
        pd.DataFrame(sheet_rows),
        pd.DataFrame(time_rows),
        pd.DataFrame(duplicate_rows),
        pd.DataFrame(excluded_rows),
        profiles,
    )


def write_excel(df: pd.DataFrame, path: Path) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="summary", index=False)


def markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df.empty:
        return "No rows."
    view = df[columns].copy()
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in view.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in columns) + " |")
    return "\n".join(lines)


def write_reports(outdir: Path, inventory: pd.DataFrame, missing: pd.DataFrame, numeric: pd.DataFrame, categorical: pd.DataFrame, sheets: pd.DataFrame, time_ranges: pd.DataFrame, duplicates: pd.DataFrame, excluded: pd.DataFrame, profiles: list[dict[str, object]]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    write_excel(inventory, outdir / "tab_data_inventory.xlsx")
    write_excel(missing, outdir / "tab_missing_summary.xlsx")
    write_excel(numeric, outdir / "tab_numeric_profile.xlsx")
    write_excel(categorical, outdir / "tab_categorical_profile.xlsx")
    write_excel(sheets, outdir / "tab_sheet_coverage.xlsx")
    write_excel(time_ranges, outdir / "tab_time_range_summary.xlsx")
    write_excel(duplicates, outdir / "tab_duplicate_summary.xlsx")
    write_excel(excluded, outdir / "tab_excluded_sheets.xlsx")
    (outdir / "data_profile.json").write_text(json.dumps(profiles, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = [
        "# 数据检查报告",
        "",
        "## 数据表概览",
        "",
        markdown_table(inventory, ["file", "sheet", "rows", "columns", "time_columns", "included_status"]),
        "",
        "## 缺失值概览",
        "",
    ]
    missing_nonzero = missing[missing["missing_count"] > 0].copy() if not missing.empty else missing
    summary.append(markdown_table(missing_nonzero.head(30), ["file", "sheet", "column", "missing_count", "missing_ratio"]) if not missing_nonzero.empty else "未发现缺失值。")
    summary.extend(["", "## 异常值概览", ""])
    outlier_nonzero = numeric[numeric["iqr_outliers"] > 0].copy() if not numeric.empty else numeric
    summary.append(markdown_table(outlier_nonzero.head(30), ["file", "sheet", "column", "iqr_outliers"]) if not outlier_nonzero.empty else "数值字段未发现明显 IQR 异常值。")
    (outdir / "data_profile_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")

    draft = [
        "# 数据预处理论文段落草稿",
        "",
        f"本文首先对附件数据进行覆盖性审计，共识别 {len(inventory)} 个数据表。审计内容包括工作表名称、记录数、字段数、时间字段、数值字段、缺失比例和 IQR 异常值。所有 Excel 文件均先读取全部工作表，再根据题意判断纳入范围；对同结构工作表，后续建模应合并并保留来源文件与来源工作表字段，以保证结果可追溯。",
        "",
        "正式写入论文前，应将 `included_status` 和 `exclusion_reason` 补齐，并核对题面中的时间范围、样本范围和单位要求。",
    ]
    (outdir / "data_preprocessing_draft.md").write_text("\n".join(draft) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile CSV/XLSX files for CUMCM data audits.")
    parser.add_argument("paths", nargs="*", help="Input files or directories. Kept for backward compatibility.")
    parser.add_argument("--input", "-i", action="append", dest="inputs", help="Input file or directory. Can be repeated.")
    parser.add_argument("--output", "-o", "--outdir", dest="output", default="tables/data_profile", help="Output directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    inputs = (args.inputs or []) + args.paths
    if not inputs:
        print("No input path provided. Use --input <file-or-dir>.", file=sys.stderr)
        return 2

    files = discover_inputs(inputs)
    if not files:
        print("No CSV/XLSX files found.", file=sys.stderr)
        return 2

    inventory, missing, numeric, categorical, sheets, time_ranges, duplicates, excluded, profiles = build_outputs(files)
    outdir = Path(args.output).expanduser().resolve()
    write_reports(outdir, inventory, missing, numeric, categorical, sheets, time_ranges, duplicates, excluded, profiles)
    print(f"Profiled {len(profiles)} table(s) from {len(files)} file(s).")
    print(f"Reports written to: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
