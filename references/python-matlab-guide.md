# Python / MATLAB 双路线

## 选择原则

- 默认使用 Python：适合数据清洗、机器学习、批量图表、可复现项目结构。
- 用户要求 MATLAB 或团队熟悉 MATLAB 时使用 MATLAB：适合矩阵计算、优化工具箱、经典数值计算和工程队伍协作。
- 不在同一子问题中混用两种语言，除非有明确分工。

## Python 路线

推荐目录：

- `src/01_data_profile.py`
- `src/02_preprocess.py`
- `src/03_model_q1.py`
- `src/04_model_q2.py`
- `src/05_model_q3.py`
- `src/plot_style.py`

常用库：

- 数据：pandas、numpy、openpyxl。
- 统计和预测：statsmodels、scikit-learn。
- 优化：scipy.optimize、pulp、ortools。
- 图网络：networkx。
- 绘图：matplotlib、seaborn。

要求：

- 设置随机种子。
- 所有图表保存到 `figures/` 和 `tables/`。
- 每个脚本顶部说明输入和输出。
- 不把结果只保存在交互式 notebook 中。

## MATLAB 路线

推荐目录：

- `src/01_data_profile.m`
- `src/02_preprocess.m`
- `src/03_model_q1.m`
- `src/04_model_q2.m`
- `src/05_model_q3.m`
- `src/plot_style.m`

常用功能：

- 数据读取：`readtable`, `readmatrix`。
- 优化：`linprog`, `intlinprog`, `fmincon`, `ga`, `particleswarm`。
- 统计和机器学习：Statistics and Machine Learning Toolbox。
- 微分方程：`ode45`, `ode15s`。
- 绘图：`plot`, `bar`, `heatmap`, `exportgraphics`。

要求：

- 使用 `rng(2024)` 固定随机种子。
- 使用 `exportgraphics` 输出 300 dpi PNG 和矢量 PDF。
- 变量命名和论文符号尽量一致。
- 每个 `.m` 文件说明输入、输出和对应论文问题。

## 代码到论文映射

无论使用 Python 还是 MATLAB，都要维护映射：

| 论文位置 | 代码文件 | 输出文件 | 说明 |
|---|---|---|---|
| 问题一结果 | `src/03_model_q1.py` / `.m` | `figures/fig_q1_*.png` | …… |
| 问题二结果 | `src/04_model_q2.py` / `.m` | `tables/table_q2_*.csv` | …… |
| 灵敏度分析 | `src/sensitivity.py` / `.m` | `figures/fig_sensitivity_*.png` | …… |
