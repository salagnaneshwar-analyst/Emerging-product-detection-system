"""
train.py
End-to-end pipeline: preprocess → sentiment → trends → export outputs.
Run this once before launching the Streamlit dashboard.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from modules.preprocess import preprocess_dataframe
from modules.sentiment import analyze_sentiment, sentiment_summary, product_sentiment
from modules.trends import compute_growth_score, top_keywords, detect_pain_points, full_forecast
from modules.utils import ensure_dir, generate_insights


def run_pipeline(input_path: str = "data/market_reviews.csv"):
    print("=" * 60)
    print("  Emerging Products NLP Pipeline")
    print("=" * 60)

    ensure_dir("outputs")
    ensure_dir("models")

    # -----------------------------------------------------------
    # 1. Load raw data
    # -----------------------------------------------------------
    print("\n[1/5] Loading data...")
    df = pd.read_csv(input_path)
    df["date"] = pd.to_datetime(df["date"])
    print(f"      Loaded {len(df)} records.")

    # -----------------------------------------------------------
    # 2. Preprocess
    # -----------------------------------------------------------
    print("[2/5] Preprocessing text...")
    df = preprocess_dataframe(df, text_col="customer_text")
    df.to_csv("data/market_reviews_clean.csv", index=False)
    print("      Saved: data/market_reviews_clean.csv")

    # -----------------------------------------------------------
    # 3. Sentiment Analysis
    # -----------------------------------------------------------
    print("[3/5] Running sentiment analysis...")
    df = analyze_sentiment(df, text_col="customer_text")
    summary = sentiment_summary(df)
    prod_sent = product_sentiment(df)
    df.to_csv("data/market_reviews_sentiment.csv", index=False)
    prod_sent.to_csv("outputs/product_sentiment.csv", index=False)
    print(f"      Positive: {summary['positive_pct']}%  "
          f"Negative: {summary['negative_pct']}%  "
          f"Neutral: {summary['neutral_pct']}%")

    # -----------------------------------------------------------
    # 4. Trend & Growth Scoring
    # -----------------------------------------------------------
    print("[4/5] Computing trend growth scores...")
    growth = compute_growth_score(df)
    growth.to_csv("outputs/growth_scores.csv", index=False)

    keywords = top_keywords(df, text_col="cleaned_text", top_n=40)
    keywords.to_csv("outputs/top_keywords.csv", index=False)

    pain = detect_pain_points(df, text_col="cleaned_text")
    pain.to_csv("outputs/pain_points.csv", index=False)

    print("\n      Top 5 Emerging Products:")
    for _, row in growth.head(5).iterrows():
        print(f"        {row['trend_label']}  {row['product_name']}  "
              f"({row['growth_score_pct']:+.1f}%)")

    # -----------------------------------------------------------
    # 5. Business Insights
    # -----------------------------------------------------------
    print("\n[5/5] Generating business insights...")
    insights = generate_insights(growth)
    for ins in insights:
        print(f"      {ins}")

    insights_df = pd.DataFrame({"insight": insights})
    insights_df.to_csv("outputs/business_insights.csv", index=False)

    print("\n" + "=" * 60)
    print("  Pipeline complete. All outputs saved to /outputs/")
    print("  Run:  streamlit run app.py   to launch dashboard.")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
