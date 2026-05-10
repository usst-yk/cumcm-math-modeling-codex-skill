# Scripts

这些脚本用于把重复、容易出错的工作固定下来。普通学生不需要手动运行；Codex 会在需要时后台调用。

| Script | Purpose |
| --- | --- |
| `init_cumcm_project.py` | 创建标准数学建模项目目录。 |
| `build_task_plan.py` | 生成题目拆解模板。 |
| `data_profile.py` | 审计 CSV/XLSX/JSON/TXT 数据和 Excel 多 sheet。 |
| `result_registry.py` | 维护关键结果注册表。 |
| `validate_results.py` | 检查论文、图表、表格和结果注册表是否一致。 |
| `make_roadmap_svg.py` | 从任务计划生成可编辑路线图 SVG。 |
| `make_paper_figures.py` | 提供统一论文图表样式。 |
| `compile_tex.py` | 编译 TeX 论文并保存错误日志。 |
| `run_skill_evals.py` | 维护者自检 demo 和 eval 文件完整性。 |

命名约定：脚本使用 snake_case，优先使用动词开头或明确动作名。

