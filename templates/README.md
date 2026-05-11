# Templates

默认项目只创建固定输出目录，不批量复制模板。需要某个模板时，只把内容写入
默认目录中的对应文件；不要创建额外日志、附录、展示或 notebook 目录。

| Template | Copied to | Purpose |
| --- | --- | --- |
| `problem_parse.schema.json` | `problem/problem_parse.schema.json` | 题面解析字段约束。 |
| `task_plan.json` | `problem/task_plan.json` | 结构化题目拆解，含 benchmark 来源、评分目标、卖点和修订状态占位。 |
| `task_plan.schema.json` | `problem/task_plan.schema.json` | 任务计划字段约束，覆盖 benchmark、rubric、selling point 和 revision 字段。 |
| `method_card.schema.json` | 默认不复制 | 结构化方法卡字段约束。 |
| `model_card.md` | `problem/model_card_template.md` | 每问模型卡。 |
| `modeling_idea.md` | `modeling/modeling_idea_template.md` | 每问详细建模思路模板，包含逐步推导、求解步骤、GPT-image 流程图计划和论文写法，先于代码求解。 |
| `assumptions_symbols.md` | `problem/assumptions.md` | 假设和符号说明模板。 |
| `result_registry.csv` | `results/result_registry.csv` | 关键数值来源追踪。 |
| `validation_report.md` | `results/validation_report.md` | 验证结果记录。 |
| `paper_main.tex` | `paper/main.tex` | 轻量国赛 TeX 论文骨架；单问和全题都只用这一个文件，不拆 `paper/sections/`。 |
| `refs.bib` | `paper/refs.bib` | 参考文献占位，含常见数学建模参考书示例。 |
| `appendix_code.md` | `paper/main.tex` 的复现说明部分 | 附录代码说明格式。 |
| `run_log.md` | `results/validation_report.md` 或 `paper/main.tex` 复现说明 | 运行记录。 |
| `ai_usage_statement.md` | `paper/main.tex` 的 AI 使用说明部分 | AI 辅助使用、人工核验和可复现声明。 |
| `ai_figure_brief.md` | `modeling/ai_figure_brief_template.md` | AI 示意图 brief 模板。 |

不创建 `appendix/`、`logs/`、`presentation/`、`notebooks/` 或
`figures/ai_briefs/`。

TeX 模板吸收了常见 CUMCM 模板的章节顺序。论文图表字体由
`assets/fonts/` 和 `scripts/make_paper_figures.py` 统一管理，避免新手因为
macOS/Windows 字体差异导致图中文字变形。

命名约定：模板名与目标产物保持一致。
