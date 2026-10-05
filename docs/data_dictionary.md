# Data dictionary

| Field | Type | Definition |
|---|---|---|
| `state_code` | text | Two-digit INEGI/SNIIV entity code |
| `state` | text | Federal entity name |
| `housing_backlog_units` | integer | Housing units classified as in housing backlog |
| `housing_without_backlog_units` | integer | Housing units not classified as in backlog |
| `total_housing_units` | integer | Sum of units with and without backlog |
| `backlog_rate_pct` | decimal | Backlog units as percentage of total housing units |
| `need_volume_index` | decimal | Min-max normalized backlog volume |
| `need_rate_index` | decimal | Min-max normalized backlog rate |
| `market_scale_index` | decimal | Min-max normalized total housing stock |
| `opportunity_score` | decimal | Weighted housing-need screening score, 0–100 |
| `rank` | integer | Descending rank by opportunity score |
| `market_segment` | text | Median-based strategic segment |
