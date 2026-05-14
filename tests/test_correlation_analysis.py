import pandas as pd

from src.correlation_analysis import (
    aggregate_daily_sentiment,
    align_news_to_trading_day,
    combine_sentiment_and_returns,
    compute_daily_returns,
)


def test_weekend_news_aligns_to_next_trading_day():
    news_df = pd.DataFrame(
        {
            "headline": ["Positive update"],
            "stock": ["AAPL"],
            "publish_day": [pd.Timestamp("2024-01-06")],
            "sentiment_score": [0.5],
        }
    )
    price_df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-05", "2024-01-08"]), "Close": [10, 11], "stock": ["AAPL", "AAPL"]})

    aligned = align_news_to_trading_day(news_df, price_df)

    assert aligned.loc[0, "trading_day"] == pd.Timestamp("2024-01-08")


def test_sentiment_and_returns_can_be_joined():
    news_df = pd.DataFrame(
        {
            "headline": ["Positive update"],
            "stock": ["AAPL"],
            "publish_day": [pd.Timestamp("2024-01-05")],
            "sentiment_score": [0.5],
        }
    )
    price_df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-04", "2024-01-05"]),
            "Close": [10, 12],
            "stock": ["AAPL", "AAPL"],
        }
    )

    aligned = align_news_to_trading_day(news_df, price_df)
    daily_sentiment = aggregate_daily_sentiment(aligned)
    daily_returns = compute_daily_returns(price_df)
    combined = combine_sentiment_and_returns(daily_sentiment, daily_returns)

    assert len(combined) == 1
