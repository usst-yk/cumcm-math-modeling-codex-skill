# Validation Report

## 数据边界

- 本案例没有官方附件数据，因此 `data/benchmark_activities.csv` 和 `data/realtime_wait_updates.csv` 是透明 benchmark 数据。
- 坐标、排队时间、游客偏好、固定演出时间均用于复现建模流程，不代表上海迪士尼官方或实时运营数据。

## 问题 1 验证

- 每条路线均检查 09:00-21:00 总时间边界。
- 固定演出 `parade`、`castle_show`、`fireworks` 只允许在基准时间窗开始。
- 动态规划路线与贪心基线在 9 个游客-日期组合中逐项比较，平均得分提升 16.74%，最低提升 1.49%。
- 中文图 `fig_q1_model_flow.png`、`fig_q1_result.png`、`fig_q1_validation.png` 对应模型流程、核心结果和基线验证。

## 问题 2 验证

- 13:30 作为 APP 复核时刻；若游客正在体验某项目，则在该项目结束后重规划。
- 已完成项目被锁定，剩余候选项目使用同一实时排队扰动表。
- 相比保持原剩余路线，重规划平均减少等待 19.67 分钟，6 个场景发生路线项目集合变化。
- 中文图 `fig_q2_model_flow.png`、`fig_q2_result.png`、`fig_q2_validation.png` 对应重规划流程、收益结果和保持原路线对照。

## 限制

- 该 benchmark 没有外部真实客流数据校准，不能作为实际出游攻略。
- 动态规划基于离散分钟和有限候选项目，声称的是 benchmark 数据下的最优路线，不声称官方意义上的全局最优。
