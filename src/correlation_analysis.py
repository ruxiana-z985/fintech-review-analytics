"""Align news and stock data, then compute correlations."""

from __future__ import annotations

import pandas as pd


def align_news_to_trading_day(news_df: pd.DataFrame, price_df: pd.DataFrame) -> pd.DataFrame:
    aligned = news_df.copy().sort_values("publish_day").reset_index(drop=True)
    trading_days = (
        price_df[["Date"]].dropna().sort_values("Date").rename(columns={"Date": "trading_day"})
    )
    trading_days["trading_day"] = pd.to_datetime(trading_days["trading_day"]).dt.normalize()

    aligned["publish_day"] = pd.to_datetime(aligned["publish_day"]).dt.normalize()
    merged = pd.merge_asof(
        aligned.sort_values("publish_day"),
        trading_days.sort_values("trading_day"),
        left_on="publish_day",
        right_on="trading_day",
        direction="forward",
    )
    return merged.dropna(subset=["trading_day"])


def aggregate_daily_sentiment(aligned_news_df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        aligned_news_df.groupby(["stock", "trading_day"])
        .agg(
            average_sentiment=("sentiment_score", "mean"),
            article_count=("headline", "count"),
        )
        .reset_index()
    )
    grouped["sentiment_bucket"] = pd.cut(
        grouped["average_sentiment"],
        bins=[-1.01, -0.05, 0.05, 1.01],
        labels=["negative", "neutral", "positive"],
    )
    return grouped


def compute_daily_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    returns_df = price_df.copy().sort_values("Date").reset_index(drop=True)
    returns_df["daily_return"] = returns_df["Close"].pct_change() * 100
    returns_df["trading_day"] = pd.to_datetime(returns_df["Date"]).dt.normalize()
    return returns_df[["stock", "trading_day", "daily_return", "Close"]]


def combine_sentiment_and_returns(
    daily_sentiment_df: pd.DataFrame, returns_df: pd.DataFrame
) -> pd.DataFrame:
    return daily_sentiment_df.merge(
        returns_df,
        on=["stock", "trading_day"],
        how="inner",
    ).dropna(subset=["average_sentiment", "daily_return"])


def correlation_by_stock(combined_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for stock, group in combined_df.groupby("stock"):
        correlation = group["average_sentiment"].corr(group["daily_return"])
        rows.append(
            {
                "stock": stock,
                "pearson_correlation": correlation,
                "observations": len(group),
            }
        )
    return pd.DataFrame(rows).sort_values("stock").reset_index(drop=True)


def average_return_by_sentiment_bucket(combined_df: pd.DataFrame) -> pd.DataFrame:
    return (
        combined_df.groupby(["stock", "sentiment_bucket"])["daily_return"]
        .mean()
        .reset_index()
        .sort_values(["stock", "sentiment_bucket"])
    )
