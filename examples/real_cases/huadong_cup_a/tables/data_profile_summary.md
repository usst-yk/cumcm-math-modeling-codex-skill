# 数据检查报告

## 数据表概览

| file | sheet | rows | columns | time_columns | included_status |
| --- | --- | --- | --- | --- | --- |
| benchmark_activities.csv | benchmark_activities | 19 | 16 | time_window_start; time_window_end; wait_workday; wait_holiday | to_review |
| realtime_wait_updates.csv | realtime_wait_updates | 30 | 4 | day_type | to_review |

## 缺失值概览

| file | sheet | column | missing_count | missing_ratio |
| --- | --- | --- | --- | --- |
| benchmark_activities.csv | benchmark_activities | time_window_start | 14 | 0.7368421052631579 |
| benchmark_activities.csv | benchmark_activities | time_window_end | 14 | 0.7368421052631579 |

## 异常值概览

| file | sheet | column | iqr_outliers |
| --- | --- | --- | --- |
| benchmark_activities.csv | benchmark_activities | x_m | 2 |
| benchmark_activities.csv | benchmark_activities | y_m | 1 |
| benchmark_activities.csv | benchmark_activities | utility_family | 4 |
| benchmark_activities.csv | benchmark_activities | utility_couple | 1 |
