import pandas as pd

from src.database import prepare_database_frames, verification_queries


def test_prepare_database_frames_builds_bank_and_review_tables():
    analysis_df = pd.DataFrame(
        [
            {
                "review_id": "r1",
                "review_text": "Great app",
                "rating": 5,
                "date": "2026-05-14",
                "bank": "Commercial Bank of Ethiopia",
                "source": "Google Play",
                "sentiment_label": "positive",
                "sentiment_score": 0.9,
                "sentiment_polarity": 0.8,
                "identified_theme": "UI and App Stability",
            }
        ]
    )

    banks_df, reviews_df = prepare_database_frames(analysis_df)

    assert {"bank_id", "bank_name", "app_name"} == set(banks_df.columns)
    assert reviews_df.loc[0, "bank_id"] == 1
    assert reviews_df.loc[0, "review_date"] == "2026-05-14"


def test_verification_queries_return_expected_checks():
    queries = verification_queries()

    assert set(queries) == {
        "review_count_per_bank",
        "average_rating_per_bank",
        "null_check",
    }
