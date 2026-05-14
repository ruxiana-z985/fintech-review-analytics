"""Utilities for collecting Google Play reviews for Ethiopian bank apps."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.config import BANK_APPS, DEFAULT_COUNTRY, DEFAULT_LANGUAGE, RAW_COLUMNS


class ScraperUnavailableError(RuntimeError):
    """Raised when the Google Play scraper dependency is unavailable."""


def _import_google_play_scraper():
    try:
        from google_play_scraper import Sort, app, reviews
    except ModuleNotFoundError as exc:
        raise ScraperUnavailableError(
            "google-play-scraper is not installed in the active Python environment."
        ) from exc
    return Sort, app, reviews


def scrape_bank_reviews(
    bank_app,
    *,
    count: int = 500,
    lang: str = DEFAULT_LANGUAGE,
    country: str = DEFAULT_COUNTRY,
) -> pd.DataFrame:
    """Scrape raw review rows for a single bank app."""
    Sort, _, reviews = _import_google_play_scraper()
    review_rows, _ = reviews(
        bank_app.app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=count,
        filter_score_with=None,
    )

    data: list[dict[str, Any]] = []
    for row in review_rows:
        data.append(
            {
                "review_id": row.get("reviewId", ""),
                "review": row.get("content", ""),
                "rating": row.get("score"),
                "date": row.get("at"),
                "bank": bank_app.bank_name,
                "source": "Google Play",
                "app_name": bank_app.app_name,
            }
        )

    return pd.DataFrame(data, columns=RAW_COLUMNS)


def scrape_all_banks(count_per_bank: int = 500) -> pd.DataFrame:
    """Scrape all configured banks and concatenate the results."""
    frames = [
        scrape_bank_reviews(bank_app, count=count_per_bank) for bank_app in BANK_APPS
    ]
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=RAW_COLUMNS)


def save_dataframe(df: pd.DataFrame, destination: Path) -> None:
    """Save a dataframe to CSV, creating parent directories as needed."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)


def scrape_reviews() -> list[dict[str, Any]]:
    """Compatibility wrapper for the original starter scaffold."""
    return scrape_all_banks(count_per_bank=5).to_dict(orient="records")
