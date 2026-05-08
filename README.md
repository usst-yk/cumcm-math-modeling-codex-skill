# Guosai Math Modeling Skill

面向全国大学生数学建模竞赛（CUMCM/国赛）的 Codex skill，用于赛题分析、建模路线设计、算法实现规划、论文写作、图表设计与结果验证。

## 能力特点

- 按国赛高分论文思路进行问题拆解。
- 默认先给 3 条建模路线并比较，再选择主路线和备用路线。
- 每一问覆盖变量定义、目标函数、约束、解析推导、算法步骤、验证方案、可视化设计和论文段落。
- 支持数据预处理、灵敏度分析、稳健性检查、论文摘要和正文写作。
- 附带项目初始化脚本、数据检查脚本、论文模板和附录代码模板。

## 安装

将本仓库复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/keyang1992/guosai-math-modeling-skill.git ~/.codex/skills/guosai-math-modeling
```

重启 Codex 后，在对话中使用：

```text
[$guosai-math-modeling] 请分析这道国赛数学建模题，并按一等奖标准给出建模方案。
```

## 推荐使用方式

提供完整题目时，可直接要求：

```text
按国赛一等奖标准重做：先给 3 条建模路线并比较，选主路线；每问都要包含变量定义、目标函数、约束、解析推导、算法步骤、验证方案、可视化设计和论文段落。
```

如果题目带有 CSV/XLSX 数据，先把数据放入项目目录，再要求 skill 进行字段检查、缺失值检查、异常值检查和预处理方案设计。

## 文件结构

```text
guosai-math-modeling/
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
    └── init_guosai_project.py
```

## 说明

这个 skill 追求竞赛可交付性：不堆砌模型名，优先把每一问转化为可解释、可计算、可验证、可写入论文的方案。数据结果、指标和结论应来自代码输出、题目数据、公式推导或明确假设。
