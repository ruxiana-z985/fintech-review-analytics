"""Exploratory analysis helpers for the FNSPID dataset."""

from __future__ import annotations

import re
from collections import Counter

import pandas as pd

TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z\-']+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "for",
    "from",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
}


def add_headline_length(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["headline_length"] = enriched["headline"].astype(str).str.len()
    enriched["word_count"] = enriched["headline"].astype(str).str.split().str.len()
    return enriched


def publisher_counts(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    counts = df["publisher"].value_counts().head(top_n)
    return counts.rename_axis("publisher").reset_index(name="article_count")


def daily_publication_counts(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.groupby("publish_day").size().reset_index(name="article_count")
    return counts.sort_values("publish_day")


def hourly_publication_counts(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.groupby("publish_hour").size().reset_index(name="article_count")
    return counts.sort_values("publish_hour")


def extract_domains(df: pd.DataFrame) -> pd.DataFrame:
    domains = (
        df["publisher"]
        .astype(str)
        .str.extract(r"@([^ >]+)", expand=False)
        .fillna("non-email-publisher")
    )
    counts = domains.value_counts().rename_axis("domain").reset_index(name="article_count")
    return counts


def top_keywords(df: pd.DataFrame, top_n: int = 25) -> pd.DataFrame:
    counter: Counter[str] = Counter()
    for headline in df["headline"].astype(str):
        tokens = [
            token.lower()
            for token in TOKEN_PATTERN.findall(headline)
            if token.lower() not in STOPWORDS
        ]
        counter.update(tokens)
    return pd.DataFrame(counter.most_common(top_n), columns=["keyword", "count"])


def top_bigrams(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    counter: Counter[str] = Counter()
    for headline in df["headline"].astype(str):
        tokens = [
            token.lower()
            for token in TOKEN_PATTERN.findall(headline)
            if token.lower() not in STOPWORDS
        ]
        counter.update(" ".join(pair) for pair in zip(tokens, tokens[1:]))
    return pd.DataFrame(counter.most_common(top_n), columns=["bigram", "count"])
