#!/usr/bin/env python3
"""Check basic Codex skill structure and local documentation links."""

from __future__ import annotations

import re
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH_RE = re.compile(
    r"(?<![\w/.-])((?:agents|references|scripts|templates|examples|evals|\.github)/[A-Za-z0-9_./*-]+)"
)


def check_front_matter(issues: list[str]) -> None:
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        issues.append("SKILL.md front matter must start with --- on its own line")
        return
    try:
        _, front, _ = text.split("---", 2)
    except ValueError:
        issues.append("SKILL.md front matter must have an opening and closing ---")
        return
    if not re.search(r"^name:\s*\S+", front, flags=re.MULTILINE):
        issues.append("SKILL.md front matter missing name")
    if not re.search(r"^description:\s*(?:\||>|\S+)", front, flags=re.MULTILINE):
        issues.append("SKILL.md front matter missing description")
    if "\t" in front:
        issues.append("SKILL.md front matter should not contain tab indentation")


def check_referenced_paths(issues: list[str]) -> None:
    docs = [ROOT / "SKILL.md", ROOT / "README.md"]
    docs.extend((ROOT / "references").glob("*.md"))
    docs.extend((ROOT / "agents").glob("*.md"))
    for doc in docs:
        text = doc.read_text(encoding="utf-8", errors="ignore")
        for raw in PATH_RE.findall(text):
            if "*" in raw:
                continue
            rel = raw.rstrip(".,;:，。；：)")
            if not (ROOT / rel).exists():
                issues.append(f"{doc.relative_to(ROOT)} references missing path: {rel}")


def check_required_entrypoints(issues: list[str]) -> None:
    required = [
        "SKILL.md",
        "README.md",
        "agents/problem_parser.md",
        "agents/coordinator.md",
        "agents/coder.md",
        "agents/abstract_writer.md",
        "references/task-routing.md",
        "references/output-policy.md",
        "references/figure-plan.md",
        "references/official-benchmark.md",
        "references/first-prize-rubric.md",
        "scripts/problem_parser.py",
        "scripts/build_task_plan.py",
        "scripts/data_profile.py",
        "scripts/validate_results.py",
        "scripts/build_official_case_index.py",
        "scripts/run_skill_evals.py",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            issues.append(f"missing required entrypoint: {rel}")


def check_task_plan_fields(issues: list[str]) -> None:
    schema_path = ROOT / "templates" / "task_plan.schema.json"
    template_path = ROOT / "templates" / "task_plan.json"
    required_fields = {"benchmark_sources", "rubric_targets", "selling_points", "revision_status"}
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        template = json.loads(template_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"task plan template/schema could not be read: {exc}")
        return

    top_props = set(schema.get("properties", {}))
    missing_top = {"benchmark_sources", "rubric_targets", "revision_status"} - top_props
    if missing_top:
        issues.append(f"task_plan.schema.json missing top-level fields: {', '.join(sorted(missing_top))}")

    sub_props = set(
        schema.get("properties", {})
        .get("subquestions", {})
        .get("items", {})
        .get("properties", {})
    )
    missing_sub = required_fields - sub_props
    if missing_sub:
        issues.append(f"task_plan.schema.json missing subquestion fields: {', '.join(sorted(missing_sub))}")

    missing_template_top = {"benchmark_sources", "rubric_targets", "revision_status"} - set(template)
    if missing_template_top:
        issues.append(f"task_plan.json missing top-level fields: {', '.join(sorted(missing_template_top))}")

    for idx, subquestion in enumerate(template.get("subquestions", []), start=1):
        missing = required_fields - set(subquestion)
        if missing:
            issues.append(f"task_plan.json subquestion {idx} missing fields: {', '.join(sorted(missing))}")


def check_project_dirs(issues: list[str]) -> None:
    script = ROOT / "scripts" / "init_cumcm_project.py"
    text = script.read_text(encoding="utf-8")
    forbidden = ['"logs"', '"appendix"', '"presentation"', '"notebooks"', '"figures/ai_briefs"', "progress.html"]
    for item in forbidden:
        if item in text:
            issues.append(f"init_cumcm_project.py should not create {item.strip(chr(34))}")


def main() -> int:
    issues: list[str] = []
    check_front_matter(issues)
    check_referenced_paths(issues)
    check_required_entrypoints(issues)
    check_task_plan_fields(issues)
    check_project_dirs(issues)
    if issues:
        print("Skill structure checks failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Skill structure checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
