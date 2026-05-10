# Agents

这些文件不是后端 Agent 实现，而是 Codex 在不同阶段使用的角色卡。

| File | Purpose |
| --- | --- |
| `problem_parser.md` | 先做题面事实抽取，不进入建模。 |
| `coordinator.md` | 读题、拆题、识别约束和风险点。 |
| `modeler.md` | 比较三条建模路线，形成每问模型卡。 |
| `coder.md` | 写可复现代码，保存表格、图和结果记录。 |
| `writer.md` | 从已登记结果写论文段落。 |
| `abstract_writer.md` | 在各问正文和结果确定后，最后写并检查摘要。 |
| `reviewer.md` | 从评委视角做终审和阻塞项检查。 |
| `openai.yaml` | Codex UI 展示元数据。 |

命名约定：角色卡使用单数角色名，保持简短稳定；解析和协调分开，避免一上来就建模。
