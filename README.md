# CUMCM Math Modeling Codex Skill

面向全国大学生数学建模竞赛（CUMCM）的 Codex skill。它不是完整 Web/后端 Agent 系统，也不承诺自动生成获奖论文；它的定位是把 Codex 的数学建模过程组织成更稳定的工作流：先审题、审计数据、比较路线，再按子问题生成代码产物、登记结果、做验证，最后写论文和终审。

## 项目见解

数学建模竞赛里，AI 最容易出错的地方不是“不会写模型名”，而是：

- 没有读全题意和附件，只解决了一个相邻问题。
- Excel 多 sheet 没检查，数据覆盖不完整。
- 摘要、正文、表格、图和代码输出的数字不一致。
- 直接写“最优”“精度较高”，但没有可行性、误差或敏感性验证。
- 技术路线图好看但不可编辑，文字和箭头逻辑不可控。

这个 skill 的设计重点就是压住这些风险。它借鉴多角色流水线思想，但不做复杂后端，而是在 Codex 内部使用阶段提示、项目模板和检查脚本，形成一个可审计、可复现、可追踪的建模交付流程。

## Codex 安装

在 Codex 中直接请求安装这个 GitHub 仓库：

```text
请安装这个 skill：https://github.com/usst-yk/cumcm-math-modeling-codex-skill
```

安装后重启 Codex。

使用时可以显式调用：

```text
[$cumcm-math-modeling] 请分析这道 CUMCM 题，先做题意拆解和建模路线设计。
```

## 使用指南

### 1. 开始新题

让 Codex 先建立一个标准工作区，后面的题面、数据、代码、图、表和论文都放在固定位置。你不需要手动运行脚本，直接这样说：

```text
[$cumcm-math-modeling] 请为这道题新建一个项目，项目名为 cumcm_2026_A，然后把后续数据、代码、图表、论文和日志都放进这个项目目录。
```

这个操作只是整理工作区，会生成 `problem/`、`data/raw/`、`src/`、`results/`、`figures/`、`tables/`、`paper/`、`logs/` 等目录，并放入任务计划、结果注册表和论文模板。它的作用是防止文件散乱、数字追踪断掉。

### 2. 全题路线设计

适合比赛前期定方向：

```text
[$cumcm-math-modeling] 请分析这道 CUMCM 题，先拆解每问的输入、模型对象、输出和验证标准；再给出 3 条整体建模路线和 72 小时推进顺序。先不要写最终论文。
```

### 3. 单问推进

适合只做某一问，避免全题发散：

```text
[$cumcm-math-modeling] 只推进第 1 问。请先写 Q1 model card，再给出基线、主模型、验证方案、预期表格和图表命名。没有可追溯数据时不要写最终数值结论。
```

### 4. 数据审计

适合已经有附件数据时：

```text
[$cumcm-math-modeling] 请审计当前 data/raw 中的附件，列出所有文件和 Excel sheet，生成数据覆盖、缺失、异常、时间范围和重复值检查，并指出哪些表可用于建模。
```

### 5. 代码到论文

适合已有代码、表格和图后写论文：

```text
[$cumcm-math-modeling] 根据当前代码输出、结果表和图片写第 1 问论文段落。请先读取结果注册表和输出文件；论文中的数值必须能追溯到表格、代码输出、公式或明确假设。
```

### 6. 技术路线图

默认优先生成可编辑 SVG / Mermaid / Graphviz 源，而不是直接生成不可编辑图片：

```text
[$cumcm-math-modeling] 请根据当前 task_plan.json 生成技术路线图，优先输出可编辑 SVG，并附论文图注。
```

### 7. 终审检查

适合提交前检查：

```text
[$cumcm-math-modeling] 请从评委视角检查当前项目，重点看题意覆盖、数据审计、结果注册表、验证报告、图表引用、摘要数字和代码复现命令是否一致。
```

## 文件架构

```text
cumcm-math-modeling/
├── SKILL.md                  # skill 入口和触发后的核心工作流
├── agents/                   # Coordinator/Modeler/Coder/Writer/Reviewer 角色卡
├── assets/                   # 论文、假设、附录模板
├── examples/                 # 示例提示词和 toy demo
├── evals/                    # 轻量评估用例
├── references/               # 按需加载的详细规则
├── scripts/                  # 数据审计、任务计划、结果登记、验证、路线图等脚本
└── templates/                # task_plan、model_card、result_registry、TeX 等模板
```

关键文件：

- `references/stage-gates.md`：阶段门禁。
- `references/problem-routing.md`：题型与组合题型路由。
- `references/data-audit.md`：数据审计规则。
- `references/result-tracking.md`：结果注册表规则。
- `scripts/data_profile.py`：附件数据审计。
- `scripts/validate_results.py`：论文、图表、表格和结果注册表一致性检查。
- `scripts/make_roadmap_svg.py`：生成可编辑技术路线图。
- `scripts/init_cumcm_project.py`：后台初始化项目工作区；一般让 Codex 调用即可。

## 设计原则

- 先审题和审计数据，再建模。
- 先基线和可解释结构，再复杂算法。
- 按子问题逐问推进，不先写整篇最终论文。
- 先保存代码产物，再写论文结论。
- 每个关键数值必须进入结果注册表。
- 技术路线图优先可编辑源文件。
- 验证失败或输入不足时，记录阻塞项，不硬写最终结论。

## 边界

- 不保证获奖。
- 不替代人工确认关键假设。
- 不编造缺失数据、参考文献、指标、距离、排名或最优值。
- 不自动提交竞赛材料。
- 不把 Codex skill 变成完整 Web 应用或后端 Agent 服务。
