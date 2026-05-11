# CUMCM 2025 C 题监督-返工闭环测试

本目录是一个 C 题受控测试，用于证明建模、验证和论文写作链路已经沉淀到 skill，而不是依赖单次人工经验。

题目方向来自公开题名“NIPT 的时点选择与胎儿的异常判定”。本目录不包含官方附件原始数据，而是生成不含个人信息的合成数据，检查建模、验证和论文链路。

## 关键证明

- `figures/fig_q2_sensitivity.png` 和 `tables/tab_q2_sensitivity.csv` 是返工后补上的真实产物。
- `results/validation_audit.md` 和 `results/paper_style_audit.md` 是最终复检证据。
- 本示例只保留默认输出目录，不包含 `logs/`、`appendix/`、进度面板或打包目录。

## 运行

```powershell
python src/solve_nipt_supervised.py
python ..\..\..\scripts\validate_results.py --project . --mode full --paper-genre contest_paper --output results\validation_audit.md
python ..\..\..\scripts\lint_paper_style.py --paper paper\main.tex --genre contest_paper --output results\paper_style_audit.md
```
