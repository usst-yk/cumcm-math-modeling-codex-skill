# Validation Report

| Subquestion | Check | Source | Result | Status | Paper consequence |
| --- | --- | --- | --- | --- | --- |
| Q1 | 投放点和起爆点复算 | `tables/tab_q1_key_points.csv` | 投放点 `(17620, 0, 1800)`，起爆点 `(17188, 0, 1736.496)` | pass | 可写入模型求解过程 |
| Q1 | 遮蔽判定 | `tables/tab_q1_intervals.csv` | 有效区间 `8.013006-9.418516 s`，时长 `1.405510 s` | pass | 可写入结果分析 |
| Q1 | 图表一致性 | `figures/fig_q1_distance_geometry.png` | 距离曲线与遮蔽半径阈值对应 | pass | 可作为问题一图 |
| Q1 | 模型边界 | `src/solve_q1.py` | 使用真目标轴中点视线判据，未声明为官方完整目标体遮蔽判据 | limited | 论文需说明判据假设 |
| Q2 | 策略可行性 | `tables/tab_q2_strategy.csv` | FY1 速度 `80.963727 m/s`，满足 `70-140 m/s`；投放时刻 `0.056749 s`，起爆时刻 `2.711605 s` | pass | 可写入推荐策略 |
| Q2 | 遮蔽判定 | `tables/tab_q2_intervals.csv` | 有效区间 `2.711605-7.435498 s`，时长 `4.723893 s` | pass | 可写入结果分析 |
| Q2 | 图表一致性 | `figures/fig_q2_optimized_distance_geometry.png` | 距离曲线与有效半径阈值对应 | pass | 可作为问题二图 |
| Q2 | 优化声明 | `src/solve_q2.py` | 使用确定性粗到细搜索得到 best-found 方案，未证明全局最优 | limited | 论文需避免绝对最优表述 |
