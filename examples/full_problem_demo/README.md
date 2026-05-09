# Full Problem Demo

This is a small toy case for checking the skill workflow without claiming contest-level performance.

Suggested local commands from the demo root:

```bash
python ../../scripts/data_profile.py --input data/raw --output tables/data_profile
python ../../scripts/build_task_plan.py --problem problem/problem_statement.md --output-dir problem --problem-id toy_demo
python ../../scripts/make_roadmap_svg.py --task-plan problem/task_plan.json --output figures/roadmap.svg
python ../../scripts/result_registry.py --registry results/result_registry.csv --subquestion Q1 --claim "第7天总需求待建模计算" --status draft
python ../../scripts/validate_results.py --project .
```

Expected checks:

- data audit lists `station_demand.csv`;
- time range is detected from `date`;
- spatial fields are detected from longitude/latitude/city;
- task plan contains Q1-Q3;
- roadmap SVG is generated;
- validation audit reports missing paper artifacts until a paper is written.
