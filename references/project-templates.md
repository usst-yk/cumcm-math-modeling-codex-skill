# 项目模板与脚本

## 初始化项目

用户不需要手动运行初始化命令。优先让 Codex 根据用户的项目名调用脚本，创建标准工作区，然后继续后续建模任务。

后台命令：

```bash
python3 scripts/init_cumcm_project.py /path/to/project
```

生成目录：

- `data/`: 原始数据和清洗数据。
- `src/`: 数据处理、建模、求解、绘图代码。
- `figures/`: 代码生成的论文图片。
- `tables/`: 代码生成的结果表和统计表。
- `paper/`: 论文正文、假设符号表、数据预处理草稿。
- `appendix/`: 附录代码和补充材料。

复制模板：

- `paper/main.md`: 论文 Markdown 骨架。
- `paper/assumptions-symbols.md`: 假设和符号说明模板。
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

- `data_profile_summary.md`: 字段、缺失值、异常值、统计量和相关性说明。
- `data_preprocessing_draft.md`: 可放入论文的数据预处理段落草稿。
- `data_profile.json`: 结构化检查结果。
- `*_correlation.csv`: 数值字段相关系数矩阵。

## 论文模板

- `assets/paper-template.md`: 自动填充优先使用。
- `assets/paper-template.docx`: 给队友继续 Word 排版时使用。
- `assets/assumptions-symbols-template.md`: 单独维护假设和符号。
- `assets/appendix-code-template.md`: 附录代码说明格式。
