# CUMCM 2025 A 题真实案例

本目录存放 2025 年高教社杯全国大学生数学建模竞赛 A 题“烟幕干扰弹的投放策略”的示例材料。

这个案例的用途不是提供标准答案，而是作为真实题面样例，检查 skill 能否完成：

- 读取真实赛题 PDF；
- 提取题面文字；
- 识别 5 个子问题；
- 识别 result1/result2/result3 附件模板；
- 生成题面解析和任务计划；
- 对附件模板做数据审计。

## 已放入的内容

| Path | 内容 |
| --- | --- |
| `problem/problem_statement.pdf` | 原始题面 PDF。 |
| `problem/problem_statement.md` | 从 PDF 提取的题面文字，便于 Codex 解析。 |
| `problem/problem_parse.json` | 规则解析得到的结构化题面结果。 |
| `problem/problem_parse.md` | 题面解析的人类可读版本。 |
| `problem/task_plan.json` | 由题面解析生成的任务计划。 |
| `problem/task_plan.md` | 任务计划的人类可读版本。 |
| `data/raw/result1.xlsx` | 问题 3 的结果模板附件。 |
| `data/raw/result2.xlsx` | 问题 4 的结果模板附件。 |
| `data/raw/result3.xlsx` | 问题 5 的结果模板附件。 |
| `tables/data_profile/` | 附件模板的数据审计输出。 |
| `results/result_registry.csv` | 后续求解时登记关键数值的空模板。 |
| `results/validation_report.md` | 后续验证分析的记录模板。 |
| `src/make_problem_figures.py` | 题面背景和子问题范围的中文示意图脚本。 |
| `src/plot_utils.py` | 中文图表字体配置。 |
| `src/solve_q1.py` | 问题 1 的可复现几何运动求解脚本。 |
| `src/solve_q2.py` | 问题 2 的单机单弹确定性搜索脚本。 |
| `tables/tab_q1_key_points.csv` | 问题 1 投放点、起爆点。 |
| `tables/tab_q1_intervals.csv` | 问题 1 有效遮蔽区间和时长。 |
| `tables/tab_q2_strategy.csv` | 问题 2 推荐策略。 |
| `tables/tab_q2_intervals.csv` | 问题 2 有效遮蔽区间和时长。 |
| `figures/fig_problem_overview_xy.png` | 题面坐标系、导弹、无人机和目标平面示意图。 |
| `figures/fig_problem_question_scope.png` | 五个子问题的资源范围和输出要求示意图。 |
| `figures/fig_q1_model_schematic.png` | 问题 1 时序和遮蔽判定示意图。 |
| `figures/fig_q1_distance_geometry.png` | 问题 1 距离阈值和侧视几何图。 |
| `figures/fig_q2_model_schematic.png` | 问题 2 优化变量和投放时序示意图。 |
| `figures/fig_q2_optimized_distance_geometry.png` | 问题 2 距离阈值和侧视几何图。 |
| `results/validation_audit.md` | 问题 1 产物一致性自动检查结果。 |
| `paper/main.tex` | 可编译论文片段入口。 |
| `paper/sections/problem_overview.tex` | 题面结构与几何背景论文片段。 |
| `paper/sections/q1.tex` | 问题 1 论文片段。 |
| `paper/sections/q2.tex` | 问题 2 论文片段。 |

## 使用方式

如果要让 Codex 从这个案例开始分析，可以直接说：

```text
[$cumcm-math-modeling] 请以 examples/real_cases/cumcm_2025_a 为案例，先阅读题面解析和任务计划，再给出 2025 国赛 A 题的建模路线。
```

如果只想先做第一问，可以说：

```text
[$cumcm-math-modeling] 请只做 examples/real_cases/cumcm_2025_a 的问题 1，先建立几何运动模型，计算有效遮蔽时长，并说明结果如何写进论文。
```

如果要继续完整求解，建议按子问题推进：当前已完成 Q1 的几何遮蔽计算和 Q2 的单机单弹搜索示例，随后可扩展到 Q3、Q4、Q5 的多弹、多机、多导弹联合优化。

本案例的图默认使用中文标题、坐标轴和图例。正式做题时，只要几何关系、时间过程、优化变量、空间布局或任务拆解能用图讲清楚，就应优先生成中文示意图，再写入论文图注。

## 当前限制

- 本目录目前完成了问题 1 和问题 2 的示例闭环。
- 问题 3-5 尚未包含正式求解代码、最终图表或完整论文。
- 问题 1 和问题 2 使用真目标轴中点视线判据，用于展示可复现交付链路，不作为官方标准答案。
- 问题 2 使用确定性粗到细搜索得到 best-found 方案，尚未证明全局最优。
- `problem_parse` 和 `task_plan` 是规则脚本生成的草稿，进入正式建模前仍需要人工确认几何约束、遮蔽判定和优化变量。
