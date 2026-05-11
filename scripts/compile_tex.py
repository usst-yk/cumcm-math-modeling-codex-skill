#!/usr/bin/env python3
"""Compile a TeX paper and save compile errors."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile CUMCM TeX paper.")
    parser.add_argument("--tex", default="paper/main.tex", help="TeX file.")
    parser.add_argument("--engine", default="", help="xelatex, latexmk, or tectonic. Auto-detect by default.")
    args = parser.parse_args()

    tex = Path(args.tex).expanduser().resolve()
    if not tex.exists():
        raise SystemExit(f"TeX file not found: {tex}")

    engine = args.engine
    if not engine:
        for candidate in ("latexmk", "xelatex", "tectonic"):
            if shutil.which(candidate):
                engine = candidate
                break
    if not engine:
        raise SystemExit("No TeX engine found: install latexmk/xelatex/tectonic or pass --engine.")

    if engine == "latexmk":
        cmd = [engine, "-xelatex", "-interaction=nonstopmode", tex.name]
    elif engine == "tectonic":
        cmd = [engine, tex.name]
    else:
        cmd = [engine, "-interaction=nonstopmode", tex.name]

    proc = subprocess.run(
        cmd,
        cwd=tex.parent,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if proc.returncode != 0:
        log = tex.parent / "compile_error.log"
        log.write_text((proc.stdout or "") + "\n" + (proc.stderr or ""), encoding="utf-8")
        print(f"Compile failed. Error log: {log}")
        return proc.returncode
    print(f"Compile succeeded: {tex.with_suffix('.pdf')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
