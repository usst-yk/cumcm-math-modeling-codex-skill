# Q3 Modeling Idea

## 本问作用

问题三面向女胎样本建立异常风险判定模型。由于女胎不能依赖 Y 染色体浓度，必须从染色体 Z 值、X 染色体偏离、GC 偏离和个体变量中构造筛查型风险评分。

## 模型

输入为女胎样本的 Z13、Z18、Z21、X 染色体偏离、GC 含量、年龄和 BMI，输出为异常概率、分类阈值和判别指标。主模型为 Logistic 风险评分，阈值选择偏向筛查任务中的灵敏度要求，同时报告 AUC、灵敏度、特异度和混淆矩阵。

## 求解

`src/solve_nipt_supervised.py` 标准化特征并拟合 Logistic 模型，保存 `tables/tab_q3_classification.csv`，生成 `figures/fig_q3_result.png` 和 `figures/fig_q3_validation.png`。`figures/fig_q3_model_flow.png` 说明从多指标特征到风险评分和异常判定的流程。

## 验证

验证包括 ROC 曲线、AUC、混淆矩阵、灵敏度和特异度。由于这是受控数据，结论只证明建模链路和验证方式可复核，不给出真实医学诊断承诺。

## 代码反向验证与最终思路

代码实际使用的特征构造、标准化、Logistic 训练、阈值判定和验证指标与最终思路一致。最终思路是用多指标风险评分替代单指标硬阈值，并在论文中说明筛查阈值的取舍。
