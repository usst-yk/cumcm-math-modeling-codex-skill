# Code To Paper

代码不是最终交付，论文才是最终交付。每次运行脚本后执行这几个动作：

1. 确认输入数据、单位、随机种子和求解状态。
2. 保存结果表到 `tables/`。
3. 保存结果图、验证图和 GPT-image 流程图到 `figures/`。
4. 把关键数字和验证结论写入 `results/validation_report.md`。
5. 更新 `modeling/qx_modeling_idea.md` 的“代码反向验证与最终思路”。
6. 更新 `paper/main.tex` 对应问题的分析、模型、求解、结果和验证。

论文不得描述代码没有实现的模型；代码也不得产生论文没有解释的关键结论。
