"""Shared configuration for the Nova Financial Solutions project."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
PRICE_DIR = DATA_DIR / "prices"
REPORTS_DIR = PROJECT_ROOT / "reports"

NEWS_DATA_CANDIDATES = [
    DATA_DIR / "raw_analyst_ratings.csv",
    DATA_DIR / "financial_news.csv",
    DATA_DIR / "FNSPID.csv",
]

DOWNLOAD_PRICE_DIR = Path(r"C:/Users/lenovo/Downloads/yfinance_data/Data")
TICKERS = ["AAPL", "AMZN", "GOOG", "META", "NVDA"]

PRICE_FILE_MAP = {ticker: PRICE_DIR / f"{ticker}.csv" for ticker in TICKERS}
DOWNLOAD_PRICE_FILE_MAP = {
    ticker: DOWNLOAD_PRICE_DIR / f"{ticker}.csv" for ticker in TICKERS
}

POSITIVE_WORDS = {
    "beat",
    "bullish",
    "buy",
    "gain",
    "growth",
    "high",
    "jump",
    "outperform",
    "profit",
    "rally",
    "record",
    "rise",
    "strong",
    "surge",
    "upgrade",
}

NEGATIVE_WORDS = {
    "bearish",
    "cut",
    "decline",
    "downgrade",
    "drop",
    "fall",
    "fraud",
    "lawsuit",
    "loss",
    "miss",
    "plunge",
    "risk",
    "slump",
    "weak",
    "warning",
}
