# Power BI dashboard specification

Import `data/processed/powerbi_market_table.csv` as `Market`.

## Recommended pages

### 1. Executive overview

- KPI: total backlog units
- KPI: national backlog rate
- KPI: number of priority-need markets
- Horizontal bar: opportunity score by state (Top N = 10)
- Scatter: total units vs backlog rate; bubble size = backlog units; legend = segment
- Slicer: market segment

### 2. State explorer

- Filled map using `state`
- Matrix with rank, backlog units, backlog rate, total units and score
- Drill-through tooltip with state metrics

## DAX measures

```DAX
Total Backlog = SUM(Market[housing_backlog_units])

Total Housing = SUM(Market[total_housing_units])

National Backlog Rate = DIVIDE([Total Backlog], [Total Housing])

Priority Markets =
CALCULATE(
    DISTINCTCOUNT(Market[state]),
    Market[market_segment] = "Priority need markets"
)

Average Opportunity Score = AVERAGE(Market[opportunity_score])
```

Format `National Backlog Rate` as a percentage with one decimal. Use conditional formatting on `opportunity_score`, but keep the score's label explicit: it measures housing need, not investment return.
