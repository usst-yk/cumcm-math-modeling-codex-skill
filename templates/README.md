# Templates

这些模板只在用户明确要求完整项目或使用 `init_cumcm_project.py --full`
时复制到项目目录中。默认文件精简求解不会批量复制模板；这只影响模板
文件数量，不影响建模、求解、验证或论文写作深度。

| Template | Copied to | Purpose |
| --- | --- | --- |
| `problem_parse.schema.json` | `problem/problem_parse.schema.json` | 题面解析字段约束。 |
| `task_plan.json` | `problem/task_plan.json` | 结构化题目拆解。 |
| `task_plan.schema.json` | `problem/task_plan.schema.json` | 任务计划字段约束。 |
| `method_card.schema.json` | 默认不复制 | 结构化方法卡字段约束。 |
| `model_card.md` | `problem/model_card_template.md` | 每问模型卡。 |
| `modeling_idea.md` | `modeling/modeling_idea_template.md` | 每问建模思路模板，先于代码求解。 |
| `assumptions_symbols.md` | `problem/assumptions.md` | 假设和符号说明模板。 |
| `result_registry.csv` | `results/result_registry.csv` | 关键数值来源追踪。 |
| `validation_report.md` | `results/validation_report.md` | 验证结果记录。 |
| `paper_main.tex` | `paper/main.tex` | 轻量国赛 TeX 论文骨架；单问和全题都只用这一个文件，不拆 `paper/sections/`。 |
| `refs.bib` | `paper/refs.bib` | 参考文献占位，含常见数学建模参考书示例。 |
| `appendix_code.md` | `appendix/code-template.md` | 附录代码说明格式。 |
| `run_log.md` | `logs/run_log.md` | 运行记录。 |

TeX 模板吸收了常见 CUMCM 模板的章节顺序，但不依赖额外 class、字体文件或编译产物，避免新手因为缺字体而编译失败。

命名约定：模板名与目标产物保持一致。
