# Task Plan

- Contest: CUMCM
- Problem: huadong_cup_a
- Question count: 2

| ID | Type | Input | Model object | Output | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 | optimization | problem/problem_statement.md; data/benchmark_activities.csv | 有限开放时段内的项目访问顺序和休整/演出安排 | 三类游客在工作日、双休日、节假日的游览路线; 体验得分、项目数、排队时间、候场时间、步行时间和结束时间; 与贪心基线的对比 | feasibility check; time-window check; baseline scheme comparison | solved |
| Q2 | optimization | tables/tab_q1_routes.csv; data/realtime_wait_updates.csv; data/benchmark_activities.csv | 实时排队信息到达后未完成项目的访问顺序 | 实时排队更新后的剩余路线调整结果; 保持原剩余路线与重规划路线的等待时间和得分差异; 新增和删除项目清单 | baseline comparison with unchanged remaining route; feasibility check; queue-time sensitivity | solved |

## Global assumptions
- 本案例没有官方排队附件，项目数据和实时扰动为透明 benchmark 数据。
- 开放时段统一设为 09:00-21:00。
- 体验得分用于模型比较，不代表真实满意度。

## Risk points
- 不能把 benchmark 数据说成官方数据。
- 不能声称路线是实际园区实时最优路线。
- 实时重规划必须锁定已完成项目。
