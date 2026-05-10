# Validation Report

本案例采用统一的“真目标轴中点代表视线判据”：
烟幕云团中心到“导弹-真目标轴中点”线段的距离不超过 10 m，且垂足在线段内部时，记为有效遮蔽。
该判据用于构造可复现 benchmark，不等同于官方完整圆柱目标遮蔽判据。

| Subquestion | Check | Source | Result | Status | Paper consequence |
| --- | --- | --- | --- | --- | --- |
| 全局 | 题面几何示意 | `figures/fig_problem_overview_xy.png` | 导弹、无人机、假目标和真目标位置已用中文图示说明 | pass | 可放在问题分析部分 |
| 全局 | 子问题范围示意 | `figures/fig_problem_question_scope.png` | Q1-Q5 的无人机、烟幕弹、导弹和输出要求已用中文图示说明 | pass | 可放在问题分析部分 |
| Q1 | 模型示意图 | `figures/fig_q1_model_schematic.png` | 投放、起爆、遮蔽开始和遮蔽结束时序已用中文图示说明 | pass | 可作为问题一模型图 |
| Q1 | 投放点和起爆点复算 | `tables/tab_q1_key_points.csv` | 投放点 `(17620, 0, 1800)`，起爆点 `(17188, 0, 1736.496)` | pass | 可写入模型求解过程 |
| Q1 | 遮蔽判定 | `tables/tab_q1_intervals.csv` | 有效区间 `8.013006-9.418516 s`，时长 `1.405510 s` | pass | 可写入结果分析 |
| Q1 | 判据验证图 | `figures/fig_q1_validation_margin.png` | 距离裕度和投影参数同时支持有效区间判定 | pass | 可作为问题一验证图 |
| Q2 | 策略可行性 | `tables/tab_q2_strategy.csv` | FY1 速度 `80.963727 m/s`，满足 `70-140 m/s`；投放和起爆时序可行 | pass | 可写入推荐策略 |
| Q2 | 遮蔽判定 | `tables/tab_q2_intervals.csv` | 有效区间 `2.711605-7.435498 s`，时长 `4.723893 s` | pass | 可写入结果分析 |
| Q2 | 敏感性图 | `figures/fig_q2_sensitivity.png` | 速度、航向角、投放时刻和引信延迟的局部扰动均可复算 | pass | 可作为问题二敏感性分析图 |
| Q2 | 优化声明 | `src/solve_q2.py` | 使用确定性粗到细搜索得到 best-found 方案，未证明全局最优 | limited | 论文需避免绝对最优表述 |
| Q3 | 三弹策略可行性 | `tables/tab_q3_strategy.csv` | FY1 速度 `75.415887 m/s`，同航向投放 3 枚，投放间隔均不小于 `1 s` | pass | 可写入问题三策略表 |
| Q3 | 遮蔽判定 | `tables/tab_q3_intervals.csv` | M1 有效遮蔽总时长 `4.740000 s` | limited | 论文需说明第 2、3 枚在当前判据和搜索策略下边际贡献不足 |
| Q3 | benchmark 暴露问题 | `results/benchmark_findings.md` | 贪心边际覆盖没有真正解决同航向多弹联合优化 | limited | 后续 skill 应强化多弹联合搜索或分段协同建模 |
| Q4 | 三机策略可行性 | `tables/tab_q4_strategy.csv` | FY1、FY2、FY3 各 1 枚，速度范围、起爆高度均可行 | pass | 可写入问题四策略表 |
| Q4 | 遮蔽判定 | `tables/tab_q4_intervals.csv` | M1 有效遮蔽总时长 `14.520000 s`，由三段遮蔽区间组成 | pass | 可写入问题四结果分析 |
| Q5 | 多机多弹约束 | `tables/tab_q5_strategy.csv` | 每架无人机至多 3 枚，同机投放间隔不小于 `1 s`，起爆高度为正 | pass | 可写入问题五策略表 |
| Q5 | 多导弹遮蔽结果 | `tables/tab_q5_intervals.csv` | M1 `22.980000 s`，M2 `18.360000 s`，M3 `6.400000 s` | pass | 可写入问题五结果分析 |
| Q5 | 结果模板 | `tables/result3_benchmark.xlsx` | 已按附件模板输出导弹编号和单弹有效干扰时长 | pass | 可作为 benchmark 输出附件 |

## Remaining limits

- 当前 benchmark 使用代表视线点，尚未检查圆柱目标完整外轮廓的全部可见性。
- Q2-Q5 均为固定随机种子的 best-found 策略，不声明全局最优。
- Q3 暴露出当前求解器对“同一航向、同一速度、连续投放多弹”的联合优化能力不足。
- Q5 使用贪心边际覆盖，能给出可复现方案，但不保证最优资源分配。
