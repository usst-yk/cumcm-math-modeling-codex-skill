# CUMCM 2025 A 题真实案例

本目录存放 2025 年高教社杯全国大学生数学建模竞赛 A 题“烟幕干扰弹的投放策略”的示例材料。

这个案例的用途不是提供标准答案，而是作为真实题面 benchmark，检查 skill 能否完成：

- 读取真实赛题 PDF；
- 提取题面文字；
- 识别 5 个子问题；
- 识别 result1/result2/result3 附件模板；
- 生成题面解析和任务计划；
- 对附件模板做数据审计；
- 用统一判据跑通 Q1-Q5；
- 生成中文图表、结果注册表、验证报告和完整论文；
- 反过来发现 skill 在真实建模题上的不足。

## 已放入的内容

| Path | 内容 |
| --- | --- |
| `problem/problem_statement.pdf` | 原始题面 PDF。 |
| `problem/problem_statement.md` | 从 PDF 提取的题面文字，便于 Codex 解析。 |
| `problem/problem_parse.json` | 规则解析得到的结构化题面结果。 |
| `problem/problem_parse.md` | 题面解析的人类可读版本。 |
| `problem/task_plan.json` | 由题面解析生成的任务计划。 |
| `problem/task_plan.md` | 任务计划的人类可读版本。 |
| `modeling/qx_modeling_idea.md` | 每问建模思路，先于代码求解。 |
| `modeling/route_comparison.md` | 三条建模路线比较和主路线选择。 |
| `data/raw/result1.xlsx` | 问题 3 的结果模板附件。 |
| `data/raw/result2.xlsx` | 问题 4 的结果模板附件。 |
| `data/raw/result3.xlsx` | 问题 5 的结果模板附件。 |
| `tables/data_profile/` | 附件模板的数据审计输出。 |
| `results/result_registry.csv` | Q1-Q5 核心数值和来源登记表。 |
| `results/validation_report.md` | Q1-Q5 验证分析记录。 |
| `results/benchmark_findings.md` | 完整 benchmark 暴露出的不足和后续优化方向。 |
| `src/make_problem_figures.py` | 题面背景和子问题范围的中文示意图脚本。 |
| `src/plot_utils.py` | 中文图表字体配置。 |
| `src/solve_q1.py` | 问题 1 的可复现几何运动求解脚本。 |
| `src/solve_q2.py` | 问题 2 的单机单弹确定性搜索脚本。 |
| `src/solve_q3_q5.py` | 问题 3-5 的固定随机种子 benchmark 求解脚本。 |
| `tables/tab_q1_key_points.csv` | 问题 1 投放点、起爆点。 |
| `tables/tab_q1_intervals.csv` | 问题 1 有效遮蔽区间和时长。 |
| `tables/tab_q2_strategy.csv` | 问题 2 推荐策略。 |
| `tables/tab_q2_intervals.csv` | 问题 2 有效遮蔽区间和时长。 |
| `tables/tab_q3_strategy.csv` | 问题 3 三弹策略。 |
| `tables/tab_q3_intervals.csv` | 问题 3 有效遮蔽区间和时长。 |
| `tables/tab_q4_strategy.csv` | 问题 4 三机策略。 |
| `tables/tab_q4_intervals.csv` | 问题 4 有效遮蔽区间和时长。 |
| `tables/tab_q5_strategy.csv` | 问题 5 多机多弹多导弹策略。 |
| `tables/tab_q5_intervals.csv` | 问题 5 各导弹有效遮蔽区间和时长。 |
| `tables/result1_benchmark.xlsx` | 问题 3 附件格式 benchmark 输出。 |
| `tables/result2_benchmark.xlsx` | 问题 4 附件格式 benchmark 输出。 |
| `tables/result3_benchmark.xlsx` | 问题 5 附件格式 benchmark 输出。 |
| `figures/fig_problem_overview_xy.png` | 题面坐标系、导弹、无人机和目标平面示意图。 |
| `figures/fig_problem_question_scope.png` | 五个子问题的资源范围和输出要求示意图。 |
| `figures/fig_q1_model_flow.png` | 问题 1 时序和遮蔽判定示意图。 |
| `figures/fig_q1_distance_geometry.png` | 问题 1 距离阈值和侧视几何图。 |
| `figures/fig_q1_validation_margin.png` | 问题 1 距离裕度和投影参数验证图。 |
| `figures/fig_q2_model_flow.png` | 问题 2 优化变量和投放时序示意图。 |
| `figures/fig_q2_optimized_distance_geometry.png` | 问题 2 距离阈值和侧视几何图。 |
| `figures/fig_q2_sensitivity.png` | 问题 2 推荐策略的局部敏感性图。 |
| `figures/fig_q3_model_flow.png` | 问题 3 三弹协同示意图。 |
| `figures/fig_q3_result.png` | 问题 3 遮蔽时间轴。 |
| `figures/fig_q3_validation.png` | 问题 3 速度和起爆高度检查图。 |
| `figures/fig_q4_model_flow.png` | 问题 4 三机协同示意图。 |
| `figures/fig_q4_result.png` | 问题 4 遮蔽时间轴。 |
| `figures/fig_q4_validation.png` | 问题 4 速度和起爆高度检查图。 |
| `figures/fig_q5_model_flow.png` | 问题 5 多机多弹协同示意图。 |
| `figures/fig_q5_result.png` | 问题 5 多导弹遮蔽时间轴。 |
| `figures/fig_q5_validation.png` | 问题 5 速度和起爆高度检查图。 |
| `results/validation_audit.md` | 产物一致性自动检查结果。 |
| `paper/main.tex` | 可编译完整 benchmark 论文；所有问题内容都在这个单文件中。 |

## 使用方式

如果要让 Codex 从这个案例开始分析，可以直接说：

```text
[$cumcm-math-modeling] 请以 examples/real_cases/cumcm_2025_a 为案例，先阅读题面解析和任务计划，再给出 2025 国赛 A 题的建模路线。
```

如果只想先做第一问，可以说：

```text
[$cumcm-math-modeling] 请只做 examples/real_cases/cumcm_2025_a 的问题 1，先建立几何运动模型，计算有效遮蔽时长，并说明结果如何写进论文。
```

如果要重新跑完整 benchmark，可以说：

```text
[$cumcm-math-modeling] 请重新运行 examples/real_cases/cumcm_2025_a 的 Q1-Q5 benchmark，更新结果注册表、验证报告和论文。
```

本案例的图默认使用中文标题、坐标轴和图例。正式做题时，只要几何关系、时间过程、优化变量、空间布局或任务拆解能用图讲清楚，就应优先生成中文示意图，再写入论文图注。已经求解的每一问至少保留“模型/题意示意图 + 核心结果图”，涉及优化、验证或敏感性分析时再补一张检查图。

## Benchmark 结果

- Q1：给定方案遮蔽时长 `1.405510 s`。
- Q2：单机单弹 best-found 遮蔽时长 `4.723893 s`。
- Q3：FY1 三弹 benchmark 遮蔽总时长 `4.740000 s`。
- Q4：FY1-FY3 各一弹遮蔽总时长 `14.520000 s`。
- Q5：M1、M2、M3 遮蔽总时长分别为 `22.980000 s`、`18.360000 s`、`6.400000 s`。

## 当前限制

- 本案例统一使用真目标轴中点代表视线判据，用于展示可复现交付链路，不作为官方标准答案。
- Q2-Q5 使用固定随机种子的 best-found 搜索方案，尚未证明全局最优。
- Q3 暴露出当前贪心求解器对“同一航向、同一速度、多弹连续投放”的联合优化能力不足。
- `problem_parse` 和 `task_plan` 是规则脚本生成的草稿，进入正式建模前仍需要人工确认几何约束、遮蔽判定和优化变量。
