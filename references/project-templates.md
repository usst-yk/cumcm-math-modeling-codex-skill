# 项目模板与脚本

## 初始化项目

用户不需要手动运行初始化命令。默认创建论文优先工作区，包含必要目录、
`paper/main.tex` 和 `results/result_registry.csv`。只有用户明确要求
“完整项目模板”“全流程交付包”时，才复制所有辅助模板和日志。
论文优先不允许削弱建模、求解、验证或论文写作。

默认论文优先模式：

```bash
python3 scripts/init_cumcm_project.py /path/to/project
```

完整模板模式：

```bash
python3 scripts/init_cumcm_project.py /path/to/project --full
```

生成目录：

- `problem/`: 题面原文和必要的题面解析结果。
- `modeling/`: 每问详细建模思路、路线比较、GPT-image 流程图提示和代码反向验证。
- `data/`: 原始数据、清洗数据和预处理产物；不要使用 `date/` 目录。
- `src/`: 数据处理、建模、求解、绘图代码。
- `figures/`: 代码生成的论文图片。
- `tables/`: 代码生成的结果表和统计表。
- `paper/`: 默认包含 `main.tex`；不再创建分问片段目录。
- `results/`: 默认包含结果注册表，用于追踪写入论文的关键数字。

完整模式才复制模板：

- `problem/problem_parse.schema.json`: 题面解析字段约束。
- `problem/task_plan.schema.json`: 任务计划字段约束。
- `problem/task_plan.json`: 任务计划草稿。
- `problem/model_card_template.md`: 每问模型卡模板。
- `modeling/modeling_idea_template.md`: 每问建模思路模板。
- `problem/assumptions.md`: 假设和符号说明模板。
- `paper/main.tex`: TeX 论文骨架。最终论文、benchmark 和完整报告都使用
  TeX，Markdown 只用于说明文档或草稿笔记。
- `appendix/code-template.md`: 附录代码格式模板。

## 数据检查

运行：

```bash
python3 scripts/data_profile.py /path/to/data --outdir /path/to/project/tables/data_profile
```

支持：

- CSV。
- XLSX/XLS 多 sheet。
- 数据目录批量扫描。

输出：

- 标准数据检查：先给数据问题清单和必要摘要；字段解释、缺失异常、
  单位风险和排除原因不能省略，并把会影响建模的结论写入 `paper/main.tex`。
- 完整审计：再输出 `data_profile_summary.md`、`data_preprocessing_draft.md`、
  `data_profile.json` 和多张审计表。需要完整审计时加 `--full`。

## 论文模板

- `templates/paper_main.tex`: TeX 论文骨架。
- `templates/assumptions_symbols.md`: 单独维护假设和符号。
- `templates/appendix_code.md`: 附录代码说明格式。
