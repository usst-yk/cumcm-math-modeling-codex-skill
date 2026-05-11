# Scripts

这些脚本把重复工作固定下来。新手不需要手动运行；Codex 会在需要时后台调用。

| Script | Purpose |
| --- | --- |
| `init_cumcm_project.py` | 创建 `problem/ data/ modeling/ src/ tables/ figures/ results/ paper/` 和 `paper/main.tex`。 |
| `problem_parser.py` | 解析题面，生成题面要点。 |
| `build_task_plan.py` | 拆解子问题，规划表格、图片和验证。 |
| `data_profile.py` | 审计 CSV/XLSX 数据，输出到 `tables/`。 |
| `validate_results.py` | 检查论文、图表、表格和验证说明是否完整一致。 |
| `make_paper_figures.py` | 统一论文图片字体和样式。 |
| `compile_tex.py` | 编译 `paper/main.tex`。 |
| `run_skill_evals.py` | 维护者自检示例和评测文件。 |
| `check_skill_structure.py` | 检查 skill 文件结构。 |
| `build_official_case_index.py` | 校验官方 benchmark 来源索引。 |
