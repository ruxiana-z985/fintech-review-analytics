"""Technical indicator computations for stock price data."""

from __future__ import annotations

import pandas as pd


def compute_indicators(price_df: pd.DataFrame) -> pd.DataFrame:
    df = price_df.copy().sort_values("Date").reset_index(drop=True)

    close = df["Close"]
    df["daily_return"] = close.pct_change() * 100
    df["sma_20"] = close.rolling(window=20).mean()
    df["sma_50"] = close.rolling(window=50).mean()
    df["ema_20"] = close.ewm(span=20, adjust=False).mean()

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = (-delta.clip(upper=0)).rolling(window=14).mean()
    rs = gain / loss
    df["rsi_14"] = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    df["volatility_20"] = df["daily_return"].rolling(window=20).std()
    return df
