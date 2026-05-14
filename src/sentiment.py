"""Baseline sentiment analysis helpers for bank app reviews."""

from __future__ import annotations

import hashlib
import re
from typing import Any

import pandas as pd

from src.config import ANALYSIS_COLUMNS

TOKEN_PATTERN = re.compile(r"[a-zA-Z']+")
POSITIVE_WORDS = {
    "amazing",
    "awesome",
    "best",
    "easy",
    "excellent",
    "fast",
    "good",
    "great",
    "helpful",
    "love",
    "nice",
    "perfect",
    "quick",
    "reliable",
    "smooth",
    "useful",
}
NEGATIVE_WORDS = {
    "bad",
    "bug",
    "crash",
    "crashes",
    "delay",
    "error",
    "fail",
    "failed",
    "freezes",
    "hate",
    "issue",
    "lag",
    "login",
    "otp",
    "poor",
    "problem",
    "slow",
    "stuck",
    "terrible",
    "worst",
}


def tokenize(text: Any) -> list[str]:
    """Tokenize text into lowercase alphabetical tokens."""
    return TOKEN_PATTERN.findall(str(text).lower())


def score_text_sentiment(text: Any) -> float:
    """Return a simple lexicon polarity score in the range [-1, 1]."""
    tokens = tokenize(text)
    if not tokens:
        return 0.0

    positive_count = sum(token in POSITIVE_WORDS for token in tokens)
    negative_count = sum(token in NEGATIVE_WORDS for token in tokens)
    raw_score = (positive_count - negative_count) / len(tokens)
    return max(-1.0, min(1.0, raw_score * 3))


def classify_sentiment(text: Any, rating: Any = None) -> tuple[str, float, float]:
    """Predict label, confidence score, and signed polarity for a review."""
    polarity = score_text_sentiment(text)

    if rating is not None and not pd.isna(rating):
        polarity = (0.7 * polarity) + (0.3 * ((float(rating) - 3.0) / 2.0))

    if polarity >= 0.15:
        label = "positive"
    elif polarity <= -0.15:
        label = "negative"
    else:
        label = "neutral"

    confidence = round(min(0.99, max(0.5, abs(polarity) + 0.5)), 3)
    return label, confidence, round(polarity, 3)


def build_analysis_dataset(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Build the Task 2 analysis dataset from the cleaned review dataframe."""
    analysis_df = clean_df.copy()
    analysis_df["review_id"] = analysis_df.apply(_build_stable_review_id, axis=1)
    analysis_df["review_text"] = analysis_df["review"]

    labels: list[str] = []
    confidences: list[float] = []
    polarities: list[float] = []
    for row in analysis_df.itertuples(index=False):
        label, confidence, polarity = classify_sentiment(row.review, row.rating)
        labels.append(label)
        confidences.append(confidence)
        polarities.append(polarity)

    analysis_df["sentiment_label"] = labels
    analysis_df["sentiment_score"] = confidences
    analysis_df["sentiment_polarity"] = polarities
    analysis_df["identified_theme"] = "Unassigned"

    return analysis_df[ANALYSIS_COLUMNS].copy()


def _build_stable_review_id(row: pd.Series) -> str:
    payload = "|".join(
        [
            str(row.get("bank", "")),
            str(row.get("date", "")),
            str(row.get("rating", "")),
            str(row.get("review", "")),
        ]
    )
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]
    return f"generated-{digest}"
