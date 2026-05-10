# Task Plan

- Contest: 华东杯
- Problem: huadong_cup_a
- Question count: 2
- Status: solved benchmark

| ID | Type | Input | Model object | Output | Validation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 | optimization | `benchmark_activities.csv` | 游客项目访问顺序 | 9 个游客-日期路线、得分、等待和步行时间 | 时间窗检查；闭园时间检查；贪心基线比较 | solved |
| Q2 | optimization | Q1 路线；`realtime_wait_updates.csv` | 13:30 后剩余路线 | 调整路线、等待节省、得分增益、项目变更 | 保持原路线对照；实时排队敏感性；时间窗检查 | solved |

## Routes

- Q1 baseline：按单位时间效用最高的项目贪心选线。
- Q1 primary：带排队、步行、时间窗和偏好效用的分钟级动态规划搜索。
- Q2 baseline：保持 Q1 原剩余路线，仅用实时排队更新重新计时。
- Q2 primary：锁定已完成项目后，对剩余项目重新规划。

## Benchmark Boundary

本案例用于 skill benchmark。题面未给官方附件，因此所有数值数据均来自本目录 `data/raw/`，不能解释为官方答案或实时出游建议。
