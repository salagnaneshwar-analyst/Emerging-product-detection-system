"""
sentiment.py
Lexicon-based Sentiment Analysis (no paid API, no heavy models)
Uses VADER-style approach with a hand-crafted product-domain lexicon.
"""

import re
import pandas as pd

# ---------------------------------------------------------------------------
# Domain-enriched sentiment lexicon
# ---------------------------------------------------------------------------
POSITIVE_WORDS = {
    "love", "amazing", "excellent", "fantastic", "great", "wonderful", "best",
    "awesome", "brilliant", "perfect", "outstanding", "incredible", "superb",
    "exceptional", "impressed", "obsessed", "changer", "recommend", "exceeded",
    "smooth", "premium", "innovative", "flawless", "intuitive", "solid",
    "worth", "useful", "reliable", "quality", "efficient", "comfortable",
    "sleek", "stylish", "durable", "fast", "easy", "convenient", "top"
}

NEGATIVE_WORDS = {
    "disappointed", "terrible", "horrible", "bad", "poor", "awful", "worst",
    "waste", "useless", "broken", "damaged", "faulty", "cheap", "overpriced",
    "frustrating", "annoying", "mediocre", "gimmick", "regret", "return",
    "stopped", "failed", "confusing", "bugs", "slow", "heavy", "unreliable",
    "uncomfortable", "defective", "scam", "misleading", "boring", "ugly"
}

INTENSIFIERS = {"very", "extremely", "absolutely", "totally", "completely", "so", "really"}
NEGATORS = {"not", "never", "no", "cannot", "cant", "doesnt", "dont", "isnt", "wasnt"}


def score_text(text: str) -> float:
    """Return polarity score in [-1, 1]."""
    if not isinstance(text, str):
        return 0.0

    words = re.sub(r"[^\w\s]", "", text.lower()).split()
    score = 0.0
    for i, word in enumerate(words):
        multiplier = 1.0
        # Check for intensifier before current word
        if i > 0 and words[i - 1] in INTENSIFIERS:
            multiplier = 1.5
        # Check for negator in last 3 words
        window = words[max(0, i - 3): i]
        if any(neg in window for neg in NEGATORS):
            multiplier *= -1

        if word in POSITIVE_WORDS:
            score += 1.0 * multiplier
        elif word in NEGATIVE_WORDS:
            score -= 1.0 * multiplier

    # Normalize
    norm = max(len(words), 1)
    return round(max(-1.0, min(1.0, score / (norm ** 0.5))), 4)


def classify_sentiment(score: float) -> str:
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"


def analyze_sentiment(df: pd.DataFrame, text_col: str = "customer_text") -> pd.DataFrame:
    """Add polarity score and sentiment prediction to DataFrame."""
    df = df.copy()
    df["polarity_score"] = df[text_col].apply(score_text)
    df["predicted_sentiment"] = df["polarity_score"].apply(classify_sentiment)
    return df


def sentiment_summary(df: pd.DataFrame) -> dict:
    """Return summary statistics for sentiment distribution."""
    counts = df["predicted_sentiment"].value_counts().to_dict()
    total = len(df)
    return {
        "positive": counts.get("positive", 0),
        "negative": counts.get("negative", 0),
        "neutral": counts.get("neutral", 0),
        "positive_pct": round(counts.get("positive", 0) / total * 100, 1),
        "negative_pct": round(counts.get("negative", 0) / total * 100, 1),
        "neutral_pct": round(counts.get("neutral", 0) / total * 100, 1),
        "avg_polarity": round(df["polarity_score"].mean(), 4)
    }


def product_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Return mean polarity per product."""
    return (
        df.groupby("product_name")["polarity_score"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "avg_polarity", "count": "mention_count"})
        .sort_values("avg_polarity", ascending=False)
        .reset_index()
    )


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    df = pd.read_csv("data/market_reviews.csv")
    df = analyze_sentiment(df)
    df.to_csv("data/market_reviews_sentiment.csv", index=False)
    print("Sentiment Analysis Complete")
    print(sentiment_summary(df))
    print("\nTop Products by Sentiment:")
    print(product_sentiment(df).head(10))
