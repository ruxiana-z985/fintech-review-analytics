import pandas as pd

from src.themes import annotate_themes, build_theme_summary, identify_theme


def test_identify_theme_detects_account_access_issues():
    assert identify_theme("I keep getting login error and OTP problems") == (
        "Account Access Issues"
    )


def test_annotate_themes_labels_rows():
    analysis_df = pd.DataFrame(
        [
            {
                "review_id": "r1",
                "review_text": "The app crashes after every update",
                "rating": 1,
                "date": "2026-05-14",
                "bank": "Commercial Bank of Ethiopia",
                "source": "Google Play",
                "sentiment_label": "negative",
                "sentiment_score": 0.88,
                "sentiment_polarity": -0.75,
                "identified_theme": "Unassigned",
            }
        ]
    )

    themed_df = annotate_themes(analysis_df)

    assert themed_df.loc[0, "identified_theme"] == "UI and App Stability"


def test_build_theme_summary_returns_keyword_strings():
    analysis_df = pd.DataFrame(
        [
            {
                "review_id": "r1",
                "review_text": "slow transfer and failed transaction",
                "rating": 1,
                "date": "2026-05-14",
                "bank": "Dashen Bank",
                "source": "Google Play",
                "sentiment_label": "negative",
                "sentiment_score": 0.82,
                "sentiment_polarity": -0.7,
                "identified_theme": "Transaction Performance",
            }
        ]
    )

    summary_df = build_theme_summary(analysis_df)

    assert summary_df.loc[0, "bank"] == "Dashen Bank"
    assert "transfer" in summary_df.loc[0, "top_keywords"]
