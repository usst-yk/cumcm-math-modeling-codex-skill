# CUMCM 2025 B 题合成光谱回归案例

本目录用于测试 2025 年国赛 B 题“碳化硅外延层厚度的确定”的代码执行与结果准确性。

这个案例不是官方标准答案，也不复刻官方附件。它使用 B 题的核心数据结构
（波数-反射率光谱），生成真实厚度已知的合成附件，再运行厚度反演算法。
这样可以明确判断代码是否准确：估计厚度必须接近 `8.000 um`。

## 来源

- 官方赛题页：https://www.mcm.edu.cn/html_cn/node/03c91a444e62eee81a3740fa97a461a6.html
- B 题 PDF 镜像：https://col.gxmzu.edu.cn/mathmod/UploadFiles/B%E9%A2%98.pdf

## 已放入的内容

| Path | 内容 |
| --- | --- |
| `problem/problem_statement.pdf` | B 题题面 PDF 镜像。 |
| `problem/problem_statement.md` | 面向本 benchmark 的题面摘要和测试目标。 |
| `problem/problem_parse.json` | 结构化题面解析。 |
| `problem/task_plan.json` | 含 benchmark、rubric、selling point 和 revision 字段的任务计划。 |
| `src/solve_sic_thickness.py` | 生成合成光谱并反演厚度的完整脚本。 |
| `data/raw/sic_10deg_synthetic.csv` | 10 deg 合成波数-反射率数据，运行脚本后生成。 |
| `data/raw/sic_15deg_synthetic.csv` | 15 deg 合成波数-反射率数据，运行脚本后生成。 |
| `tables/tab_q2_thickness.csv` | 两组光谱厚度估计和误差。 |
| `tables/tab_q2_reliability.csv` | 真值回归与角度一致性验证。 |
| `figures/fig_q1_model_schematic.png` | 单光束干涉厚度模型示意图。 |
| `figures/fig_q2_model_schematic.png` | 反演算法流程图。 |
| `figures/fig_q2_result.png` | 两组光谱与峰值检测结果。 |
| `figures/fig_q2_validation.png` | 估计厚度与合成验证误差图。 |
| `figures/fig_sensitivity.png` | 折射率和入射角敏感性分析图。 |
| `tables/tab_sensitivity.csv` | 折射率和入射角扰动下的厚度变化表。 |
| `results/result_registry.csv` | 核心数值来源登记。 |
| `results/validation_report.md` | 验证报告。 |
| `paper/main.tex` | 轻量论文入口，运行脚本后刷新。 |
| `paper/main.pdf` | 交付包内的最新版编译论文 PDF。 |
| `progress.html` | 返工闭环与子 agent 工作进度面板。 |

## 运行

在本目录运行：

```powershell
python src/solve_sic_thickness.py
```

从仓库根目录运行完整审计：

```powershell
python scripts/validate_results.py --project examples/real_cases/cumcm_2025_b --mode full --output examples/real_cases/cumcm_2025_b/results/validation_audit.md
python scripts/run_skill_evals.py
```

## Benchmark 结果

通过标准：

```text
abs(estimated_thickness_um - 8.000000) <= 0.050000
```

脚本会生成两组入射角结果，并在 `tables/tab_q2_reliability.csv` 中记录最大绝对误差。

## 当前限制

- 合成光谱只用于代码准确性回归，不等同于官方附件求解。
- 折射率固定为 `n = 2.55`，没有展开载流子浓度和波长相关折射率。
- 多光束干涉只作为风险记录，没有在本轻量案例中求解。

## 交付说明

发给作者的压缩包中，`paper/main.pdf` 使用本轮返工后重新编译的 PDF；本地目录里的
`paper/main_reworked.pdf` 是同一份新 PDF 的工作副本。压缩包不会包含 TeX 编译软件、
Python 缓存或 LaTeX 中间文件。
