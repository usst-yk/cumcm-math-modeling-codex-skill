#!/usr/bin/env python3
"""Lint paper prose for contest-paper and benchmark-report genre issues."""

from __future__ import annotations

import argparse
import bisect
import re
from dataclasses import dataclass
from pathlib import Path


CONTEST_BANNED_TERMS = [
    "mini benchmark",
    "同一程序",
    "程序生成",
    "运行命令",
    "项目验证程序",
    "程序一致性",
    "结果文件",
    "文件路径",
    "代码路径",
    "随机种子",
    "代码执行准确性",
    "回归测试",
    "本测试案例",
    "本案例",
    "本项目",
    "该项目",
    "项目组",
    "项目报告",
    "本报告",
    "工作流",
    "项目流程",
    "执行流程",
    "完整流程",
    "自动化流程",
    "处理流水线",
    "pipeline",
    "workflow",
    "dashboard",
    "进度面板",
    "看板",
    "任务分工",
    "完成情况",
    "阶段性成果",
    "下一步工作",
    "交付物",
    "产出物",
    "代码跑通",
    "跑通",
    "闭环",
    "注册表闭环",
    "结果注册表",
    "测试用例",
    "案例测试",
    "单元测试",
    "验收测试",
    "自测",
    "对拍",
    "复现通过",
    "skill",
    "benchmark",
    "registry",
    "verified",
    "script",
    "脚本",
    "src/",
    "results/",
    "tables/",
    "outputs/",
    "main.tex",
    "solve_",
    ".py",
    ".json",
    ".xlsx",
    ".csv",
]

CONTEST_APPENDIX_META_TERMS = [
    "运行命令",
    "项目验证程序",
    "程序一致性",
    "同一程序",
    "程序生成",
    "结果文件",
    "文件路径",
    "代码路径",
    "\\texttt{python",
    "src/",
    ".py",
]

TEMPLATE_PHRASES = [
    "具有重要意义",
    "为相关研究提供参考",
    "本文建立模型并求解",
    "结果表明模型有效",
    "综上所述",
    "具有较好的鲁棒性",
    "具有一定的参考价值",
    "具有良好的应用前景",
    "验证了模型的有效性",
    "本文完成了",
    "本项目完成了",
    "本文围绕该问题开展工作",
    "按照流程",
    "依次完成",
    "首先进行数据处理，然后建立模型",
    "通过上述流程得到结果",
    "形成了完整方案",
    "实现了自动化求解",
    "具有较强可操作性",
    "取得了较好效果",
]

WEAK_CAPTION_PHRASES = [
    "结果图",
    "模型结果",
    "对比图",
    "流程图",
    "仿真结果",
    "示意图",
    "变化图",
]

APPENDIX_MARKER_RE = re.compile(
    r"\\appendix|\\begin\{appendices\}|\\(?:section|chapter)\*?\{[^}]*"
    r"(附录|Appendix|appendix|复现|Reproduction|reproduction)[^}]*\}"
)
DECIMAL_RE = re.compile(r"(?<![A-Za-z0-9])[-+]?\d+\.\d{5,}(?![A-Za-z0-9])")
UNIT_RE = re.compile(r"(?<![A-Za-z])(um|deg)(?![A-Za-z])", re.IGNORECASE)
CAPTION_RE = re.compile(r"\\caption(?:\[[^\]]*\])?\{(?P<body>(?:[^{}]|\{[^{}]*\})*)\}", re.DOTALL)
INPUT_RE = re.compile(r"\\(?:input|include)\{(?P<path>[^}]+)\}")
PATH_RE = re.compile(
    r"(?i)(?:^|[\s`({\[])(?:[A-Za-z]:[\\/][^\s,;)}\]]+|"
    r"(?:src|results|tables|figures|data|outputs?)[\\/][^\s,;:，。；：、)}\]]+|"
    r"[\w.-]+[\\/][\w./\\-]+\.(?:csv|py|json|xlsx?|png|pdf|tex))"
)


@dataclass(frozen=True)
class Source:
    path: Path
    text: str
    appendix: bool


@dataclass(frozen=True)
class Issue:
    severity: str
    rule: str
    path: Path
    line: int
    evidence: str
    suggestion: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint TeX paper style by genre.")
    parser.add_argument("--paper", required=True, help="Paper directory, project directory, or main .tex file.")
    parser.add_argument("--genre", required=True, choices=("contest_paper", "benchmark_report"))
    parser.add_argument("--output", help="Optional Markdown report path.")
    return parser.parse_args()


def find_paper_root(paper_arg: str) -> tuple[Path, Path]:
    target = Path(paper_arg).expanduser().resolve()
    if target.is_file():
        return target.parent, target
    if not target.exists():
        raise SystemExit(f"Paper path not found: {target}")

    candidates = [target / "main.tex", target / "paper" / "main.tex"]
    for candidate in candidates:
        if candidate.exists():
            return candidate.parent, candidate
    raise SystemExit(f"Cannot find main.tex under: {target}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def collect_sources(root: Path, main_tex: Path) -> list[Source]:
    main_text = read_text(main_tex)
    appendix_inputs = appendix_input_paths(root, main_text)
    paths = [main_tex]
    sections = root / "sections"
    if sections.exists():
        paths.extend(sorted(sections.glob("*.tex")))

    sources: list[Source] = []
    for path in paths:
        rel = path.relative_to(root)
        text = main_text if path == main_tex else read_text(path)
        lower_name = path.name.lower()
        file_is_appendix = any(token in lower_name for token in ("appendix", "repro", "supplement"))
        is_appendix = file_is_appendix or rel in appendix_inputs
        sources.append(Source(path=rel, text=text, appendix=is_appendix))
    return sources


def appendix_input_paths(root: Path, main_text: str) -> set[Path]:
    marker = APPENDIX_MARKER_RE.search(main_text)
    if not marker:
        return set()

    appendix_paths: set[Path] = set()
    for match in INPUT_RE.finditer(main_text, marker.end()):
        raw = match.group("path").strip()
        if not raw:
            continue
        candidate = Path(raw)
        if candidate.suffix != ".tex":
            candidate = candidate.with_suffix(".tex")
        try:
            resolved = (root / candidate).resolve().relative_to(root.resolve())
        except ValueError:
            continue
        appendix_paths.add(resolved)
    return appendix_paths


def line_index(text: str) -> list[int]:
    return [0] + [match.end() for match in re.finditer(r"\n", text)]


def line_at(starts: list[int], pos: int) -> int:
    return bisect.bisect_right(starts, pos)


def compact(text: str, max_len: int = 90) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) <= max_len:
        return cleaned
    return cleaned[: max_len - 3] + "..."


def is_main_body_position(source: Source, pos: int) -> bool:
    if source.appendix:
        return False
    marker = APPENDIX_MARKER_RE.search(source.text)
    return not marker or pos < marker.start()


def iter_main_body_spans(source: Source) -> list[tuple[int, int]]:
    if source.appendix:
        return []
    marker = APPENDIX_MARKER_RE.search(source.text)
    end = marker.start() if marker else len(source.text)
    return [(0, end)]


def find_contest_banned_terms(source: Source) -> list[Issue]:
    issues: list[Issue] = []
    starts = line_index(source.text)
    for begin, end in iter_main_body_spans(source):
        body = source.text[begin:end]
        lower = body.lower()
        for term in CONTEST_BANNED_TERMS:
            haystack = lower if term.isascii() else body
            needle = term.lower() if term.isascii() else term
            search_from = 0
            while True:
                found = haystack.find(needle, search_from)
                if found < 0:
                    break
                pos = begin + found
                issues.append(
                    Issue(
                        severity="P1",
                        rule="contest-main-body-ban",
                        path=source.path,
                        line=line_at(starts, pos),
                        evidence=term,
                        suggestion="Move internal workflow or artifact wording to appendix, or rewrite as paper-facing model prose.",
                    )
                )
                search_from = found + max(1, len(needle))
    return issues


def iter_appendix_spans(source: Source) -> list[tuple[int, int]]:
    if source.appendix:
        return [(0, len(source.text))]
    marker = APPENDIX_MARKER_RE.search(source.text)
    if not marker:
        return []
    return [(marker.start(), len(source.text))]


def find_contest_appendix_meta_terms(source: Source) -> list[Issue]:
    issues: list[Issue] = []
    starts = line_index(source.text)
    for begin, end in iter_appendix_spans(source):
        body = source.text[begin:end]
        lower = body.lower()
        for term in CONTEST_APPENDIX_META_TERMS:
            haystack = lower if term.isascii() else body
            needle = term.lower() if term.isascii() else term
            search_from = 0
            while True:
                found = haystack.find(needle, search_from)
                if found < 0:
                    break
                pos = begin + found
                issues.append(
                    Issue(
                        severity="P1",
                        rule="contest-appendix-meta-ban",
                        path=source.path,
                        line=line_at(starts, pos),
                        evidence=term,
                        suggestion="Use formal calculation-scope and consistency wording; keep commands, paths, and project validation details out of the submitted paper.",
                    )
                )
                search_from = found + max(1, len(needle))
    return issues


def find_path_pollution(source: Source, genre: str) -> list[Issue]:
    if genre != "contest_paper":
        return []
    issues: list[Issue] = []
    starts = line_index(source.text)
    for begin, end in iter_main_body_spans(source):
        body = source.text[begin:end]
        for match in PATH_RE.finditer(body):
            pos = begin + match.start()
            line_start = source.text.rfind("\n", 0, pos) + 1
            line_end = source.text.find("\n", pos)
            if line_end < 0:
                line_end = len(source.text)
            line_text = source.text[line_start:line_end]
            if any(command in line_text for command in ("\\includegraphics", "\\input", "\\include")):
                continue
            issues.append(
                Issue(
                    severity="P1",
                    rule="path-pollution",
                    path=source.path,
                    line=line_at(starts, pos),
                    evidence=compact(match.group(0)),
                    suggestion="Refer to the table, figure, data set, or appendix note instead of a raw path.",
                )
            )
    return issues


def find_long_decimals(source: Source) -> list[Issue]:
    issues: list[Issue] = []
    starts = line_index(source.text)
    for match in DECIMAL_RE.finditer(source.text):
        issues.append(
            Issue(
                severity="P2",
                rule="long-decimal",
                path=source.path,
                line=line_at(starts, match.start()),
                evidence=match.group(0),
                suggestion="Round to meaningful significant digits unless the problem requires this precision.",
            )
        )
    return issues


def find_unit_issues(source: Source) -> list[Issue]:
    issues: list[Issue] = []
    starts = line_index(source.text)
    for match in UNIT_RE.finditer(source.text):
        issues.append(
            Issue(
                severity="P2",
                rule="raw-unit",
                path=source.path,
                line=line_at(starts, match.start()),
                evidence=match.group(0),
                suggestion="Use paper-ready TeX or Chinese units such as \\mu m, ^\\circ, or 度.",
            )
        )
    return issues


def find_template_phrases(source: Source) -> list[Issue]:
    issues: list[Issue] = []
    starts = line_index(source.text)
    for phrase in TEMPLATE_PHRASES:
        start = 0
        while True:
            found = source.text.find(phrase, start)
            if found < 0:
                break
            issues.append(
                Issue(
                    severity="P2",
                    rule="template-prose",
                    path=source.path,
                    line=line_at(starts, found),
                    evidence=phrase,
                    suggestion="Replace template phrasing with concrete object, metric, evidence, and limitation.",
                )
            )
            start = found + len(phrase)
    return issues


def caption_is_weak(body: str) -> bool:
    plain = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", r"\1", body)
    plain = re.sub(r"\s+", "", plain)
    if len(plain) < 12:
        return True
    if plain in WEAK_CAPTION_PHRASES:
        return True
    if any(plain == phrase or plain.endswith(phrase) for phrase in WEAK_CAPTION_PHRASES):
        return True
    has_unit = bool(re.search(r"(单位|%|kg|m/s|km|cm|mm|min|h|元|度|\\mu|\\circ)", body, re.IGNORECASE))
    has_claim = bool(re.search(r"(表明|显示|说明|降低|提高|增大|减小|优于|误差|趋势|分布|变化)", body))
    return len(plain) < 24 and not (has_unit or has_claim)


def find_weak_captions(source: Source) -> list[Issue]:
    issues: list[Issue] = []
    starts = line_index(source.text)
    for match in CAPTION_RE.finditer(source.text):
        body = match.group("body")
        if caption_is_weak(body):
            issues.append(
                Issue(
                    severity="P2",
                    rule="weak-caption",
                    path=source.path,
                    line=line_at(starts, match.start()),
                    evidence=compact(body),
                    suggestion="Name the object, variable, unit or condition, and the conclusion supported by the figure.",
                )
            )
    return issues


def lint(sources: list[Source], genre: str) -> list[Issue]:
    issues: list[Issue] = []
    for source in sources:
        if genre == "contest_paper":
            issues.extend(find_contest_banned_terms(source))
            issues.extend(find_contest_appendix_meta_terms(source))
            issues.extend(find_path_pollution(source, genre))
        issues.extend(find_long_decimals(source))
        issues.extend(find_unit_issues(source))
        issues.extend(find_template_phrases(source))
        issues.extend(find_weak_captions(source))
    return sorted(issues, key=lambda item: (item.severity, str(item.path), item.line, item.rule))


def render_report(issues: list[Issue], genre: str, root: Path, main_tex: Path) -> str:
    p1_count = sum(1 for issue in issues if issue.severity == "P1")
    p2_count = sum(1 for issue in issues if issue.severity == "P2")
    status = "fail" if genre == "contest_paper" and p1_count else "pass"

    lines = [
        "# Paper Style Lint Report",
        "",
        f"- Genre: `{genre}`",
        f"- Paper root: `{root}`",
        f"- Main TeX: `{main_tex}`",
        f"- Status: `{status}`",
        f"- P1: {p1_count}",
        f"- P2: {p2_count}",
        "",
    ]
    if not issues:
        lines.append("No issues found.")
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "| Severity | Rule | Location | Evidence | Suggestion |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for issue in issues:
        evidence = issue.evidence.replace("|", "\\|")
        suggestion = issue.suggestion.replace("|", "\\|")
        lines.append(
            f"| {issue.severity} | `{issue.rule}` | `{issue.path}:{issue.line}` | "
            f"{evidence} | {suggestion} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    root, main_tex = find_paper_root(args.paper)
    sources = collect_sources(root, main_tex)
    issues = lint(sources, args.genre)
    report = render_report(issues, args.genre, root, main_tex)

    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    print(report, end="")

    has_p1 = any(issue.severity == "P1" for issue in issues)
    if args.genre == "contest_paper" and has_p1:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
