# Agents

这些文件不是后端 Agent 实现，而是 Codex 在不同阶段使用的角色卡。

| File | Purpose |
| --- | --- |
| `problem_parser.md` | 先做题面事实抽取，不进入建模。 |
| `coordinator.md` | 读题、拆题、识别约束和风险点。 |
| `background_researcher.md` | 在建模前做背景、官方案例、方法和领域资料调研。 |
| `modeler.md` | 比较三条建模路线，形成每问建模思路/模型卡。 |
| `coder.md` | 写可复现代码，保存表格、图和结果记录。 |
| `writer.md` | 从已登记结果写论文段落。 |
| `paper_assembler.md` | 把各问段落、图表、验证和结论总装成完整论文。 |
| `abstract_writer.md` | 在各问正文和结果确定后，最后写并检查摘要。 |
| `supervisor.md` | 在阶段门处做 pass/revise/block 判断并分派返工 owner。 |
| `reviewer.md` | 从评委视角做终审和阻塞项检查。 |
| `openai.yaml` | Codex UI 展示元数据。 |

协作约定：`coordinator.md` 负责在任务计划中留下 benchmark_sources、rubric_targets 和 revision_status 的初稿；`modeler.md` 和 `reviewer.md` 负责把每问 selling_points 与验证证据对齐。

命名约定：角色卡使用单数角色名，保持简短稳定；解析和协调分开，避免一上来就建模。
