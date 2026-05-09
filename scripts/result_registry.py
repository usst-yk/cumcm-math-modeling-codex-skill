#!/usr/bin/env python3
"""Create or append a CUMCM result registry."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


COLUMNS = [
    "id",
    "subquestion",
    "claim",
    "value",
    "unit",
    "source_file",
    "source_line_or_cell",
    "script",
    "command",
    "figure_or_table",
    "validation",
    "status",
]


def load_registry(path: Path) -> pd.DataFrame:
    if path.exists():
        if path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(path)
        else:
            df = pd.read_csv(path)
        for col in COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or append a result registry for CUMCM papers.")
    parser.add_argument("--registry", default="tables/result_registry.xlsx", help="Registry path.")
    parser.add_argument("--id", default="", help="Result id, e.g. R001.")
    parser.add_argument("--subquestion", default="", help="Question id, e.g. Q1.")
    parser.add_argument("--claim", "--conclusion", default="", help="Headline claim or conclusion.")
    parser.add_argument("--value", default="", help="Numeric/text value.")
    parser.add_argument("--unit", default="", help="Unit.")
    parser.add_argument("--source-file", "--source-path", default="", help="Source file path.")
    parser.add_argument("--source-line-or-cell", "--source-location", default="", help="Sheet/cell/row/figure/equation/log line.")
    parser.add_argument("--script", default="", help="Script that produced the value.")
    parser.add_argument("--command", "--reproduce-command", default="", help="Command used to reproduce the value.")
    parser.add_argument("--figure-or-table", default="", help="Linked figure or table filename.")
    parser.add_argument("--validation", "--validation-check", default="", help="Baseline, error, feasibility, sensitivity, etc.")
    parser.add_argument("--status", default="draft", help="draft, verified, blocked.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.registry).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    df = load_registry(path)

    if any([args.subquestion, args.claim, args.value, args.source_file, args.figure_or_table]):
        row = {
            "id": args.id or f"R{len(df) + 1:03d}",
            "subquestion": args.subquestion,
            "claim": args.claim,
            "value": args.value,
            "unit": args.unit,
            "source_file": args.source_file,
            "source_line_or_cell": args.source_line_or_cell,
            "script": args.script,
            "command": args.command,
            "figure_or_table": args.figure_or_table,
            "validation": args.validation,
            "status": args.status,
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    if path.suffix.lower() in {".xlsx", ".xls"}:
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="registry", index=False)
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")

    print(f"Result registry written to: {path}")
    print(f"Rows: {len(df)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
