# 华东杯 A 题真实案例 benchmark

本目录存放华东杯 A 题“游览路线规划问题”的可复现 benchmark。题面没有提供官方附件、真实排队数据或实时 APP 样例，因此本案例把项目位置、排队时间、游客偏好、固定演出时间和实时扰动全部保存为透明基准数据，用于检查 skill 是否能完成“审题 -> 建模 -> 求解 -> 验证 -> 图表 -> TeX 论文”的闭环。

本案例不是上海迪士尼官方答案，也不是实时出游攻略。

## 已放入的内容

| Path | 内容 |
| --- | --- |
| `problem/problem_statement.pdf` | 从原始赛题 PDF 分离出的 A 题页。 |
| `problem/problem_statement.md` | A 题题面文字。 |
| `problem/problem_parse.json` / `.md` | 人工核对后的 2 问题面解析。 |
| `problem/task_plan.json` / `.md` | Q1/Q2 求解计划和 benchmark 边界。 |
| `modeling/qx_modeling_idea.md` | 每问建模思路，先于代码求解。 |
| `modeling/route_comparison.md` | 静态规划和实时重规划路线比较。 |
| `data/raw/benchmark_activities.csv` | 项目坐标、体验时长、偏好效用、排队时间、固定演出时间窗。 |
| `data/raw/realtime_wait_updates.csv` | 13:30 APP 实时排队扰动 benchmark。 |
| `src/solve_routes.py` | Q1 初始路线和 Q2 实时重规划求解脚本。 |
| `tables/tab_q1_summary.csv` | 3 类游客 x 3 类日期的路线汇总。 |
| `tables/tab_q1_routes.csv` | Q1 逐步路线明细。 |
| `tables/tab_q1_baseline_comparison.csv` | 动态规划路线与贪心基线对比。 |
| `tables/tab_q2_realtime_waits.csv` | 13:30 预测排队与实时排队对照。 |
| `tables/tab_q2_adjustment_summary.csv` | Q2 重规划收益汇总。 |
| `tables/tab_q2_adjusted_routes.csv` | Q2 调整后逐步路线明细。 |
| `figures/fig_problem_overview.png` | 项目位置和固定演出示意图。 |
| `figures/fig_q1_model_schematic.png` | Q1 模型流程示意图。 |
| `figures/fig_q1_result.png` | Q1 核心结果图。 |
| `figures/fig_q1_validation.png` | Q1 与贪心基线对比验证图。 |
| `figures/fig_q2_model_schematic.png` | Q2 实时重规划流程示意图。 |
| `figures/fig_q2_result.png` | Q2 等待节省和得分增益图。 |
| `figures/fig_q2_validation.png` | Q2 保持原路线与重规划路线对照图。 |
| `results/result_registry.csv` | 关键 benchmark 数值登记表。 |
| `results/validation_report.md` | 可行性、基线和实时调整验证记录。 |
| `paper/main.tex` | 可编译完整 benchmark 论文；问题一和问题二都写在这个单文件中。 |

## 核心 benchmark 结果

- Q1：动态规划路线相对贪心基线平均得分提升 16.74%。
- Q1：最高体验得分为 96.734，出现在家庭亲子游-工作日场景。
- Q1：节假日家庭亲子游推荐完成 9 项非休整体验。
- Q2：13:30 实时重规划较保持原剩余路线平均减少等待 19.67 分钟。
- Q2：13:30 实时重规划平均得分增益 3.626。
- Q2：9 个场景中有 6 个场景触发了剩余项目集合变化。

## 使用方式

```text
[$cumcm-math-modeling] 请以 examples/real_cases/huadong_cup_a 为 benchmark，复现华东杯 A 题的路线规划和实时调整结果，并检查结果是否和 registry 一致。
```

如果只想看题面解析：

```text
[$cumcm-math-modeling] 请阅读 examples/real_cases/huadong_cup_a/problem/problem_parse.md，说明这道题的变量、约束、输出和建模风险。
```

## 当前限制

- benchmark 数据不是官方数据，也没有真实客流校准。
- 求解只覆盖题面要求的 2 个问题，不扩展到真实票务、身高限制、快速通道、餐厅容量或天气影响。
- 动态规划基于筛选后的核心项目集合，结果用于稳定 benchmark，不声称真实园区全局最优。
