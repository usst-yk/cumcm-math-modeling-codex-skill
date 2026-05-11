# Full Problem Demo

This is a small toy case for checking the skill workflow without claiming contest-level performance.

The demo contains:

- problem statement;
- raw station-demand data;
- task plan;
- a reproducible solving script;
- generated result tables;
- generated figures;
- result registry;
- validation report;
- a Q1 paper fragment.

To regenerate artifacts from the demo root, run the demo solving script and then the audit tools.

Expected checks:

- data audit lists `station_demand.csv`;
- task plan contains Q1-Q3;
- result tables are generated under `tables/`;
- figures are generated under `figures/`;
- `results/result_registry.csv` contains R001-R003;
- `results/validation_report.md` records basic validation;
- `paper/main.tex` contains the traceable TeX paper.
