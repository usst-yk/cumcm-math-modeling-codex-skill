# Examples

新手直接复制下面的提示即可。每次建模都会围绕
`problem/ data/ modeling/ src/ tables/ figures/ results/ paper/` 推进，
最后写回 `paper/main.tex`。

## 刚拿到题

```text
[$cumcm-math-modeling] 这是我的赛题和附件。请先读题，拆解每一问，检查附件数据，给出建模路线，并说明每一问需要哪些表格、图片、验证和论文内容。
```

## 只做第一问

```text
[$cumcm-math-modeling] 只做第 1 问。请完成题意分析、变量定义、模型假设、核心公式、求解步骤、结果表、GPT-image 模型流程图、结果图、验证图，并把完整正文写入 paper/main.tex。
```

## 先把模型想清楚

```text
[$cumcm-math-modeling] 请把当前建模路线展开成详细数学模型。要求包括问题对象、变量和参数、合理假设、符号表、核心公式、目标函数或评价函数、约束条件、求解步骤、基线模型、验证方法、图表计划，以及为什么这个模型刚好可解。
```

## 写代码前

```text
[$cumcm-math-modeling] 在写代码前，请先保存 modeling/qx_modeling_idea.md。每一问都要写清输入输出、变量、假设、公式、约束、基线模型、主模型、求解计划、验证计划、图表计划和论文写法。
```

## 跑完代码后

```text
[$cumcm-math-modeling] 代码已经跑完。请反向核对代码实际使用的变量、公式、约束、算法、结果表和图片，修正 modeling/qx_modeling_idea.md，并把最终模型、结果和验证写进 paper/main.tex。
```

## 补流程图和技术路线图

```text
[$cumcm-math-modeling] 请为当前模型生成 GPT-image 流程图和技术路线图。提示词保存在 modeling/，成图保存在 figures/，并把图注和解释写入 paper/main.tex。
```

## 写论文正文

```text
[$cumcm-math-modeling] 请根据已有建模思路、代码、结果表、图片和验证报告写 paper/main.tex。正文要包括问题分析、假设和符号、模型公式、求解过程、结果解释、验证分析、模型评价、结论和复现说明。
```

## 最后写摘要

```text
[$cumcm-math-modeling] 正文、结果表、图片和验证报告已经完成。请最后写摘要：逐问说明使用的数学模型、核心结果、验证证据、问题之间的联系和模型局限，并保证所有数字都能追溯到已保存文件。
```

## 提交前检查

```text
[$cumcm-math-modeling] 请用评委视角检查 paper/main.tex、tables/、figures/ 和 results/。重点找题意没覆盖、假设不合理、公式缺失、图表不支撑结论、数字不一致、验证不足和摘要空泛的问题，并直接修正。
```

## 示例目录

| 目录 | 用途 |
| --- | --- |
| `single_question_minimal/` | 只做一问的最小示例。 |
| `full_problem_demo/` | 小型三问 toy demo，用来检查完整流程。 |
| `real_cases/cumcm_2025_a/` | 2025 国赛 A 题 benchmark，覆盖 Q1-Q5。 |
| `real_cases/huadong_cup_a/` | 华东杯 A 题路线规划 benchmark。 |
