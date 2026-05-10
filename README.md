# CUMCM Math Modeling Codex Skill

面向全国大学生数学建模竞赛（CUMCM）的 Codex skill。它不是 Web 系统，也不承诺自动获奖；目标是帮助学生把读题、附件审计、逐问建模、代码求解、图表、验证和论文一致性做稳。

## 安装

在 Codex 中直接说：

```text
请安装这个 skill：https://github.com/usst-yk/cumcm-math-modeling-codex-skill
```

安装后重启 Codex。使用时建议显式调用：

```text
[$cumcm-math-modeling] 请先解析这道数学建模题，不要急着建模。
```

## 核心原则

- 先读题，再建模；先检查数据，再写结论。
- 默认精简输出：单问求解不铺满空模板，只生成必要代码、表格、图和论文段落。
- 精简不等于少画图：每个已求解子问题通常至少有中文模型/题意示意图和核心结果图。
- 优化、预测、评价、调度、仿真等问题应补验证、敏感性或约束检查图。
- 关键数字必须能追溯到题面、数据、代码输出、结果表或结果注册表。
- 逐问闭环：分析 → 建模 → 求解 → 图表 → 验证 → 论文段落。

## 最推荐的开局

```text
[$cumcm-math-modeling] 这是我的赛题和附件。请先读题，拆解每一问，检查附件数据，然后给出建模路线。暂时不要直接写完整论文。
```

只做某一问：

```text
[$cumcm-math-modeling] 我只负责第 2 问。请只围绕第 2 问完成题意分析、建模路线、变量公式、求解方案、验证方法、必要图表和可放入论文的段落。
```

所有复杂场景的提示词都集中在：

```text
examples/README.md
```

## 默认输出

只做一问时，通常只需要：

```text
src/              当前问题的求解代码
tables/           当前问题的核心结果表
figures/          当前问题需要的中文图
paper/sections/   只有要求写论文时才生成分问段落
```

只有明确说“初始化完整项目”“全题交付”“所有中间文件都保存下来”，才会生成完整目录、日志、结果注册表、验证报告和论文模板。

## 仓库结构

```text
SKILL.md           Codex 读取的 skill 入口
README.md          简短说明
agents/            题面解析、建模、代码、写作、审稿等角色提示
references/        按需读取的规则和方法库
scripts/           后台辅助工具
templates/         完整项目模式下使用的模板
assets/            静态模板材料
examples/          使用提示、最小单问 demo、完整 demo、真实案例
evals/             轻量测试题，防止能力退化
.github/workflows/ GitHub 自动检查
```

## 示例

```text
examples/README.md
examples/single_question_minimal/
examples/full_problem_demo/
examples/real_cases/cumcm_2025_a/
```

`single_question_minimal/` 展示“只做一问”时最小输出。
`full_problem_demo/` 展示完整交付形态。
`cumcm_2025_a/` 是 2025 年国赛 A 题真实案例，不是标准答案。

## 维护者自检

普通学生不需要运行这些命令。维护 skill 时可以运行：

```text
python3 scripts/run_skill_evals.py
python3 scripts/check_skill_structure.py
```
