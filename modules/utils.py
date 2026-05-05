"""
utils.py
Shared utility functions for the Emerging Products NLP project.
"""

import os
import io
import base64
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------
def load_csv(path: str) -> pd.DataFrame:
    """Load CSV with basic validation."""
    required_cols = {"date", "customer_text", "product_name", "product_category"}
    df = pd.read_csv(path)
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    df["date"] = pd.to_datetime(df["date"])
    return df


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------------------
# Business insight generator
# ---------------------------------------------------------------------------
def generate_insights(growth_df: pd.DataFrame, sentiment_df: pd.DataFrame = None) -> list:
    """
    Auto-generate human-readable business insights from growth scores.
    """
    insights = []
    for _, row in growth_df.head(5).iterrows():
        p = row["product_name"]
        g = row["growth_score_pct"]
        t = row["trend_label"]
        if g > 40:
            insights.append(
                f"🚀 {p} demand is surging with {g:.0f}% growth — early launch recommended."
            )
        elif g > 15:
            insights.append(
                f"📈 {p} shows steady {g:.0f}% growth — strong market interest building."
            )
        elif g >= 0:
            insights.append(
                f"➡️  {p} is maintaining stable market presence."
            )
        else:
            insights.append(
                f"⚠️  {p} mentions declined {abs(g):.0f}% — monitor closely."
            )
    return insights


# ---------------------------------------------------------------------------
# Word cloud data (frequencies dict)
# ---------------------------------------------------------------------------
def word_cloud_data(df: pd.DataFrame, text_col: str = "cleaned_text") -> dict:
    from collections import Counter
    all_words = " ".join(df[text_col].dropna()).split()
    freq = Counter(all_words)
    # Remove very common filler words
    remove = {"product", "got", "get", "just", "also", "even", "still"}
    for w in remove:
        freq.pop(w, None)
    return dict(freq.most_common(80))


# ---------------------------------------------------------------------------
# KPI summary
# ---------------------------------------------------------------------------
def compute_kpis(df: pd.DataFrame) -> dict:
    total_reviews = len(df)
    unique_products = df["product_name"].nunique()
    unique_categories = df["product_category"].nunique()

    pos = (df["predicted_sentiment"] == "positive").sum() if "predicted_sentiment" in df.columns else 0
    pos_pct = round(pos / total_reviews * 100, 1) if total_reviews else 0

    return {
        "total_reviews": total_reviews,
        "unique_products": unique_products,
        "unique_categories": unique_categories,
        "positive_sentiment_pct": pos_pct,
    }


# ---------------------------------------------------------------------------
# CSV download helper (returns bytes)
# ---------------------------------------------------------------------------
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")
