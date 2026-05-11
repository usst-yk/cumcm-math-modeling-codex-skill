# Q1 Modeling Idea

## 本问作用

问题一建立男胎 Y 染色体浓度与孕周、BMI、年龄和 GC 含量之间的可解释模型，为后续 BMI 分组检测时点优化提供浓度预测函数和达标阈值依据。

## 模型

输入为男胎样本的孕周、BMI、年龄、GC 含量和 Y 染色体浓度，输出为浓度预测值、拟合指标和达到 4% 阈值的解释路径。主模型为加性线性回归，保留变量方向可解释性：孕周提高浓度，BMI 增大可能降低相对胎儿 DNA 浓度，GC 和年龄作为质量与个体差异控制变量。

## 求解

`src/solve_nipt_supervised.py` 生成受控数据、拟合线性模型、输出 `tables/tab_q1_fit_metrics.csv` 和 `tables/tab_q1_model_coefficients.csv`，并绘制 `figures/fig_q1_result.png` 与 `figures/fig_q1_validation.png`。`figures/fig_q1_model_flow.png` 表达从输入变量到阈值周数判断的流程。

## 验证

验证包括拟合优度、平均绝对误差、残差分布和阈值线解释。该受控案例只验证工作流，不把拟合指标解释为真实临床性能。

## 代码反向验证与最终思路

代码实际使用的变量、回归公式、阈值和残差图与最终思路一致。最终思路是用简单可解释模型支撑时点优化，而不是追求复杂黑箱预测。
