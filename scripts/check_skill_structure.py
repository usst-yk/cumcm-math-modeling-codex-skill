#!/usr/bin/env python3
"""Check basic Codex skill structure and local documentation links."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH_RE = re.compile(
    r"(?<![\w/.-])((?:agents|assets|references|scripts|templates|examples|evals|\.github)/[A-Za-z0-9_./*-]+)"
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
        "references/task-routing.md",
        "references/output-policy.md",
        "references/figure-plan.md",
        "scripts/problem_parser.py",
        "scripts/build_task_plan.py",
        "scripts/data_profile.py",
        "scripts/validate_results.py",
        "scripts/run_skill_evals.py",
    ]
    for rel in required:
        if not (ROOT / rel).exists():
            issues.append(f"missing required entrypoint: {rel}")


def main() -> int:
    issues: list[str] = []
    check_front_matter(issues)
    check_referenced_paths(issues)
    check_required_entrypoints(issues)
    if issues:
        print("Skill structure checks failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Skill structure checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
