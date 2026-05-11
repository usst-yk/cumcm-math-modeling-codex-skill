# Task Plan

| ID | Type | Output | Baseline | Primary | Validation |
| --- | --- | --- | --- | --- | --- |
| Q1 | mechanism_modeling | 单光束干涉频率-厚度公式 | 相邻峰间距公式 | 光谱频率模型 | 单位与角度校验 |
| Q2 | signal_inverse | 两组光谱厚度估计 | 峰间距估计 | 最小二乘频率拟合 | 已知真值误差、角度一致性、FFT 对照 |

## Benchmark Target

本案例的真值为 `8.000 um`。通过条件为：

```text
max(abs(estimated_thickness_um - 8.000)) <= 0.050 um
```

## Selling Point

这个案例把 B 题的核心物理模型变成可重复回归测试：每次修改 skill 或脚本后，
都能重新运行代码并检查估计厚度是否仍然接近已知真值。
