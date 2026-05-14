# Output Policy

每次建模输出都围绕论文推进。必须创建或更新 `paper/main.tex`。

标准目录只有这些：

- `problem/`
- `data/`
- `modeling/`
- `src/`
- `tables/`
- `figures/`
- `results/`
- `paper/`

## 文件职责

- `problem/`: 题面、题面解析、任务计划。
- `data/`: 原始数据、清洗数据、重建数据。
- `modeling/`: 每问详细建模思路、代码建模流程、路线比较、GPT-image 流程图提示。
- `src/`: 求解、绘图、验证脚本。
- `tables/`: 数据审计表、结果表、验证表。
- `figures/`: GPT-image 流程图、技术路线图、结果图、验证图。
- `results/`: 验证报告、最终复核说明。
- `paper/`: 唯一论文入口 `paper/main.tex`。

## 必须回写论文

完成任何一问后，把以下内容写回 `paper/main.tex`：

- 问题分析；
- 变量、假设、公式、约束；
- 求解算法、代码建模流程和代码反向验证；
- 结果表和结果图；
- 验证、敏感性分析或边界检查；
- 结论和复现说明。

关键数字必须能追溯到保存的表格、图片、代码输出、题面事实或
`results/validation_report.md`。
