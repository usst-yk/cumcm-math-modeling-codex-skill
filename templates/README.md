# Templates

这里放的是 skill 复用的基础模板。新手只需要知道：项目最终会回到
`paper/main.tex`，表格放 `tables/`，图片放 `figures/`，验证说明放
`results/validation_report.md`。

| Template | Purpose |
| --- | --- |
| `paper_main.tex` | 国赛论文主文件骨架。 |
| `validation_report.md` | 验证、敏感性分析和失败说明记录。 |
| `modeling_idea.md` | 每问详细建模思路模板。 |
| `task_plan.json` | 题目拆解模板。 |
| `problem_parse.schema.json` | 题面解析字段约束。 |
| `task_plan.schema.json` | 任务计划字段约束。 |
| `method_card.schema.json` | 方法卡字段约束。 |
| `model_card.md` | 每问模型卡。 |
| `assumptions_symbols.md` | 假设和符号说明模板。 |
| `refs.bib` | 参考文献占位。 |

论文图表字体由 `assets/fonts/` 和 `scripts/make_paper_figures.py` 统一管理，
中文使用内置 Noto Sans CJK SC，英文和数字优先使用 Times New Roman 风格。
