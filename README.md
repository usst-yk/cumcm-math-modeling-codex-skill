# CUMCM Math Modeling Codex skill

面向全国大学生数学建模竞赛（CUMCM）的 Codex skill，用于赛题分析、建模路线设计、算法实现规划、论文写作、图表设计与结果验证。

## 能力特点

- 按 CUMCM 高分论文思路进行问题拆解。
- 默认先给 3 条建模路线并比较，再选择主路线和备用路线。
- 每一问覆盖变量定义、目标函数、约束、解析推导、算法步骤、验证方案、可视化设计和论文段落。
- 支持数据预处理、灵敏度分析、稳健性检查、论文摘要和正文写作。
- 附带项目初始化脚本、数据检查脚本、论文模板和附录代码模板。

## 安装

将本仓库复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/usst-yk/cumcm-math-modeling-codex-skill.git ~/.codex/skills/cumcm-math-modeling
```

重启 Codex 后，在对话中使用：

```text
[$cumcm-math-modeling] 请分析这道 CUMCM 数学建模题，并按一等奖标准给出建模方案。
```

## 推荐使用方式

### 完整题目一键分析

提供完整题目时，可直接要求：

```text
[$cumcm-math-modeling] 请分析这道 CUMCM 数学建模题，并按一等奖标准给出完整建模方案：先给 3 条建模路线并比较，选主路线和备用路线；每问都要包含变量定义、目标函数、约束、解析推导、算法步骤、验证方案、可视化设计和论文段落。
```

### 只做某一问

如果只想先推进某一问，可以这样写：

```text
[$cumcm-math-modeling] 只做这道题的第 X 问。请先判断该问的评分点和隐含约束，再给 3 条建模路线并比较，选择主路线；然后完整写出该问的变量定义、目标函数、约束条件、解析推导、算法步骤、验证方案、可视化设计和可直接放进论文的中文段落。
```

### 某一问深度重做

已有初稿但觉得某一问不够深入时：

```text
[$cumcm-math-modeling] 下面是我对第 X 问的现有解法。请按 CUMCM 一等奖标准重做：指出当前解法浅在哪里，补充机制分析或解析推导，加入基准模型、主模型、稳健性检验、灵敏度分析和论文写法。
```

### 只要建模路线，不写代码

适合比赛前期快速定方向：

```text
[$cumcm-math-modeling] 先不要写代码。请把题目分解成每一问的输入、模型对象、输出和验证标准；然后给出 3 条整体建模路线，比较优缺点、实现风险和论文表现力，最后推荐一条 72 小时内可完成的主路线。
```

### 从数据开始

如果题目带有 CSV/XLSX 数据，先把数据放入项目目录，再要求 skill 进行字段检查、缺失值检查、异常值检查和预处理方案设计。

```text
[$cumcm-math-modeling] 先检查数据，不要急着建模。请读取附件中的 CSV/XLSX，给出字段含义推断、缺失值、异常值、单位、相关性、可用于每一问的变量，以及数据预处理方案。然后说明这些数据能支持哪些模型，哪些结论不能直接下。
```

### 写论文段落

如果已经有模型和结果，需要转成论文表达：

```text
[$cumcm-math-modeling] 请把下面的模型、算法和结果改写成 CUMCM 论文风格。要求包含模型建立、模型求解、结果分析、灵敏度分析和优缺点评价，语言正式、紧凑、带公式说明，并避免堆砌模型名。
```

### 修改摘要

如果已经有论文正文或各问结果，需要打磨摘要：

```text
[$cumcm-math-modeling] 请修改下面这篇 CUMCM 论文摘要。要求按“问题背景-每问方法-关键结果-模型优势与局限”的结构重写，突出具体数值结果和结论，不堆砌模型名，语言正式紧凑，控制在 300-500 字，并给出 3-5 个关键词。
```

### 检查论文是否够高分

用于提交前审稿：

```text
[$cumcm-math-modeling] 请按 CUMCM 一等奖标准审查这篇建模论文：逐问检查是否回答完整、模型是否有机制解释、验证是否充分、图表是否支撑结论、摘要是否突出结果、附录代码是否可复现，并给出优先修改清单。
```

## 文件结构

```text
cumcm-math-modeling/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── appendix-code-template.md
│   ├── assumptions-symbols-template.md
│   ├── paper-template.docx
│   └── paper-template.md
├── references/
│   ├── analytical-vs-numerical.md
│   ├── contest-modes.md
│   ├── figure-standards.md
│   ├── modeling-toolbox.md
│   ├── paper-writing.md
│   ├── problem-routing.md
│   ├── project-templates.md
│   ├── python-matlab-guide.md
│   ├── safety-rules.md
│   ├── scoring-checklist.md
│   └── workflow.md
└── scripts/
    ├── data_profile.py
    └── init_cumcm_project.py
```

## 说明

这个 skill 追求竞赛可交付性：不堆砌模型名，优先把每一问转化为可解释、可计算、可验证、可写入论文的方案。数据结果、指标和结论应来自代码输出、题目数据、公式推导或明确假设。
