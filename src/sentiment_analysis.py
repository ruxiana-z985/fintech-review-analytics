"""Headline sentiment scoring."""

from __future__ import annotations

import re

import pandas as pd

from src.config import NEGATIVE_WORDS, POSITIVE_WORDS

TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z\-']+")


def _fallback_sentiment(text: str) -> float:
    tokens = [token.lower() for token in TOKEN_PATTERN.findall(text)]
    if not tokens:
        return 0.0
    positive = sum(token in POSITIVE_WORDS for token in tokens)
    negative = sum(token in NEGATIVE_WORDS for token in tokens)
    return (positive - negative) / len(tokens)


def score_headline(text: str) -> float:
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer

        sia = SentimentIntensityAnalyzer()
        return float(sia.polarity_scores(text)["compound"])
    except Exception:
        return float(_fallback_sentiment(text))


def add_sentiment_scores(news_df: pd.DataFrame) -> pd.DataFrame:
    scored = news_df.copy()
    scored["sentiment_score"] = scored["headline"].astype(str).apply(score_headline)
    scored["sentiment_label"] = pd.cut(
        scored["sentiment_score"],
        bins=[-1.01, -0.05, 0.05, 1.01],
        labels=["negative", "neutral", "positive"],
    )
    return scored
