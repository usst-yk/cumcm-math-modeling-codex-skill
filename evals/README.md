# Evals

`evals/` 存放轻量测试提示，用来检查 skill 是否保持基本行为。

| Folder/File | Purpose |
| --- | --- |
| `expected_outputs.md` | 人工检查时的期望行为。 |
| `parser_cases/` | 题面解析测试：预测、优化调度、评价排序、预测+优化组合、括号编号误切、A题工程过程、A题几何光学、A题轨迹覆盖；每个 case 带 `expected_problem_parse.json` golden 输出。 |
| `toy_prediction_problem/prompt.md` | 预测题测试提示。 |
| `toy_optimization_problem/prompt.md` | 优化题测试提示。 |
| `toy_evaluation_problem/prompt.md` | 评价题测试提示。 |

当前自检脚本 `scripts/run_skill_evals.py` 会实际运行题面解析、golden 输出对比、任务计划生成、schema 校验、demo 文件检查和结构化方法卡检查。GitHub Actions 也会在提交和 PR 时运行这些检查。
