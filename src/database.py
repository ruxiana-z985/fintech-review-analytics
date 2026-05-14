"""Prepare and load bank review data into PostgreSQL."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from src.config import BANK_APPS

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"


def load_schema_sql() -> str:
    """Read the PostgreSQL schema file from disk."""
    return SCHEMA_PATH.read_text(encoding="utf-8")


def prepare_database_frames(analysis_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the enriched analysis dataset into bank and review tables."""
    banks_df = pd.DataFrame(
        [
            {"bank_id": index + 1, "bank_name": bank.bank_name, "app_name": bank.app_name}
            for index, bank in enumerate(BANK_APPS)
        ]
    )

    bank_lookup = banks_df.set_index("bank_name")["bank_id"]

    reviews_df = analysis_df.copy()
    reviews_df["bank_id"] = reviews_df["bank"].map(bank_lookup)
    reviews_df["review_text"] = reviews_df["review_text"].astype(str)
    reviews_df["review_date"] = pd.to_datetime(reviews_df["date"]).dt.strftime("%Y-%m-%d")

    columns = [
        "review_id",
        "bank_id",
        "review_text",
        "rating",
        "review_date",
        "sentiment_label",
        "sentiment_score",
        "sentiment_polarity",
        "identified_theme",
        "source",
    ]
    return banks_df, reviews_df[columns].copy()


def insert_reviews_to_postgres(banks_df: pd.DataFrame, reviews_df: pd.DataFrame) -> int:
    """Insert banks and reviews into PostgreSQL using BANK_REVIEWS_DSN."""
    dsn = os.getenv("BANK_REVIEWS_DSN")
    if not dsn:
        raise RuntimeError(
            "BANK_REVIEWS_DSN is not set. Example: "
            "postgresql://user:password@localhost:5432/bank_reviews"
        )

    try:
        import psycopg2
    except ModuleNotFoundError as exc:
        raise RuntimeError("psycopg2-binary is required to load PostgreSQL.") from exc

    schema_sql = load_schema_sql()
    inserted_rows = 0

    with psycopg2.connect(dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(schema_sql)

            cursor.executemany(
                """
                INSERT INTO banks (bank_id, bank_name, app_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (bank_name)
                DO UPDATE SET app_name = EXCLUDED.app_name
                """,
                list(banks_df.itertuples(index=False, name=None)),
            )

            cursor.executemany(
                """
                INSERT INTO reviews (
                    review_id,
                    bank_id,
                    review_text,
                    rating,
                    review_date,
                    sentiment_label,
                    sentiment_score,
                    sentiment_polarity,
                    identified_theme,
                    source
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (review_id)
                DO UPDATE SET
                    bank_id = EXCLUDED.bank_id,
                    review_text = EXCLUDED.review_text,
                    rating = EXCLUDED.rating,
                    review_date = EXCLUDED.review_date,
                    sentiment_label = EXCLUDED.sentiment_label,
                    sentiment_score = EXCLUDED.sentiment_score,
                    sentiment_polarity = EXCLUDED.sentiment_polarity,
                    identified_theme = EXCLUDED.identified_theme,
                    source = EXCLUDED.source
                """,
                list(reviews_df.itertuples(index=False, name=None)),
            )
            inserted_rows = len(reviews_df)
    return inserted_rows


def verification_queries() -> dict[str, str]:
    """Return the core SQL integrity checks required by the assignment."""
    return {
        "review_count_per_bank": """
            SELECT b.bank_name, COUNT(*) AS review_count
            FROM reviews r
            JOIN banks b ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY review_count DESC;
        """.strip(),
        "average_rating_per_bank": """
            SELECT b.bank_name, ROUND(AVG(r.rating)::numeric, 2) AS average_rating
            FROM reviews r
            JOIN banks b ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY average_rating DESC;
        """.strip(),
        "null_check": """
            SELECT
                SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) AS null_review_text,
                SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) AS null_rating,
                SUM(CASE WHEN review_date IS NULL THEN 1 ELSE 0 END) AS null_review_date
            FROM reviews;
        """.strip(),
    }
