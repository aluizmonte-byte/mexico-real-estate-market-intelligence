# Methodology

## Business question

Which Mexican states combine the greatest housing need, the highest need intensity and sufficient market scale to deserve deeper commercial evaluation by a developer, housing-finance provider or real-estate services company?

## Source and unit of analysis

The core dataset is the 2024 state-level **Rezago habitacional** file published by SNIIV, Mexico's National Housing Information System (SEDATU). The file covers all 32 federal entities and reports housing units with and without backlog. The analysis was retrieved and reproduced on 5 October 2026.

`total_housing_units = housing_backlog_units + housing_without_backlog_units`

`backlog_rate_pct = housing_backlog_units / total_housing_units × 100`

## Housing Need Opportunity Score

Each component is min-max normalized across the 32 states.

| Component | Weight | Business meaning |
|---|---:|---|
| Backlog units | 45% | Absolute addressable need |
| Backlog rate | 35% | Intensity of unmet housing conditions |
| Total housing units | 20% | Scale of the state housing market |

`score = 100 × (0.45 × volume_index + 0.35 × rate_index + 0.20 × scale_index)`

Weights are explicit managerial assumptions. They are designed for market screening, not causal inference or investment valuation.

## Segmentation

States are classified using the national medians of backlog units and backlog rate:

- **Priority need markets:** above both medians.
- **Scale-led markets:** high backlog volume, lower backlog rate.
- **High-rate niche markets:** high backlog rate, lower volume.
- **Lower-priority markets:** below both medians.

## Limitations

- Backlog is a social-need measure, not proof of effective demand or purchasing power.
- State-level averages hide differences among municipalities and metropolitan areas.
- The score does not include land prices, housing prices, inventory, absorption, regulation, income, credit approval or project economics.
- SHF's 2026 demand and price indicators are national context and do not enter the state score.
- A high score means “investigate further”, not “invest immediately”.
