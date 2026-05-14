import pandas as pd

from src.sentiment import build_analysis_dataset, classify_sentiment


def test_classify_sentiment_flags_positive_reviews():
    label, confidence, polarity = classify_sentiment("Great app and fast transfers", 5)

    assert label == "positive"
    assert confidence >= 0.5
    assert polarity > 0


def test_classify_sentiment_flags_negative_reviews():
    label, confidence, polarity = classify_sentiment("Login error and slow transfer", 1)

    assert label == "negative"
    assert confidence >= 0.5
    assert polarity < 0


def test_build_analysis_dataset_adds_sentiment_columns():
    clean_df = pd.DataFrame(
        [
            {
                "review": "Helpful support",
                "rating": 4,
                "date": "2026-05-14",
                "bank": "Bank of Abyssinia",
                "source": "Google Play",
            }
        ]
    )

    analysis_df = build_analysis_dataset(clean_df)

    assert "sentiment_label" in analysis_df.columns
    assert "sentiment_score" in analysis_df.columns
    assert analysis_df.loc[0, "review_id"].startswith("generated-")
