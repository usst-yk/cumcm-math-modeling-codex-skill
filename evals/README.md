# Evals

`evals/` 存放轻量测试提示，用来检查 skill 是否保持基本行为。

| Folder/File | Purpose |
| --- | --- |
| `expected_outputs.md` | 人工检查时的期望行为。 |
| `toy_prediction_problem/prompt.md` | 预测题测试提示。 |
| `toy_optimization_problem/prompt.md` | 优化题测试提示。 |
| `toy_evaluation_problem/prompt.md` | 评价题测试提示。 |

当前自检脚本 `scripts/run_skill_evals.py` 检查这些文件是否存在。后续可以扩展为真正运行 toy cases 并检查产物。

