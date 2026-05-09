# CUMCM Math Modeling Codex skill

面向全国大学生数学建模竞赛（CUMCM）的 Codex skill，用于赛题分析、建模路线设计、算法实现规划、论文写作、图表设计与结果验证。

## 能力特点

- 按 CUMCM 高分论文思路进行问题拆解。
- 默认先给 3 条建模路线并比较，再选择主路线和备用路线。
- 每一问覆盖变量定义、目标函数、约束、解析推导、算法步骤、验证方案、可视化设计和论文段落。
- 支持基于论文生成黑白技术路线图，并默认给所采用模型的流程框图。
- 支持数据预处理、灵敏度分析、稳健性检查、论文摘要和正文写作。
- 附带项目初始化脚本、数据检查脚本、论文模板和附录代码模板。

## 安装

### 方式一：使用 Git 克隆

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/usst-yk/cumcm-math-modeling-codex-skill.git ~/.codex/skills/cumcm-math-modeling
```

### 方式二：下载 GitHub 压缩包并本地解压

不使用 Git 时，可以下载仓库 ZIP 压缩包：

```bash
mkdir -p ~/.codex/skills
curl -L https://github.com/usst-yk/cumcm-math-modeling-codex-skill/archive/refs/heads/main.zip -o /tmp/cumcm-math-modeling-codex-skill.zip
rm -rf ~/.codex/skills/cumcm-math-modeling
unzip /tmp/cumcm-math-modeling-codex-skill.zip -d /tmp
mv /tmp/cumcm-math-modeling-codex-skill-main ~/.codex/skills/cumcm-math-modeling
```

### 方式三：已有本地压缩包时安装

如果已经拿到 `cumcm-math-modeling-codex-skill.zip`，可直接解压到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/cumcm-math-modeling
unzip /path/to/cumcm-math-modeling-codex-skill.zip -d /tmp/cumcm-skill-install
mv /tmp/cumcm-skill-install/cumcm-math-modeling-codex-skill-main ~/.codex/skills/cumcm-math-modeling
```

如果压缩包解压后的目录名不是 `cumcm-math-modeling-codex-skill-main`，将 `mv` 命令中的源目录改成实际解压出来的目录即可。最终目录应满足：

```text
~/.codex/skills/cumcm-math-modeling/SKILL.md
```

### 生成可分发压缩包

维护者可在仓库上级目录生成一个不包含 `.git` 的安装包：

```bash
cd ~/.codex/skills
zip -r cumcm-math-modeling-codex-skill.zip cumcm-math-modeling -x "cumcm-math-modeling/.git/*"
```

使用该压缩包安装时，解压后的目录可能名为 `cumcm-math-modeling`，直接放入 `~/.codex/skills/` 即可。

重启 Codex 后，在对话中使用：

```text
[$cumcm-math-modeling] 请分析这道 CUMCM 数学建模题，并按一等奖标准给出建模方案。
```

## 推荐使用方式

### 1. 从零开始一口气求解整题

适合什么都还没定，只提供题面和附件，希望从读题、建模、代码、图表到 TeX 论文一次推进：

```text
[$cumcm-math-modeling] 请基于当前题面和附件，从零开始完整求解这道 CUMCM 题。要求先检查数据和题目任务，判断评分点与隐含约束，给出 3 条整体建模路线并选择主路线；随后完成代码求解、图表生成、TeX 论文、技术路线图和模型流程图，并做最终交付检查。所有数值必须可追溯。
```

### 2. 单问完整建模

适合只推进某一问，例如第 1 问或第 2 问：

```text
[$cumcm-math-modeling] 只做 B 题第 1 问。请先判断评分点和隐含约束，再给 3 条建模路线并比较，选择主路线；然后写出变量定义、目标函数、约束条件、解析推导、算法步骤、验证方案、可视化设计，并生成 TeX 论文。
```

### 3. 全题建模路线设计

适合比赛前期定方向：

```text
[$cumcm-math-modeling] 请分析这道 CUMCM 题，拆解每个问题的任务、评分点和隐含约束；给出整体建模路线，说明每问采用的模型、输入输出、验证方式和论文结构。
```

### 4. 按一等奖标准重做

适合已有方案但深度不够时：

```text
[$cumcm-math-modeling] 这个方案不够深，请按 CUMCM 一等奖标准重做。要求包含 3 条路线比较、解析推导、基线模型、主模型、验证、灵敏度分析和论文段落。
```

### 5. 数据求解并生成 TeX 论文

适合附件数据已经在当前项目目录时：

```text
[$cumcm-math-modeling] 基于当前文件夹的数据，完成第 1 问代码求解，并把结果写成 TeX 论文。所有数值必须来自代码输出，图表按规范命名。
```

### 6. 代码到论文

适合已经有代码、输出表格和图片时：

```text
[$cumcm-math-modeling] 根据当前项目里的代码、输出表格和图片，把第 1 问写成 TeX 论文。论文中的数值必须和输出文件一致。
```

### 7. 技术路线图和模型流程图

默认使用 GPT Image 直接生成黑白流程图，并附图注和论文说明：

```text
[$cumcm-math-modeling] 请基于这篇论文生成技术路线图和模型流程框图。要求黑白风格、内容简洁、不要装饰性图标，并附论文图注和说明文字。
```

### 8. 摘要和结论

适合论文主体和结果已经完成后：

```text
[$cumcm-math-modeling] 基于当前论文和结果表，写 CUMCM 摘要。要求每问包含模型、核心结果、关键数值和验证方式，不要背景套话。
```

### 9. 论文审稿和查错

适合提交前检查：

```text
[$cumcm-math-modeling] 请从评委视角审稿这篇论文，重点检查答题覆盖、约束条件、数值可追溯性、验证充分性、图表结论和复现性。
```

### 10. 最终交付检查

适合比赛收尾：

```text
[$cumcm-math-modeling] 请检查当前项目是否达到最终交付标准：TeX、PDF、代码、结果表、图、图注、附录代码和运行命令是否齐全，并列出需补充项。
```

## 推荐工作流

1. 全题拆解与路线选择。
2. 单问建模与代码求解。
3. 代码到 TeX 论文。
4. 生成技术路线图和模型流程图。
5. 写摘要和结论。
6. 审稿查错。
7. 最终交付检查。

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
