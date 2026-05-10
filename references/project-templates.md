# 项目模板与脚本

## 初始化项目

用户不需要手动运行初始化命令。默认创建精简工作区，只放必要目录，不复制一堆空模板。只有用户明确要求“完整项目模板”“全流程交付包”时，才使用完整模式。

默认精简模式：

```bash
python3 scripts/init_cumcm_project.py /path/to/project
```

完整模板模式：

```bash
python3 scripts/init_cumcm_project.py /path/to/project --full
```

生成目录：

- `problem/`: 题面原文和必要的题面解析结果。
- `data/`: 原始数据和清洗数据。
- `src/`: 数据处理、建模、求解、绘图代码。
- `figures/`: 代码生成的论文图片。
- `tables/`: 代码生成的结果表和统计表。
- `paper/`: 用户要求写论文时再放分问段落或正文。

完整模式才复制模板：

- `problem/problem_parse.schema.json`: 题面解析字段约束。
- `problem/task_plan.schema.json`: 任务计划字段约束。
- `problem/task_plan.json`: 任务计划草稿。
- `problem/model_card_template.md`: 每问模型卡模板。
- `problem/assumptions.md`: 假设和符号说明模板。
- `paper/main.md`: 论文 Markdown 骨架。
- `paper/main.tex`: TeX 论文骨架。
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

- 精简检查：先给数据问题清单和必要摘要。
- 完整审计：再输出 `data_profile_summary.md`、`data_preprocessing_draft.md`、
  `data_profile.json` 和多张审计表。需要完整审计时加 `--full`。

## 论文模板

- `assets/paper-template.md`: 自动填充优先使用。
- `assets/paper-template.docx`: 给队友继续 Word 排版时使用。
- `assets/assumptions-symbols-template.md`: 单独维护假设和符号。
- `assets/appendix-code-template.md`: 附录代码说明格式。
