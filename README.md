# CUMCM Math Modeling Codex Skill

这是一个面向全国大学生数学建模竞赛和同类竞赛的 Codex skill。

它会帮助你完成从读题到论文的基本流程：拆解问题、检查数据、设计模型、
写代码求解、生成图表、验证结果，并把最终内容写入 `paper/main.tex`。

## 安装

在 Codex 中说：

```text
请安装这个 skill：https://github.com/usst-yk/cumcm-math-modeling-codex-skill
```

安装后重启 Codex。

## 最简单用法

刚拿到赛题和附件时，可以这样说：

```text
[$cumcm-math-modeling] 请先读题，拆解每一问，检查附件数据，并给出建模路线。
```

只做某一问时，可以这样说：

```text
[$cumcm-math-modeling] 我只做第 1 问。请完成建模、求解、验证、图表和可写入论文的正文。
```

已有代码和结果时，可以这样说：

```text
[$cumcm-math-modeling] 请根据当前代码、结果表和图片写入 paper/main.tex，关键数字必须能找到来源。
```

## 默认输出目录

```text
problem/          题面原文、题意解析、每问任务拆解
data/             原始数据、清洗数据、预处理结果
modeling/         每一问的建模思路、代码建模流程、验证方案、流程图提示
src/              数据处理、模型求解、绘图和验证代码
tables/           数据审计表、结果表、约束检查表、敏感性分析表
figures/          论文图片，包括流程图、结果图、验证图
results/          验证报告、结果来源说明、最终校验记录
paper/main.tex    唯一论文入口文件
```

默认最终交付都围绕 `paper/main.tex` 展开。
