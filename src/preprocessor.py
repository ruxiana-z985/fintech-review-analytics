"""Helpers for cleaning and validating scraped review data."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

from src.config import CLEAN_COLUMNS, RAW_COLUMNS

WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_text(text: Any) -> str:
    """Collapse repeated whitespace and strip surrounding spaces."""
    if pd.isna(text):
        return ""
    return WHITESPACE_PATTERN.sub(" ", str(text)).strip()


def preprocess_dataframe(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Clean the raw scraped review dataset into the required five-column output."""
    missing_columns = [column for column in RAW_COLUMNS if column not in raw_df.columns]
    if missing_columns:
        raise ValueError(
            "Raw dataframe is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    df = raw_df.copy()
    report: dict[str, Any] = {
        "raw_count": int(len(df)),
        "dropped_missing_review_or_rating": 0,
        "dropped_duplicate_review_id": 0,
        "dropped_empty_review_after_cleaning": 0,
        "dropped_invalid_rating": 0,
        "dropped_invalid_date": 0,
    }

    report["dropped_missing_review_or_rating"] = int(
        df[["review", "rating"]].isna().any(axis=1).sum()
    )
    df = df.dropna(subset=["review", "rating"])

    if "review_id" in df.columns:
        duplicate_mask = df["review_id"].astype(str).duplicated(keep="first")
        report["dropped_duplicate_review_id"] = int(duplicate_mask.sum())
        df = df.loc[~duplicate_mask].copy()

    df["review"] = df["review"].apply(normalize_text)
    empty_mask = df["review"].eq("")
    report["dropped_empty_review_after_cleaning"] = int(empty_mask.sum())
    df = df.loc[~empty_mask].copy()

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    invalid_rating_mask = df["rating"].isna() | ~df["rating"].between(1, 5)
    report["dropped_invalid_rating"] = int(invalid_rating_mask.sum())
    df = df.loc[~invalid_rating_mask].copy()
    df["rating"] = df["rating"].astype(int)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    invalid_date_mask = df["date"].isna()
    report["dropped_invalid_date"] = int(invalid_date_mask.sum())
    df = df.loc[~invalid_date_mask].copy()
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    df["bank"] = df["bank"].fillna("Unknown Bank").astype(str).str.strip()
    df["source"] = df["source"].fillna("Google Play").astype(str).str.strip()

    clean_df = df[CLEAN_COLUMNS].sort_values(["bank", "date"], ascending=[True, False])
    clean_df = clean_df.reset_index(drop=True)

    report["clean_count"] = int(len(clean_df))
    report["retention_rate"] = round(
        (report["clean_count"] / report["raw_count"] * 100) if report["raw_count"] else 0,
        2,
    )
    report["date_range"] = {
        "min": clean_df["date"].min() if not clean_df.empty else None,
        "max": clean_df["date"].max() if not clean_df.empty else None,
    }
    report["bank_counts"] = clean_df["bank"].value_counts().sort_index().to_dict()
    report["rating_counts"] = clean_df["rating"].value_counts().sort_index().to_dict()

    return clean_df, report


def preprocess_reviews(reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Backward-compatible helper for list-of-dict pipelines."""
    df = pd.DataFrame(reviews)
    clean_df, _ = preprocess_dataframe(df)
    return clean_df.to_dict(orient="records")


def write_preprocessing_report(report: dict[str, Any], destination: Path) -> None:
    """Persist a markdown summary of the preprocessing stage."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Preprocessing Report",
        "",
        f"- Raw reviews: {report['raw_count']}",
        f"- Clean reviews: {report['clean_count']}",
        f"- Retention rate: {report['retention_rate']}%",
        f"- Dropped missing review/rating: {report['dropped_missing_review_or_rating']}",
        f"- Dropped duplicate review ids: {report['dropped_duplicate_review_id']}",
        (
            "- Dropped empty reviews after cleaning: "
            f"{report['dropped_empty_review_after_cleaning']}"
        ),
        f"- Dropped invalid ratings: {report['dropped_invalid_rating']}",
        f"- Dropped invalid dates: {report['dropped_invalid_date']}",
        (
            "- Date range: "
            f"{report['date_range']['min']} to {report['date_range']['max']}"
        ),
        "",
        "## Bank Counts",
        "",
        "```json",
        json.dumps(report["bank_counts"], indent=2, sort_keys=True),
        "```",
        "",
        "## Rating Counts",
        "",
        "```json",
        json.dumps(report["rating_counts"], indent=2, sort_keys=True),
        "```",
    ]
    destination.write_text("\n".join(lines), encoding="utf-8")
