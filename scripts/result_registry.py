#!/usr/bin/env python3
"""Create or append a CUMCM result registry."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


COLUMNS = [
    "subquestion",
    "conclusion",
    "value",
    "unit",
    "source_type",
    "source_path",
    "source_location",
    "reproduce_command",
    "validation_check",
    "paper_locations",
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
    parser.add_argument("--subquestion", default="", help="Question id, e.g. Q1.")
    parser.add_argument("--conclusion", default="", help="Headline conclusion.")
    parser.add_argument("--value", default="", help="Numeric/text value.")
    parser.add_argument("--unit", default="", help="Unit.")
    parser.add_argument("--source-type", default="", help="data, code, table, figure, equation, assumption.")
    parser.add_argument("--source-path", default="", help="Source file path.")
    parser.add_argument("--source-location", default="", help="Sheet/cell/row/figure/equation/log line.")
    parser.add_argument("--reproduce-command", default="", help="Command used to reproduce the value.")
    parser.add_argument("--validation-check", default="", help="Baseline, error, feasibility, sensitivity, etc.")
    parser.add_argument("--paper-locations", default="", help="Abstract/body/table/figure/caption locations.")
    parser.add_argument("--status", default="draft", help="draft, verified, blocked.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.registry).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    df = load_registry(path)

    if any(getattr(args, field.replace("-", "_"), "") for field in ["subquestion", "conclusion", "value", "source-type", "source-path"]):
        row = {
            "subquestion": args.subquestion,
            "conclusion": args.conclusion,
            "value": args.value,
            "unit": args.unit,
            "source_type": args.source_type,
            "source_path": args.source_path,
            "source_location": args.source_location,
            "reproduce_command": args.reproduce_command,
            "validation_check": args.validation_check,
            "paper_locations": args.paper_locations,
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
