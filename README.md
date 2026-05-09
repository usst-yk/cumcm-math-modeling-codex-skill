# CUMCM Math Modeling Codex Skill

面向全国大学生数学建模竞赛（CUMCM）的 Codex skill，用于把建模任务组织成可审计、可复现、可写入论文的工作流。

这个仓库不是完整 Web/后端多 Agent 系统，也不承诺自动生成获奖论文。它更像一套 Codex 内部可调用的工作规范、项目模板和辅助脚本：帮助完成题意拆解、数据审计、建模路线设计、代码产物管理、结果追踪、验证检查、图表规范和论文写作。

## 适合做什么

- 拆解 CUMCM 题目，形成 `problem/task_plan.json`。
- 审计附件数据，尤其是 CSV/XLSX 多文件、多 sheet 覆盖情况。
- 比较三条建模路线，保留基线模型和主模型的取舍依据。
- 按子问题逐问推进：模型卡、代码、表格、图、结果登记、验证、论文段落。
- 用 `results/result_registry.csv` 追踪关键结论、数值来源和复现命令。
- 生成可编辑的技术路线图 SVG，而不是默认依赖不可编辑图片。
- 从评委视角检查论文、代码、表格、图和摘要是否一致。

## 不适合做什么

- 不保证获奖。
- 不替代人工判断关键假设和建模取舍。
- 不编造缺失数据、参考文献、指标、距离、排名或最优值。
- 不自动提交竞赛材料。
- 不把 Codex skill 变成完整 Web 应用或后端 Agent 服务。

## 工作流设计

该 skill 借鉴多角色流水线，但不实现独立 Agent 后端。Codex 使用这些角色卡作为阶段提示：

1. Coordinator：题意拆解，生成任务计划。
2. Data Auditor：附件和数据审计。
3. Modeler：路线比较、模型卡和基线设计。
4. Solver：代码求解，保存表格、图和运行日志。
5. Validator：误差、可行性、敏感性和一致性检查。
6. Writer：基于结果注册表写论文段落。
7. Reviewer：评委视角终审。

关键阶段门禁写在 `references/stage-gates.md`。例如：没有完成数据审计和基线路线，不进入求解；关键数值没有登记到结果注册表，不进入最终写作。

## 项目初始化

```bash
python scripts/init_cumcm_project.py --name cumcm_2026_A
```

会生成：

```text
problem/                 # 题面、假设、task_plan、model cards
data/raw/                # 原始附件
data/processed/          # 清洗或重构后的数据
src/                     # 按子问题组织的求解脚本
notebooks/               # 可选探索 notebook
results/                 # result_registry、validation report、敏感性分析
figures/                 # 论文图和路线图
tables/                  # 结果表和数据审计表
paper/                   # TeX/Markdown 论文
appendix/                # 附录代码和补充材料
logs/                    # run_log 和 error_log
```

## 常用脚本

```bash
python scripts/build_task_plan.py --problem problem/problem_statement.md --output-dir problem
python scripts/data_profile.py --input data/raw --output tables/data_profile
python scripts/result_registry.py --registry results/result_registry.csv --subquestion Q1 --claim "..." --value "..." --source-file tables/tab_q1_result.csv
python scripts/make_roadmap_svg.py --task-plan problem/task_plan.json --output figures/roadmap.svg
python scripts/validate_results.py --project .
python scripts/compile_tex.py --tex paper/main.tex
```

## 示例

`examples/full_problem_demo/` 提供一个很小的配送 toy 题，用来检查数据审计、任务计划、路线图、结果注册表和验证脚本是否能串起来。它只是工作流演示，不代表真实国赛题的复杂度。

## 推荐使用方式

### 全题路线设计

```text
[$cumcm-math-modeling] 请分析这道 CUMCM 题，先拆解每问的输入、模型对象、输出和验证标准；再给出 3 条整体建模路线和 72 小时推进顺序。先不要写最终论文。
```

### 单问推进

```text
[$cumcm-math-modeling] 只推进第 1 问。请先写 Q1 model card，再给出基线、主模型、验证方案、预期表格和图表命名。没有可追溯数据时不要写最终数值结论。
```

### 数据审计

```text
[$cumcm-math-modeling] 请审计当前 data/raw 中的附件，列出所有文件和 Excel sheet，生成数据覆盖、缺失、异常、时间范围和重复值检查，并指出哪些表可用于建模。
```

### 代码到论文

```text
[$cumcm-math-modeling] 根据当前代码输出、结果表和图片写第 1 问论文段落。请先读取结果注册表和输出文件；论文中的数值必须能追溯到表格、代码输出、公式或明确假设。
```

### 终审检查

```text
[$cumcm-math-modeling] 请从评委视角检查当前项目，重点看题意覆盖、数据审计、结果注册表、验证报告、图表引用、摘要数字和代码复现命令是否一致。
```

## 文件结构

```text
cumcm-math-modeling/
├── SKILL.md
├── agents/
├── assets/
├── examples/
├── evals/
├── references/
├── scripts/
└── templates/
```

## 设计原则

- 先审题和审计数据，再建模。
- 先基线和可解释结构，再复杂算法。
- 先保存代码产物，再写论文结论。
- 每个关键数值必须可追溯。
- 验证失败或输入不足时，记录阻塞项，不硬写最终结论。
