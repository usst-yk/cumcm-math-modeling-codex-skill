# External Agent Patterns

记录外部数学建模 Agent 项目中值得借鉴的设计思想。除非许可证兼容且处理好署名，否则不要把外部源码直接复制进本 skill。

## MathModelAgent 可借鉴点

- Coordinator -> Modeler -> Coder -> Writer 的角色分工。
- 按子问题循环推进，而不是先写整篇论文。
- 在求解前显式做 EDA。
- 代码失败后有重试、反思和错误记录。
- 论文段落从代码输出和生成图片中写出。
- 工作目录中保留必要结果、图表和中间文件；本 skill 不沿用 notebook
  目录作为默认输出。

本 skill 的对应实现：

- 角色卡放在 `agents/`。
- 阶段门槛放在 `references/stage-gates.md`。
- 子问题循环放在 `references/agent-workflow.md`。
- 失败恢复由 `references/validation.md` 和 `results/validation_report.md` 约束。
- 结果到论文的一致性由 `references/result-tracking.md` 和 `scripts/validate_results.py` 检查。

## MM-Agent 可借鉴点

- 四阶段流程：问题分析、数学建模、计算求解、报告生成。
- 用方法库思路辅助模型选择。
- 用 benchmark/eval 题例检查系统行为。

本 skill 的对应实现：

- `references/method-library.md` 存放轻量建模方法库。
- `evals/` 存放 toy prompts。
- `scripts/run_skill_evals.py` 检查 demo 和 eval 结构。
