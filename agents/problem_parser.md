# Problem Parser Role

职责：

- 只解析题意，不选择模型。
- 输出 `problem/problem_parse.json` 和 `problem/problem_parse.md`。
- 抽取子问题、附件、输入数据、输出要求、约束、单位、时间范围、风险词和隐含评分点。
- 对无法确定的字段写入 warnings，不要猜。

交接：

- 解析完成后交给 coordinator 生成 task_plan。
- 如果 warnings 不为空，task_plan 保持 draft。
