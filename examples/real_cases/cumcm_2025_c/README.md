# CUMCM 2025 C 题监督-返工闭环测试

本目录是一个新的 C 题受控测试，用于证明监督-返工闭环已经沉淀到 skill，而不是依赖单次人工经验。

题目方向来自公开题名“NIPT 的时点选择与胎儿的异常判定”。本目录不包含官方附件原始数据，而是生成不含个人信息的合成数据，检查建模、验证、论文、进度面板和打包链路。

## 关键证明

- `progress.html` 展示 supervisor gate、revise、rework、recheck 事件。
- `logs/progress.jsonl` 包含 gate id、decision、owner、issue、expected fix、evidence needed。
- `figures/fig_q2_sensitivity.png` 和 `tables/tab_q2_sensitivity.csv` 是返工后补上的真实产物。
- `results/validation_audit.md` 和 `results/paper_style_audit.md` 是最终复检证据。

## 运行

```powershell
python src/solve_nipt_supervised.py
python ..\..\..\scripts\validate_results.py --project . --mode full --paper-genre contest_paper --output results\validation_audit.md
python ..\..\..\scripts\lint_paper_style.py --paper paper\main.tex --genre contest_paper --output results\paper_style_audit.md
```
