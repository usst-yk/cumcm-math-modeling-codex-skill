#!/usr/bin/env python3
"""Validate and summarize official CUMCM benchmark source metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "evals" / "official_cases" / "official_case_index.json"


REQUIRED_TYPES = {"portal", "review_index", "paper_showcase", "expert_talk", "problem_review"}
REQUIRED_FIELDS = {"id", "type", "title", "url", "use"}


def validate_index(data: dict) -> list[str]:
    issues: list[str] = []
    sources = data.get("sources", [])
    if not isinstance(sources, list) or not sources:
        return ["official case index must contain a non-empty sources list"]

    seen_ids: set[str] = set()
    source_types: set[str] = set()
    a_years: set[int] = set()

    for idx, item in enumerate(sources, start=1):
        label = item.get("id", f"source_{idx}")
        missing = sorted(REQUIRED_FIELDS - set(item))
        if missing:
            issues.append(f"{label} missing fields: {', '.join(missing)}")
        source_id = str(item.get("id", ""))
        if source_id in seen_ids:
            issues.append(f"duplicate source id: {source_id}")
        seen_ids.add(source_id)

        source_type = str(item.get("type", ""))
        source_types.add(source_type)
        if source_type not in REQUIRED_TYPES:
            issues.append(f"{label} has unknown type: {source_type}")

        parsed = urlparse(str(item.get("url", "")))
        if parsed.scheme != "https" or parsed.netloc != "dxs.moe.gov.cn":
            issues.append(f"{label} should use an official dxs.moe.gov.cn https URL")

        if source_type == "problem_review" and item.get("problem") == "A":
            year = item.get("problem_year")
            if isinstance(year, int):
                a_years.add(year)

    missing_types = sorted(REQUIRED_TYPES - source_types)
    if missing_types:
        issues.append(f"official case index missing source types: {', '.join(missing_types)}")

    required_a_years = {2020, 2022, 2023, 2024, 2025}
    missing_a_years = sorted(required_a_years - a_years)
    if missing_a_years:
        issues.append(f"official case index missing A-problem review years: {missing_a_years}")

    return issues


def write_markdown(data: dict, output: Path) -> None:
    lines = [
        "# Official Case Index",
        "",
        "This generated summary lists official benchmark sources only. It does not",
        "copy official paper content.",
        "",
        "| ID | Type | Title | Use |",
        "| --- | --- | --- | --- |",
    ]
    for item in data.get("sources", []):
        lines.append(
            "| {id} | {type} | [{title}]({url}) | {use} |".format(
                id=item.get("id", ""),
                type=item.get("type", ""),
                title=item.get("title", ""),
                url=item.get("url", ""),
                use=item.get("use", ""),
            )
        )
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate official CUMCM benchmark metadata.")
    parser.add_argument("--index", default=str(DEFAULT_INDEX), help="official_case_index.json path")
    parser.add_argument("--write-md", help="markdown summary output path")
    args = parser.parse_args()

    index_path = Path(args.index).expanduser().resolve()
    data = json.loads(index_path.read_text(encoding="utf-8"))
    issues = validate_index(data)
    if issues:
        print("Official case index checks failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    if args.write_md:
        write_markdown(data, Path(args.write_md).expanduser().resolve())
    print("Official case index checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
