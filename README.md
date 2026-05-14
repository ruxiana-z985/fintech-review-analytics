# News Sentiment Analysis

Nova Financial Solutions project for predicting price moves with news sentiment.

## Project Focus

This repository addresses the Week 1 challenge:

1. Exploratory data analysis on the FNSPID financial news dataset
2. Technical indicator analysis on stock price data
3. Correlation analysis between headline sentiment and daily stock returns

## Expected Data

Place the financial news dataset in one of these paths:

- `data/raw/raw_analyst_ratings.csv`
- `data/raw/financial_news.csv`
- `data/raw/FNSPID.csv`

Stock price CSVs are loaded from either:

- `data/raw/prices/*.csv`
- or the provided local source folder `C:/Users/lenovo/Downloads/yfinance_data/Data`

Supported tickers in this submission:

- `AAPL`
- `AMZN`
- `GOOG`
- `META`
- `NVDA`

## Deliverables in This Repo

- [notebooks/task_1_eda.ipynb](C:/Users/lenovo/Desktop/fintech-review-analytics/notebooks/task_1_eda.ipynb)
- [notebooks/task_2_technical_indicators.ipynb](C:/Users/lenovo/Desktop/fintech-review-analytics/notebooks/task_2_technical_indicators.ipynb)
- [notebooks/task_3_sentiment_correlation.ipynb](C:/Users/lenovo/Desktop/fintech-review-analytics/notebooks/task_3_sentiment_correlation.ipynb)
- [scripts/run_pipeline.py](C:/Users/lenovo/Desktop/fintech-review-analytics/scripts/run_pipeline.py)
- [reports/final_report.md](C:/Users/lenovo/Desktop/fintech-review-analytics/reports/final_report.md)

## Setup

```bash
pip install -r requirements.txt
```

## Run

Copy the stock price CSVs into the project:

```bash
python scripts/run_pipeline.py --copy-price-data
```

Run the full workflow:

```bash
python scripts/run_pipeline.py
```

Run task-specific outputs:

```bash
python scripts/run_pipeline.py --task eda
python scripts/run_pipeline.py --task indicators
python scripts/run_pipeline.py --task correlation
```

## Notes

- Sentiment scoring uses VADER when available and falls back to a lightweight lexicon scorer.
- Technical indicators use TA-Lib when available and fall back to pandas implementations.
- The correlation step aligns weekend and holiday news to the next trading day.
