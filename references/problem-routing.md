# Problem Routing

Use this reference after parsing the problem statement. Select models from the task form, data scale, validation path, and paper objective, not from method popularity.

## Routing Matrix

For CUMCM A problems, also read `references/cumcm-a-problem-patterns.md`.
Recent A problems often combine mechanism simulation, geometry, and constrained
optimization; route them by physical object and validation path before choosing
an algorithm.

| 题型 | 优先基线 | 主模型候选 | 必做验证 |
| --- | --- | --- | --- |
| 预测 | 均值、移动平均、线性趋势、季节朴素预测 | ARIMA/SARIMA、指数平滑、状态空间、随机森林、XGBoost、SVR、LSTM only with enough data | 留出/滚动验证、MAE/RMSE/MAPE/R2、残差图、基线比较 |
| 优化 | 贪心、规则方案、松弛下界/上界、小规模手算 | LP、MILP、DP、网络流、指派/背包、VRP、启发式/元启发式 | 可行性、约束违反表、目标值、基线比较、小规模精确解 |
| 调度 | FIFO、最短加工时间、最近邻 | MILP、CP-SAT、动态规划、遗传算法、模拟退火、禁忌搜索 | 时间窗/容量可行性、延误/成本、基线方案、小规模枚举 |
| 评价 | 等权评分、单指标排序 | 熵权-TOPSIS、AHP、组合赋权、PCA、灰色关联、模糊综合评价 | 指标方向、标准化、权重扰动、排序稳定性、替代权重 |
| 传播 | 指数增长、Logistic | SIR/SEIR、差分方程、元胞自动机、Agent-based simulation | 参数敏感性、峰值/终态、边界案例、重复运行 |
| 空间 | 欧氏距离、最近点、区域均值 | GIS、IDW/Kriging、Voronoi、p-median、最大覆盖、空间聚类 | 坐标/尺度检查、边界效应、距离敏感性、覆盖率 |
| 分类 | 多数类、逻辑回归/简单树 | SVM、随机森林、XGBoost、CNN/迁移学习 only with enough images | 混淆矩阵、准确率/召回率/F1、误判分析、特征贡献 |
| 聚类 | K-means with small K, 人工分组 | K-means、层次聚类、DBSCAN、GMM、谱聚类 | 轮廓系数、CH/DBI、稳定性、簇解释 |
| 文本 | 词频、TF-IDF+线性模型 | LDA、SVM、逻辑回归、随机森林、BERT only with enough labeled data | 主题解释、分类指标、代表性文本、错误样例 |
| 图像 | 手工颜色/纹理/形状特征 | SVM/RF/KNN、轻量 CNN、迁移学习 | 样例可视化、混淆矩阵、误判样例、特征重要性 |

## Route Comparison Fields

For every full problem and single-question deep solution, compare exactly three routes by:

- Fit to the subquestion.
- Assumptions and data demand.
- Interpretability.
- Implementation risk within contest time.
- Validation path.
- Paper expressiveness.

## Method Guardrails

- Do not use TOPSIS/AHP/entropy weighting unless the task is genuinely evaluation/ranking and indicator direction can be checked.
- Do not use neural networks when the sample is small or no validation split is possible.
- Do not force ARIMA when there is no time-series structure.
- Do not use AHP mechanically when there is no expert judgment or pairwise-comparison basis.
- Do not use TOPSIS when indicator direction and normalization are unresolved.
- Do not use metaheuristics when an exact or convex formulation is tractable.
- Benchmark heuristic algorithms against greedy, random, relaxed, or small exact solutions.
- Do not treat simulation output as proof without boundary cases and parameter sensitivity.
- Do not report optimality without solver status, objective value, and constraint violation check.

## Combined Task Routing

Real CUMCM problems often combine task types. Route the combination explicitly.

1. Prediction + optimization:
   - Forecast demand, risk, state, or capacity first, then use forecasts as optimization parameters.
   - Required validation: show how forecast error affects the optimized plan.

2. Evaluation + optimization:
   - Build indicators and weights to produce priorities, then use priorities in resource allocation, sorting, or site selection.
   - Required validation: weight perturbation and ranking/solution stability.

3. Clustering + stratified modeling:
   - Cluster regions, samples, stations, or users, then build differentiated models by group.
   - Required validation: explain cluster meaning and test sensitivity to cluster count or algorithm.

4. Simulation + intervention optimization:
   - Build propagation/evolution simulation, then compare intervention strategies.
   - Required validation: peak, final state, cost, repeated runs, and parameter sensitivity.

5. Spatial analysis + scheduling:
   - Estimate distance/coverage/region structure, then solve allocation, routing, or dispatch.
   - Required validation: coordinate system, distance approximation, boundary cases, and feasibility.

## Per-Question Mapping Template

| 问题 | 输入 | 决策/模型对象 | 输出 | 基线 | 主模型 | 验证 | 图表 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 |  |  |  |  |  |  |  |
| Q2 |  |  |  |  |  |  |  |
| Q3 |  |  |  |  |  |  |  |
