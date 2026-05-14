# Single Question Minimal Demo

这个目录展示“只做某一问”时最小、清楚的输出形态。

它不是完整比赛项目，不包含空模板或日志。对新手来说，只做一问通常保留这些文件就够了：

```text
problem.md
modeling/q1_modeling_idea.md
modeling/q1_model_flow_prompt.md
src/solve_q1.py
tables/tab_q1_result.csv
figures/fig_q1_model_flow.png
figures/fig_q1_result.png
results/validation_report.md
paper/main.tex
```

如果这一问是优化、预测、评价、调度或仿真，还应再补一张验证、敏感性或约束检查图。

单问论文也使用 TeX：`paper/main.tex`。Markdown 只用于 README 说明，
不作为论文成品。

新手可以只说“帮我求解第一问”，但最终不能只交代码或结果图。单问也要有
建模推导、代码建模流程、结果来源、验证说明和可放进论文的正文。
