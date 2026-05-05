"""
preprocess.py
NLP Preprocessing Pipeline for Emerging Product Detection
"""

import re
import string
import pandas as pd


# ---------------------------------------------------------------------------
# Stopwords (no NLTK dependency – built-in list)
# ---------------------------------------------------------------------------
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "he", "him", "his", "she", "her", "hers",
    "it", "its", "they", "them", "their", "what", "which", "who", "this",
    "that", "these", "those", "am", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "dare", "ought", "used", "a", "an", "the", "and", "but", "if", "or",
    "because", "as", "until", "while", "of", "at", "by", "for", "with",
    "about", "against", "between", "into", "through", "during", "before",
    "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once",
    "very", "just", "also", "so", "too", "not", "no", "nor"
}

# Simple rule-based lemmatizer suffix map
SUFFIX_MAP = {
    "ies": "y", "ied": "y", "ing": "", "ness": "",
    "tion": "te", "sion": "se", "ed": "", "er": "", "est": "",
    "ly": "", "ful": "", "less": "", "ment": ""
}


def simple_lemmatize(word: str) -> str:
    """Rule-based suffix stripping (lightweight lemmatization)."""
    if len(word) <= 4:
        return word
    for suffix, replacement in SUFFIX_MAP.items():
        if word.endswith(suffix) and len(word) - len(suffix) > 2:
            return word[: len(word) - len(suffix)] + replacement
    return word


def clean_text(text: str) -> str:
    """Full NLP preprocessing pipeline."""
    if not isinstance(text, str):
        return ""
    # 1. Lowercase
    text = text.lower()
    # 2. Remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)
    # 3. Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # 4. Remove digits
    text = re.sub(r"\d+", "", text)
    # 5. Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list:
    """Split cleaned text into tokens."""
    return text.split()


def remove_stopwords(tokens: list) -> list:
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def lemmatize_tokens(tokens: list) -> list:
    return [simple_lemmatize(t) for t in tokens]


def preprocess(text: str) -> str:
    """Full pipeline → returns cleaned string."""
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize_tokens(tokens)
    return " ".join(tokens)


def preprocess_dataframe(df: pd.DataFrame, text_col: str = "customer_text") -> pd.DataFrame:
    """Apply preprocessing to a DataFrame column."""
    df = df.copy()
    df["cleaned_text"] = df[text_col].apply(preprocess)
    return df


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample = "I absolutely love my new Smart Ring! It changed my daily routine completely."
    print("Original :", sample)
    print("Processed:", preprocess(sample))

    df = pd.read_csv("data/market_reviews.csv")
    df = preprocess_dataframe(df)
    df.to_csv("data/market_reviews_clean.csv", index=False)
    print(f"\nPreprocessed dataset saved. Shape: {df.shape}")
    print(df[["customer_text", "cleaned_text"]].head(3))
