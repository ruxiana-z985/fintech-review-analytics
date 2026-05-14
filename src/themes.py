"""Theme extraction helpers for bank app reviews."""

from __future__ import annotations

from collections import Counter
from itertools import pairwise
from typing import Any

import pandas as pd

THEME_KEYWORDS = {
    "Account Access Issues": {
        "access",
        "account",
        "code",
        "fingerprint",
        "login",
        "otp",
        "password",
        "pin",
        "register",
        "verification",
    },
    "Transaction Performance": {
        "cash",
        "delay",
        "failed",
        "fund",
        "load",
        "pending",
        "send",
        "slow",
        "transfer",
        "transaction",
    },
    "UI and App Stability": {
        "app",
        "bug",
        "button",
        "crash",
        "design",
        "freeze",
        "interface",
        "open",
        "screen",
        "update",
    },
    "Customer Support": {
        "branch",
        "call",
        "care",
        "customer",
        "help",
        "office",
        "response",
        "service",
        "staff",
        "support",
    },
    "Feature Requests": {
        "add",
        "biometric",
        "feature",
        "improve",
        "loan",
        "notification",
        "request",
        "statement",
        "tool",
        "upgrade",
    },
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "app",
    "be",
    "can",
    "but",
    "did",
    "do",
    "does",
    "don",
    "even",
    "for",
    "from",
    "have",
    "i",
    "if",
    "im",
    "isn",
    "i",
    "in",
    "is",
    "it",
    "its",
    "it",
    "just",
    "my",
    "not",
    "of",
    "on",
    "or",
    "our",
    "re",
    "s",
    "so",
    "still",
    "or",
    "so",
    "that",
    "the",
    "this",
    "t",
    "than",
    "their",
    "them",
    "there",
    "they",
    "too",
    "to",
    "up",
    "very",
    "we",
    "were",
    "when",
    "will",
    "with",
    "you",
    "your",
    "very",
}


def _tokenize_terms(text: Any) -> list[str]:
    clean = "".join(char.lower() if char.isalpha() or char == " " else " " for char in str(text))
    return [token for token in clean.split() if token and token not in STOPWORDS]


def identify_theme(text: Any) -> str:
    """Assign the best matching business theme to a review."""
    tokens = _tokenize_terms(text)
    token_set = set(tokens)

    bigrams = {" ".join(pair) for pair in pairwise(tokens)}
    token_set.update(bigrams)

    best_theme = "General Feedback"
    best_score = 0
    for theme_name, keywords in THEME_KEYWORDS.items():
        score = len(token_set.intersection(keywords))
        if score > best_score:
            best_score = score
            best_theme = theme_name
    return best_theme


def annotate_themes(analysis_df: pd.DataFrame) -> pd.DataFrame:
    """Apply theme labels to the analysis dataset."""
    themed_df = analysis_df.copy()
    themed_df["identified_theme"] = themed_df["review_text"].apply(identify_theme)
    return themed_df


def extract_top_keywords(texts: list[str], top_n: int = 10) -> list[str]:
    """Extract the most common non-stopword tokens from a group of reviews."""
    counter: Counter[str] = Counter()
    for text in texts:
        counter.update(_tokenize_terms(text))
    return [term for term, _ in counter.most_common(top_n)]


def build_theme_summary(analysis_df: pd.DataFrame, top_n_terms: int = 5) -> pd.DataFrame:
    """Summarize dominant themes and sample keywords per bank."""
    rows: list[dict[str, Any]] = []
    if analysis_df.empty:
        return pd.DataFrame(columns=["bank", "identified_theme", "review_count", "top_keywords"])

    grouped = analysis_df.groupby(["bank", "identified_theme"])
    for (bank_name, theme_name), group_df in grouped:
        rows.append(
            {
                "bank": bank_name,
                "identified_theme": theme_name,
                "review_count": int(len(group_df)),
                "top_keywords": ", ".join(
                    extract_top_keywords(group_df["review_text"].tolist(), top_n=top_n_terms)
                ),
            }
        )

    summary_df = pd.DataFrame(rows)
    return summary_df.sort_values(["bank", "review_count"], ascending=[True, False]).reset_index(
        drop=True
    )
