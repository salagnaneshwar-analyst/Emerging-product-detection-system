"""
trends.py
Trend Detection, Growth Scoring, and 3-Month Forecasting
Uses only pandas + numpy — no paid APIs.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# ---------------------------------------------------------------------------
# Helper: resample mentions per product per month
# ---------------------------------------------------------------------------
def monthly_mentions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")
    monthly = (
        df.groupby(["product_name", "month"])
        .size()
        .reset_index(name="mention_count")
    )
    monthly["month_dt"] = monthly["month"].dt.to_timestamp()
    return monthly


# ---------------------------------------------------------------------------
# Growth Score: compare last 3 months vs previous 3 months
# ---------------------------------------------------------------------------
def compute_growth_score(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with growth_score and trend label per product."""
    monthly = monthly_mentions(df)
    monthly = monthly.sort_values(["product_name", "month_dt"])

    max_date = monthly["month_dt"].max()
    recent_cutoff = max_date - pd.DateOffset(months=3)
    prior_cutoff = max_date - pd.DateOffset(months=6)

    results = []
    for product, grp in monthly.groupby("product_name"):
        recent = grp[grp["month_dt"] > recent_cutoff]["mention_count"].sum()
        prior = grp[
            (grp["month_dt"] > prior_cutoff) & (grp["month_dt"] <= recent_cutoff)
        ]["mention_count"].sum()

        if prior == 0:
            growth = 100.0 if recent > 0 else 0.0
        else:
            growth = round((recent - prior) / prior * 100, 1)

        if growth >= 40:
            trend = "🚀 Rapidly Emerging"
        elif growth >= 15:
            trend = "📈 Growing"
        elif growth >= 0:
            trend = "➡️  Stable"
        else:
            trend = "📉 Declining"

        results.append({
            "product_name": product,
            "recent_mentions": int(recent),
            "prior_mentions": int(prior),
            "growth_score_pct": growth,
            "trend_label": trend
        })

    return pd.DataFrame(results).sort_values("growth_score_pct", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Simple linear forecast for next 3 months
# ---------------------------------------------------------------------------
def forecast_product(monthly_grp: pd.DataFrame, months_ahead: int = 3) -> list:
    """Linear regression forecast for a single product."""
    grp = monthly_grp.sort_values("month_dt").reset_index(drop=True)
    x = np.arange(len(grp))
    y = grp["mention_count"].values.astype(float)

    if len(x) < 2:
        slope, intercept = 0.0, float(y[-1]) if len(y) else 0.0
    else:
        slope, intercept = np.polyfit(x, y, 1)

    last_month = grp["month_dt"].iloc[-1]
    forecasts = []
    for i in range(1, months_ahead + 1):
        future_month = last_month + pd.DateOffset(months=i)
        predicted = max(0, intercept + slope * (len(x) + i - 1))
        forecasts.append({
            "month_dt": future_month,
            "mention_count": round(predicted, 1),
            "is_forecast": True
        })
    return forecasts


def full_forecast(df: pd.DataFrame, top_n: int = 10) -> dict:
    """
    For top N products by mention count, produce historical + forecast DataFrame.
    Returns dict: {product_name: combined_df}
    """
    monthly = monthly_mentions(df)
    top_products = (
        df.groupby("product_name").size()
        .sort_values(ascending=False)
        .head(top_n)
        .index.tolist()
    )

    result = {}
    for product in top_products:
        grp = monthly[monthly["product_name"] == product].copy()
        grp["is_forecast"] = False
        future = forecast_product(grp, months_ahead=3)
        future_df = pd.DataFrame(future)
        combined = pd.concat([grp[["month_dt", "mention_count", "is_forecast"]], future_df], ignore_index=True)
        result[product] = combined

    return result


# ---------------------------------------------------------------------------
# Keyword frequency
# ---------------------------------------------------------------------------
def top_keywords(df: pd.DataFrame, text_col: str = "cleaned_text", top_n: int = 30) -> pd.DataFrame:
    from collections import Counter
    all_words = " ".join(df[text_col].dropna()).split()
    freq = Counter(all_words).most_common(top_n)
    return pd.DataFrame(freq, columns=["word", "frequency"])


# ---------------------------------------------------------------------------
# Customer Pain Point Detection
# ---------------------------------------------------------------------------
PAIN_KEYWORDS = {
    "battery", "charge", "overpric", "expens", "broke", "broke", "damage",
    "slow", "lag", "crash", "bug", "poor", "cheap", "return", "refund",
    "complic", "confus", "heavy", "uncomfort", "unreli", "support", "service"
}


def detect_pain_points(df: pd.DataFrame, text_col: str = "cleaned_text") -> pd.DataFrame:
    def has_pain(text):
        if not isinstance(text, str):
            return False
        return any(kw in text for kw in PAIN_KEYWORDS)

    pain_df = df[df[text_col].apply(has_pain)].copy()
    if pain_df.empty:
        return pd.DataFrame(columns=["product_name", "pain_count"])

    return (
        pain_df.groupby("product_name")
        .size()
        .reset_index(name="pain_count")
        .sort_values("pain_count", ascending=False)
    )


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv("data/market_reviews_clean.csv")

    growth = compute_growth_score(df)
    print("=== Growth Scores ===")
    print(growth.head(10).to_string(index=False))

    pain = detect_pain_points(df)
    print("\n=== Customer Pain Points ===")
    print(pain.head(10).to_string(index=False))
