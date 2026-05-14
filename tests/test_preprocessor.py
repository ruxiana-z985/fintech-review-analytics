import pandas as pd

from src.preprocessor import normalize_text, preprocess_dataframe


def test_normalize_text_strips_and_collapses_whitespace():
    assert normalize_text("  Hello   WORLD  ") == "Hello WORLD"


def test_preprocess_dataframe_cleans_required_columns():
    raw_df = pd.DataFrame(
        [
            {
                "review_id": "1",
                "review": "  Fast   PAYMENTS ",
                "rating": 5,
                "date": "2026-05-14 10:00:00",
                "bank": "Dashen Bank",
                "source": "Google Play",
                "app_name": "Dashen Mobile",
            },
            {
                "review_id": "1",
                "review": "duplicate row",
                "rating": 4,
                "date": "2026-05-13",
                "bank": "Dashen Bank",
                "source": "Google Play",
                "app_name": "Dashen Mobile",
            },
        ]
    )

    clean_df, report = preprocess_dataframe(raw_df)

    assert clean_df.to_dict(orient="records") == [
        {
            "review": "Fast PAYMENTS",
            "rating": 5,
            "date": "2026-05-14",
            "bank": "Dashen Bank",
            "source": "Google Play",
        }
    ]
    assert report["dropped_duplicate_review_id"] == 1
