"""Load financial news and stock price data."""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

from src.config import (
    DOWNLOAD_PRICE_FILE_MAP,
    NEWS_DATA_CANDIDATES,
    PRICE_DIR,
    PRICE_FILE_MAP,
    TICKERS,
)


def copy_price_data() -> list[Path]:
    """Copy known stock CSVs into the project data directory."""
    PRICE_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    for ticker, source in DOWNLOAD_PRICE_FILE_MAP.items():
        destination = PRICE_FILE_MAP[ticker]
        if source.exists():
            shutil.copy2(source, destination)
            copied.append(destination)
    return copied


def locate_news_file() -> Path:
    for candidate in NEWS_DATA_CANDIDATES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "No FNSPID news dataset found. Put it in data/raw as raw_analyst_ratings.csv, "
        "financial_news.csv, or FNSPID.csv."
    )


def load_news_data(path: Path | None = None) -> pd.DataFrame:
    news_path = path or locate_news_file()
    df = pd.read_csv(news_path)

    expected_columns = {"headline", "publisher", "date", "stock"}
    missing = expected_columns.difference(df.columns)
    if missing:
        raise ValueError(f"News dataset is missing columns: {sorted(missing)}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True)
    df = df.dropna(subset=["date", "headline", "stock"])
    df["headline"] = df["headline"].astype(str)
    df["publisher"] = df["publisher"].fillna("Unknown").astype(str)
    df["stock"] = df["stock"].astype(str).str.upper()
    df["publish_day"] = df["date"].dt.tz_convert(None).dt.normalize()
    df["publish_hour"] = df["date"].dt.tz_convert(None).dt.hour
    return df


def load_stock_prices(ticker: str) -> pd.DataFrame:
    ticker = ticker.upper()
    price_path = PRICE_FILE_MAP[ticker]
    if not price_path.exists():
        copy_price_data()
    if not price_path.exists():
        raise FileNotFoundError(f"Missing stock price file for {ticker}: {price_path}")

    df = pd.read_csv(price_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    for column in numeric_cols:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["Date", "Close"]).sort_values("Date").reset_index(drop=True)
    df["stock"] = ticker
    return df


def load_all_stock_prices(tickers: list[str] | None = None) -> dict[str, pd.DataFrame]:
    tickers = tickers or TICKERS
    return {ticker: load_stock_prices(ticker) for ticker in tickers}
