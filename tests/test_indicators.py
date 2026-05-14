import pandas as pd

from src.indicators import compute_indicators


def test_compute_indicators_adds_expected_columns():
    df = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=60, freq="D"),
            "Open": range(60),
            "High": range(1, 61),
            "Low": range(60),
            "Close": range(1, 61),
            "Volume": [1000] * 60,
        }
    )

    result = compute_indicators(df)

    assert {"sma_20", "ema_20", "rsi_14", "macd", "macd_signal", "daily_return"}.issubset(
        result.columns
    )

