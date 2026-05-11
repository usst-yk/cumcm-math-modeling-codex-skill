# Problem Parse

## Facts

- 题目：2025 CUMCM B 题，碳化硅外延层厚度的确定。
- 数据形态：波数 `cm^-1` 与反射率 `%` 的一维光谱曲线。
- 本案例使用合成数据，真实厚度为 `8.000 um`。
- 两组入射角：`10 deg` 与 `15 deg`。

## Subquestions

| ID | Type | Required output | Validation |
| --- | --- | --- | --- |
| Q1 | mechanism_modeling | 单光束干涉厚度模型 | 单位、角度和公式一致性 |
| Q2 | signal_inverse | 由两组合成光谱反演厚度 | `abs(error) <= 0.050 um` |

## Risks

- 单位换算错误会造成 10000 倍量级偏差。
- 峰值间距法需要和频率拟合法互相校验。
- 本案例不是官方附件复现，结论不能写成 B 题标准答案。
