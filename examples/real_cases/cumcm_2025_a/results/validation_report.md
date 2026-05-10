# Validation Report

| Subquestion | Check | Source | Result | Status | Paper consequence |
| --- | --- | --- | --- | --- | --- |
| Q1 | 投放点和起爆点复算 | `tables/tab_q1_key_points.csv` | 投放点 `(17620, 0, 1800)`，起爆点 `(17188, 0, 1736.496)` | pass | 可写入模型求解过程 |
| Q1 | 遮蔽判定 | `tables/tab_q1_intervals.csv` | 有效区间 `8.013006-9.418516 s`，时长 `1.405510 s` | pass | 可写入结果分析 |
| Q1 | 图表一致性 | `figures/fig_q1_distance_geometry.png` | 距离曲线与遮蔽半径阈值对应 | pass | 可作为问题一图 |
| Q1 | 模型边界 | `src/solve_q1.py` | 使用真目标轴中点视线判据，未声明为官方完整目标体遮蔽判据 | limited | 论文需说明判据假设 |
