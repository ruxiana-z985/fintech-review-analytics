# Predicting Price Moves with News Sentiment

## Executive Summary

This project investigates whether financial news sentiment can help explain or anticipate short-term stock price moves for a focused set of large-cap technology stocks: AAPL, AMZN, GOOG, META, and NVDA. The analysis combines textual news data from the FNSPID dataset with historical market prices and computes both sentiment-based and technical market features.

The work is organized into three parts:

1. exploratory analysis of financial headlines and publishing behavior
2. technical-indicator analysis on stock prices
3. correlation analysis between average daily headline sentiment and daily stock returns

## Methodology

### Task 1: EDA

- computed headline length and word-count statistics
- identified most active publishers
- measured publication volume by day and hour
- extracted recurring keywords and bigrams from headlines

### Task 2: Technical Indicators

- loaded daily OHLCV price data for AAPL, AMZN, GOOG, META, and NVDA
- computed SMA, EMA, RSI, MACD, and 20-day return volatility
- generated visualizations showing price action together with indicators

### Task 3: Sentiment and Correlation

- assigned sentiment scores to headlines with VADER when available, plus a lexicon fallback
- aligned news dates to the next trading day when headlines landed on weekends or holidays
- averaged sentiment by stock and trading day
- computed daily stock returns and Pearson correlation against average daily sentiment

## Outputs

Generated outputs are written to `reports/` and include:

- publisher and keyword tables
- technical-indicator CSVs per stock
- joined sentiment/return dataset
- sentiment-return correlation table
- visualizations for EDA, indicators, and correlation

## Interpretation Template

After the FNSPID file is present in `data/raw/`, the pipeline produces the exact tables and figures needed to write the final interpretation:

- whether positive average sentiment tends to align with positive returns
- which publishers dominate coverage
- whether certain hours or dates contain abnormal news spikes
- whether technical indicators reinforce or contradict the news signal

## Limitations

- correlation does not imply causation
- news timing can lag or precede price reactions
- sentiment from headlines alone may miss nuance from full article text
- different stocks may react to news with different lags

## Recommendations

- treat sentiment as a supporting signal, not a standalone trading rule
- monitor whether strongly positive or negative daily sentiment clusters around momentum shifts
- combine sentiment features with technical indicators such as RSI and MACD before acting on a directional view
