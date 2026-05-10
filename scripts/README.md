# Scripts

这些脚本用于把重复、容易出错的工作固定下来。普通学生不需要手动运行；Codex 会在需要时后台调用。

| Script | Purpose |
| --- | --- |
| `init_cumcm_project.py` | 默认创建精简项目目录；加 `--full` 才复制完整模板。 |
| `problem_parser.py` | 离线规则解析题面，生成 `problem_parse.json/md`。 |
| `build_task_plan.py` | 生成题目拆解模板，并默认规划示意图、结果图和必要验证图。 |
| `data_profile.py` | 默认输出精简数据审计；加 `--full` 才输出全部审计表。 |
| `result_registry.py` | 维护关键结果注册表。 |
| `validate_results.py` | 检查论文、图表、表格和结果注册表是否一致；支持 `--mode lean/full`。 |
| `make_roadmap_svg.py` | 从任务计划生成可编辑路线图 SVG，也可导出逐问路线图。 |
| `build_official_case_index.py` | 校验官方 benchmark 来源索引，不下载官方论文内容。 |
| `check_skill_structure.py` | 检查 SKILL front matter、引用路径和关键入口文件。 |
| `make_paper_figures.py` | 提供统一论文图表样式。 |
| `compile_tex.py` | 编译 TeX 论文并保存错误日志。 |
| `run_skill_evals.py` | 维护者自检 demo 和 eval 文件完整性。 |

命名约定：脚本使用 snake_case，优先使用动词开头或明确动作名。
