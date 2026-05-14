"""Run the Nova Financial Solutions workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src.config import REPORTS_DIR, TICKERS
from src.correlation_analysis import (
    aggregate_daily_sentiment,
    align_news_to_trading_day,
    average_return_by_sentiment_bucket,
    combine_sentiment_and_returns,
    compute_daily_returns,
    correlation_by_stock,
)
from src.data_loader import copy_price_data, load_all_stock_prices, load_news_data
from src.eda import (
    add_headline_length,
    daily_publication_counts,
    hourly_publication_counts,
    publisher_counts,
    top_bigrams,
    top_keywords,
)
from src.indicators import compute_indicators
from src.sentiment_analysis import add_sentiment_scores


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["all", "eda", "indicators", "correlation"], default="all")
    parser.add_argument("--copy-price-data", action="store_true")
    return parser.parse_args()


def write_eda_outputs(news_df: pd.DataFrame) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    figures_dir = REPORTS_DIR / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    eda_df = add_headline_length(news_df)
    publisher_counts(eda_df).to_csv(REPORTS_DIR / "publisher_counts.csv", index=False)
    top_keywords(eda_df).to_csv(REPORTS_DIR / "top_keywords.csv", index=False)
    top_bigrams(eda_df).to_csv(REPORTS_DIR / "top_bigrams.csv", index=False)

    daily_counts = daily_publication_counts(eda_df)
    hourly_counts = hourly_publication_counts(eda_df)

    plt.figure(figsize=(10, 4))
    plt.hist(eda_df["headline_length"], bins=30)
    plt.title("Headline Character Count Distribution")
    plt.tight_layout()
    plt.savefig(figures_dir / "headline_length_distribution.png")
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(daily_counts["publish_day"], daily_counts["article_count"])
    plt.title("Daily News Volume")
    plt.tight_layout()
    plt.savefig(figures_dir / "daily_news_volume.png")
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.bar(hourly_counts["publish_hour"], hourly_counts["article_count"])
    plt.title("Publication Volume by Hour")
    plt.tight_layout()
    plt.savefig(figures_dir / "hourly_news_volume.png")
    plt.close()


def write_indicator_outputs(stock_frames: dict[str, pd.DataFrame]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    figures_dir = REPORTS_DIR / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    for ticker, df in stock_frames.items():
        indicator_df = compute_indicators(df)
        indicator_df.to_csv(REPORTS_DIR / f"{ticker}_indicators.csv", index=False)

        recent = indicator_df.tail(180)
        fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
        axes[0].plot(recent["Date"], recent["Close"], label="Close")
        axes[0].plot(recent["Date"], recent["sma_20"], label="SMA 20")
        axes[0].plot(recent["Date"], recent["ema_20"], label="EMA 20")
        axes[0].legend()
        axes[0].set_title(f"{ticker} Price with Moving Averages")

        axes[1].plot(recent["Date"], recent["rsi_14"], color="orange")
        axes[1].axhline(70, linestyle="--", color="red")
        axes[1].axhline(30, linestyle="--", color="green")
        axes[1].set_title(f"{ticker} RSI")

        axes[2].plot(recent["Date"], recent["macd"], label="MACD")
        axes[2].plot(recent["Date"], recent["macd_signal"], label="Signal")
        axes[2].bar(recent["Date"], recent["macd_hist"], alpha=0.3)
        axes[2].legend()
        axes[2].set_title(f"{ticker} MACD")

        plt.tight_layout()
        plt.savefig(figures_dir / f"{ticker}_technical_indicators.png")
        plt.close()


def write_correlation_outputs(news_df: pd.DataFrame, stock_frames: dict[str, pd.DataFrame]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    figures_dir = REPORTS_DIR / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    scored_news = add_sentiment_scores(news_df)
    combined_frames = []

    for ticker, price_df in stock_frames.items():
        ticker_news = scored_news[scored_news["stock"] == ticker]
        if ticker_news.empty:
            continue
        aligned = align_news_to_trading_day(ticker_news, price_df)
        daily_sentiment = aggregate_daily_sentiment(aligned)
        daily_returns = compute_daily_returns(price_df)
        combined = combine_sentiment_and_returns(daily_sentiment, daily_returns)
        combined_frames.append(combined)

    if not combined_frames:
        raise ValueError("No overlapping stock symbols were found between news and price data.")

    combined_df = pd.concat(combined_frames, ignore_index=True)
    combined_df.to_csv(REPORTS_DIR / "sentiment_returns_joined.csv", index=False)
    correlation_by_stock(combined_df).to_csv(REPORTS_DIR / "sentiment_return_correlation.csv", index=False)
    average_return_by_sentiment_bucket(combined_df).to_csv(
        REPORTS_DIR / "average_return_by_sentiment_bucket.csv", index=False
    )

    plt.figure(figsize=(8, 5))
    plt.scatter(combined_df["average_sentiment"], combined_df["daily_return"], alpha=0.6)
    corr = combined_df["average_sentiment"].corr(combined_df["daily_return"])
    plt.title(f"Sentiment vs Daily Return (r = {corr:.3f})")
    plt.xlabel("Average Daily Sentiment")
    plt.ylabel("Daily Return (%)")
    plt.tight_layout()
    plt.savefig(figures_dir / "sentiment_vs_return_scatter.png")
    plt.close()

    bucket_df = average_return_by_sentiment_bucket(combined_df)
    pivot = bucket_df.pivot(index="stock", columns="sentiment_bucket", values="daily_return")
    pivot.plot(kind="bar", figsize=(10, 5))
    plt.title("Average Daily Return by Sentiment Bucket")
    plt.tight_layout()
    plt.savefig(figures_dir / "average_return_by_sentiment_bucket.png")
    plt.close()


def main() -> None:
    args = parse_args()
    if args.copy_price_data:
        copied = copy_price_data()
        print(f"Copied {len(copied)} price files.")
        if args.task == "all":
            return

    stock_frames = load_all_stock_prices(TICKERS)

    if args.task in {"all", "eda", "correlation"}:
        news_df = load_news_data()
    else:
        news_df = None

    if args.task in {"all", "eda"}:
        write_eda_outputs(news_df)
    if args.task in {"all", "indicators"}:
        write_indicator_outputs(stock_frames)
    if args.task in {"all", "correlation"}:
        write_correlation_outputs(news_df, stock_frames)

    print("Pipeline finished.")


if __name__ == "__main__":
    main()
