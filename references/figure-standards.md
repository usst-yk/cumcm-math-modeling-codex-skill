# CUMCM代码绘图规范

## 总原则

代码生成的图必须服务论文结论，而不是展示过程。每张图都应满足：

- 回答一个明确子问题。
- 数据、参数和处理步骤可追溯。
- 坐标轴、单位、图例和标题完整。
- 由代码一键生成，不手工修改数值。
- 能直接放入论文正文或附录。

## 输出要求

- 默认输出到 `figures/` 文件夹。
- 每张核心图至少保存一份高分辨率位图：`.png`，建议 `dpi=300` 或更高。
- 重要论文图同时保存矢量格式：`.pdf` 或 `.svg`。
- 文件名使用可追踪命名：`fig_q1_demand_forecast.png`、`fig_q2_topsis_ranking.pdf`、`fig_q3_sensitivity_beta.png`。
- 不要使用 `output.png`、`test.jpg`、`new figure.png` 这类不可追踪文件名。
- 代码中集中设置随机种子、字体、字号、颜色和保存路径。

## 图形选择

- 趋势变化：折线图，必要时带置信区间或误差带。
- 排名比较：水平条形图，按数值排序。
- 类别占比：优先条形图或堆叠条形图，少用饼图。
- 相关关系：散点图、回归线、相关系数热力图。
- 误差分析：残差图、误差分布直方图、箱线图、真实值-预测值散点图。
- 灵敏度分析：参数-结果折线图、热力图或 tornado 图。
- 空间分布：地图、网格热力图、等值线图或空间散点图。
- 网络结构：节点-边图、中心性排名图、社团划分图。
- 解析与数值比较：同轴折线图、误差曲线、参数区间对比图。

避免：

- 3D 饼图、无意义 3D 柱状图。
- 过度渐变、阴影、装饰性背景。
- 只靠颜色区分类别而无标记、线型或标签。
- 图例遮挡关键数据。
- 一个图塞入过多曲线导致无法阅读。

## 版式与可读性

- 中文论文推荐优先使用系统可用中文字体；若字体不可用，代码应优雅回退。
- 英文、数字、符号保持统一字体风格。
- 正文字号通常不小于 9 pt；坐标轴标签、图例和注释必须清晰可读。
- 坐标轴标签必须带单位，例如 `时间 / h`、`成本 / 元`、`浓度 / mg/L`。
- 小数位保持一致；避免展示超过结论需要的有效数字。
- 图例放在空白区域或图外，不能遮挡数据。
- 多子图使用 `(a)`, `(b)`, `(c)` 标注，并在图注中解释。
- 颜色应适合灰度打印；关键类别同时使用不同线型、标记或纹理。

## Python 绘图默认建议

使用 matplotlib/seaborn 时：

```python
from pathlib import Path
import matplotlib.pyplot as plt

FIG_DIR = Path("figures")
FIG_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "axes.unicode_minus": False,
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
})

fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
# plot data here
ax.set_xlabel("时间 / h")
ax.set_ylabel("需求量 / 件")
ax.grid(True, alpha=0.25)
fig.savefig(FIG_DIR / "fig_q1_demand_forecast.png", bbox_inches="tight")
fig.savefig(FIG_DIR / "fig_q1_demand_forecast.pdf", bbox_inches="tight")
```

如需中文字体，先检测本机字体；不要硬编码只有自己电脑存在的字体路径。若中文显示不稳定，可在论文中使用英文坐标标签，正文图注用中文解释。

## MATLAB 绘图默认建议

使用 MATLAB 时：

```matlab
if ~exist('figures', 'dir')
    mkdir('figures');
end

figure('Color','w','Position',[100 100 720 480]);
plot(x, y, 'LineWidth', 1.5);
grid on;
xlabel('时间 / h');
ylabel('需求量 / 件');
set(gca, 'FontSize', 10, 'LineWidth', 1);
exportgraphics(gcf, 'figures/fig_q1_demand_forecast.png', 'Resolution', 300);
exportgraphics(gcf, 'figures/fig_q1_demand_forecast.pdf', 'ContentType', 'vector');
```

## 图注写法

每次生成图时，必须同时输出一段可直接放入论文正文的中文图注或解释。不要只给图片文件路径或代码结果。

图注应包含：

- 图中展示什么对象和变量。
- 关键趋势、差异或异常。
- 该图支持哪个子问题的结论。
- 如有解析/数值比较，说明两者一致性或偏差来源。

推荐格式：

```text
图 X 展示了……。可以看出，……；这说明……。该结果用于回答问题 X 中关于……的要求。若与解析模型比较，……，偏差主要来源于……。
```

示例：

图 3 展示了参数 beta 在不同取值下目标函数值的变化。可以看出，当 beta 小于 0.6 时，数值优化结果与解析近似曲线基本一致，说明简化模型能够解释主要趋势；当 beta 继续增大后，两者偏差扩大，主要原因是容量约束开始成为主导因素。

如果生成多张图，应逐张给出图注：

- `fig_q1_demand_forecast.png`：图 X 展示了……
- `fig_q2_topsis_ranking.png`：图 X 展示了……
- `fig_q3_sensitivity_beta.png`：图 X 展示了……

## 最终检查

- 文件名能看出对应问题和图形含义。
- 图中所有轴都有单位。
- 图例不遮挡数据。
- 图中数值和论文正文一致。
- 图能在黑白打印下区分主要类别。
- 图注解释了结论，而不是只重复图名。
- 每次输出图像文件时，同时输出论文可用图注。
- 生成图的代码随附在 `src/` 或附录中，能重新生成图片。
