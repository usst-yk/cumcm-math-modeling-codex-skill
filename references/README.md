# References

`references/` 存放按需读取的细则。`SKILL.md` 只做总控；遇到具体任务时再读取这里的文件。

## Core Workflow

| File | Purpose |
| --- | --- |
| `task-routing.md` | 判断用户需求对应的工作模式和参考文件。 |
| `problem-parsing.md` | 题面解析标准：子问、输入、输出、约束、单位、附件和风险词。 |
| `agent-workflow.md` | Coordinator -> Modeler -> Coder -> Writer -> Reviewer 的阶段流程。 |
| `stage-gates.md` | 每个阶段进入下一阶段前必须满足的条件。 |
| `workflow.md` | 完整赛题流程和 72 小时节奏。 |
| `task-modes.md` | 只审题、只做单问、写完整论文、终审等常见模式。 |
| `output-policy.md` | 新手默认文件精简输出，避免生成过多模板和空文件；不精简分析、建模、求解、验证或论文。 |

## Modeling And Validation

| File | Purpose |
| --- | --- |
| `problem-routing.md` | 按预测、优化、评价、仿真等题型选择路线。 |
| `cumcm-a-problem-patterns.md` | 2020-2025 国赛 A 题模式统计和 A 题专项方法。 |
| `method-library.md` | 常用数学建模方法库。 |
| `method-cards.json` | 结构化方法卡，供题型到方法的快速路由和自检使用。 |
| `correctness-ladder.md` | 基线、主模型、交叉检查、压力测试。 |
| `analytical-vs-numerical.md` | 解析模型和数值模型如何搭配。 |
| `validation.md` | 不同题型的验证和失败恢复。 |
| `official-benchmark.md` | 官方赛题讲评、论文展示和专家课程的 benchmark 来源。 |
| `first-prize-rubric.md` | 面向一等奖水平判断的 0-2 评分表。 |

## Data, Paper, And Artifacts

| File | Purpose |
| --- | --- |
| `data-audit.md` | 附件数据、Excel 多 sheet、缺失、异常和单位检查。 |
| `result-tracking.md` | 关键数值和论文结论的来源追踪。 |
| `code-to-paper.md` | 代码、表格、图片转论文。 |
| `paper-writing.md` | CUMCM 论文结构和写法。 |
| `paper-assembly.md` | 完整论文总装规则，防止只拼接各问片段。 |
| `paper-section-flow.md` | 分段写作顺序和每节输入输出。 |
| `technical-roadmap.md` | 技术路线图和模型流程图。 |
| `figure-plan.md` | 单问/全题默认应该生成哪些中文示意图和结果图。 |
| `figure-standards.md` | CUMCM 默认图表标准。 |
| `figure-standards-journal.md` | SCI/Nature/PRL 等期刊图表扩展标准。 |

## Review And Maintenance

| File | Purpose |
| --- | --- |
| `scoring-checklist.md` | 评分导向检查表。 |
| `final-checklist.md` | 最终交付检查。 |
| `final-review.md` | 简短评委视角审稿入口。 |
| `safety-rules.md` | 反编造和风险标记规则。 |
| `citation-policy.md` | 参考文献规则。 |
| `python-matlab-guide.md` | Python/MATLAB 实现建议。 |
| `project-templates.md` | 项目目录模板说明。 |
| `external-agent-patterns.md` | 外部数学建模 Agent 项目的可借鉴模式。 |
| `maintenance.md` | 修改和发布 skill 时使用。 |

命名约定：文件名使用 kebab-case，表达主题而不是动作。
