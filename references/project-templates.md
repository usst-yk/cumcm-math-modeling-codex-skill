# Project Template

项目目录保持简单：

- `problem/`: 题面、题面解析和任务拆解。
- `data/`: 原始数据、清洗后数据和重建 benchmark 数据。
- `modeling/`: 每问详细建模思路、代码建模流程、GPT-image 流程图提示和技术路线图提示。
- `src/`: 可复现求解脚本。
- `tables/`: 数据审计表、结果表和验证表。
- `figures/`: GPT-image 流程图、技术路线图、结果图和验证图。
- `results/`: 验证报告、复核说明和最终检查报告。
- `paper/`: 唯一论文入口 `paper/main.tex`。

创建项目：

```bash
python3 scripts/init_cumcm_project.py /path/to/project
```

求解、论文写作、结果解释、以及影响论文结论的验证和图表工作最后都要回写到
`paper/main.tex`。单纯规划、路线比较或候选模型讨论可以先留在 `problem/`
或 `modeling/`，但要说明后续写入论文的位置。
