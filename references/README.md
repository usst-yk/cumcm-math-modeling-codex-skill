# References

`references/` 存放按需读取的细则。`SKILL.md` 只做总控；遇到具体任务时再读取这里的文件。

## 2025 B Problem Evidence Chain

| File | Purpose |
| --- | --- |
| `reference_miner.md` | 从官方题面、讲评、展示论文笔记和用户提供材料中提取结构、模型、数据、验证和图表规则，禁止照抄表述或结果。 |
| `award-paper-learning.md` | 规定公开优秀论文/获奖论文包的结构化学习流程、差距表和反抄袭边界。 |
| `B_problem_data_pipeline.md` | 审计红外光谱附件的单位、排序、等间距重采样、异常波段、去趋势、平滑、滑窗 FFT 和 SNR 选带。 |
| `B_problem_model_referee.md` | 检查 Snell、Fresnel、Cauchy 色散、非线性拟合、双角度联合和 Airy 多光束模型是否到位。 |
| `B_problem_validation.md` | 规定峰间距/FFT/拟合互证、角度一致性、残差诊断、敏感性、不确定度和多光束对比门槛。 |
| `B_problem_figure_referee.md` | 审查机制图、处理图、频域图、拟合图、残差图、敏感性图和多光束判定图是否支撑结论。 |
| `storyline_planner.md` | 把 B 题写成“物理基线 -> 实测反演 -> 多光束判定与修正”的三问递进故事线。 |

## Core Workflow

| File | Purpose |
| --- | --- |
| `task-routing.md` | 判断用户需求对应的工作模式和参考文件。 |
| `problem-parsing.md` | 题面解析标准：子问、输入、输出、约束、单位、附件和风险词。 |
| `agent-workflow.md` | Coordinator -> Modeler -> Coder -> Writer -> Reviewer 的阶段流程。 |
| `stage-gates.md` | 每个阶段进入下一阶段前必须满足的条件。 |
| `workflow.md` | 完整赛题流程和 72 小时节奏。 |
| `task-modes.md` | 只审题、只做单问、写完整论文、终审等常见模式。 |
| `output-policy.md` | 新手默认论文优先输出，避免生成过多模板和空文件；所有工作都要回到 `paper/main.tex`。 |

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
| `figure-plan.md` | 单问/全题默认应该生成哪些 GPT-image 模型流程图、结果图和验证图。 |
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
