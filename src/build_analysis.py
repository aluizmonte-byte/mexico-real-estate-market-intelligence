from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "rezago_habitacional_2024.csv"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"


def minmax(series: pd.Series) -> pd.Series:
    span = series.max() - series.min()
    return (series - series.min()) / span if span else pd.Series(0.0, index=series.index)


def build_dataset() -> pd.DataFrame:
    df = pd.read_csv(RAW, dtype={"state_code": str})
    df["total_housing_units"] = df["housing_backlog_units"] + df["housing_without_backlog_units"]
    df["backlog_rate_pct"] = 100 * df["housing_backlog_units"] / df["total_housing_units"]

    # The score prioritizes need, while retaining market scale as a commercial lens.
    df["need_volume_index"] = minmax(df["housing_backlog_units"])
    df["need_rate_index"] = minmax(df["backlog_rate_pct"])
    df["market_scale_index"] = minmax(df["total_housing_units"])
    df["opportunity_score"] = 100 * (
        0.45 * df["need_volume_index"]
        + 0.35 * df["need_rate_index"]
        + 0.20 * df["market_scale_index"]
    )
    df["opportunity_score"] = df["opportunity_score"].round(1)
    df["backlog_rate_pct"] = df["backlog_rate_pct"].round(1)
    df["rank"] = df["opportunity_score"].rank(method="first", ascending=False).astype(int)

    volume_median = df["housing_backlog_units"].median()
    rate_median = df["backlog_rate_pct"].median()
    df["market_segment"] = np.select(
        [
            (df["housing_backlog_units"] >= volume_median) & (df["backlog_rate_pct"] >= rate_median),
            (df["housing_backlog_units"] >= volume_median) & (df["backlog_rate_pct"] < rate_median),
            (df["housing_backlog_units"] < volume_median) & (df["backlog_rate_pct"] >= rate_median),
        ],
        ["Priority need markets", "Scale-led markets", "High-rate niche markets"],
        default="Lower-priority markets",
    )
    return df.sort_values("rank").reset_index(drop=True)


def save_charts(df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid", font_scale=0.9)
    palette = {"Priority need markets": "#C23B22", "Scale-led markets": "#33658A",
               "High-rate niche markets": "#F6AE2D", "Lower-priority markets": "#86BBD8"}

    top = df.head(10).sort_values("opportunity_score")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [palette[x] for x in top["market_segment"]]
    ax.barh(top["state"], top["opportunity_score"], color=colors)
    for i, value in enumerate(top["opportunity_score"]):
        ax.text(value + 0.8, i, f"{value:.1f}", va="center", fontweight="bold")
    ax.set(xlabel="Housing Need Opportunity Score (0–100)", ylabel="", title="Mexico: priority markets by housing need")
    ax.set_xlim(0, 105)
    sns.despine()
    fig.tight_layout()
    fig.savefig(FIGURES / "opportunity_ranking.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 7))
    for segment, group in df.groupby("market_segment"):
        ax.scatter(group["total_housing_units"], group["backlog_rate_pct"],
                   s=np.sqrt(group["housing_backlog_units"]) * 2.2,
                   alpha=0.76, label=segment, color=palette[segment], edgecolor="white")
    for _, row in df.head(10).iterrows():
        ax.annotate(row["state"], (row["total_housing_units"], row["backlog_rate_pct"]),
                    xytext=(5, 5), textcoords="offset points", fontsize=8)
    ax.axvline(df["total_housing_units"].median(), color="#777", linestyle="--", linewidth=1)
    ax.axhline(df["backlog_rate_pct"].median(), color="#777", linestyle="--", linewidth=1)
    ax.set(xlabel="Total housing units", ylabel="Housing backlog rate (%)",
           title="Need intensity vs. market scale (bubble = backlog units)")
    ax.ticklabel_format(style="plain", axis="x")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    sns.despine()
    fig.tight_layout()
    fig.savefig(FIGURES / "need_scale_matrix.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_summary(df: pd.DataFrame) -> None:
    top = df.head(5)
    national_backlog = int(df["housing_backlog_units"].sum())
    national_total = int(df["total_housing_units"].sum())
    rate = 100 * national_backlog / national_total
    ranking = "\n".join(
        f"{int(r.rank)}. **{r.state}** — score {r.opportunity_score:.1f}; "
        f"{int(r.housing_backlog_units):,} homes; {r.backlog_rate_pct:.1f}% rate"
        for r in top.itertuples()
    )
    text = f"""# Executive summary

Mexico had **{national_backlog:,} housing units in backlog**, equivalent to **{rate:.1f}%** of the {national_total:,} housing units represented in the official 2024 SNIIV dataset.

## Top priority markets

{ranking}

## Commercial interpretation

The ranking identifies where housing need is simultaneously large, intense and commercially significant. It is a **prioritization lens**, not an investment-return forecast. Before committing capital, decision-makers should add land costs, local regulation, household income, prices, absorption and financing conditions.

Veracruz and Chiapas lead because need is both very large and widespread. Oaxaca, Tabasco and Guerrero combine a high backlog rate with meaningful volume. Estado de México appears as a scale-led opportunity: its rate is lower, but the absolute unmet need and size of the housing stock remain substantial.

## National market context

SHF estimated **864,290 housing financings for 2026**, with 42.94% directed to improvements and 28.54% to new or used home acquisition. Separately, the SHF Home Price Index reported **7.3% annual appreciation in Q2 2026**. These national indicators provide context only and are not used in the state score.
"""
    (ROOT / "reports" / "executive_summary.md").write_text(text, encoding="utf-8")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    df = build_dataset()
    df.to_csv(PROCESSED / "state_housing_opportunity.csv", index=False)
    df[["state_code", "state", "housing_backlog_units", "housing_without_backlog_units",
        "total_housing_units", "backlog_rate_pct", "opportunity_score", "rank", "market_segment"]].to_csv(
        PROCESSED / "powerbi_market_table.csv", index=False
    )
    save_charts(df)
    save_summary(df)
    print(df.head(10)[["rank", "state", "opportunity_score", "housing_backlog_units", "backlog_rate_pct"]].to_string(index=False))


if __name__ == "__main__":
    main()
