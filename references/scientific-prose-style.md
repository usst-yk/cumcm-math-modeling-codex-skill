# Scientific Prose Style

This reference defines paper-facing prose checks used by the style gate and
polishing roles.

## Result-First Paragraphs

A strong modeling-paper paragraph usually contains:

- the modeling object or decision variable;
- the data range or scenario;
- the method or equation being applied;
- the key number or trend;
- the interpretation and limitation.

Avoid paragraphs that only say the model was built and results were obtained.
The reader should know what changed, why it changed, and how the figure or table
supports the claim.

## Decimals

Long decimals make a contest paper look like raw program output. Unless the
problem requires high precision, round prose numbers to a small number of
meaningful digits and keep table precision consistent within each column.

Style-gate warning: decimals with more than four digits after the decimal point
should be reviewed.

## Units

Use paper-ready units. Raw `um` and `deg` usually indicate exported labels or
unpolished captions. Prefer TeX or Chinese unit expressions such as
`\mu m`, `\mathrm{\mu m}`, `度`, or `^\circ`, depending on the surrounding
notation.

## Template Phrases

Template phrases should be replaced with concrete model content. Common weak
phrases include:

- `具有重要意义`
- `为相关研究提供参考`
- `本文建立模型并求解`
- `结果表明模型有效`
- `综上所述`
- `具有较好的鲁棒性`
- `具有一定的参考价值`

The phrase is acceptable only when the same sentence or nearby text names the
object, metric, evidence, and boundary.

## Captions

A useful caption names the object, variable, unit, condition, and conclusion.
It should help the reader understand why the figure exists without reading the
whole paragraph again.

Weak captions:

- `结果图`
- `模型结果`
- `对比图`
- `流程图`
- `仿真结果`

Stronger pattern:

`不同调度策略下平均等待时间的变化，单位为 min；红色方案在高峰需求下将等待时间降低约 12%。`

## Benchmark Reports

Benchmark reports may retain internal terms, but their prose should still be
edited. A readable benchmark report separates:

- what was tested;
- what evidence was collected;
- what failed or passed;
- what paper-facing change follows from the evidence.
