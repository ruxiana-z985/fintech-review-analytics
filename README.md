# Fintech Review Analytics

Customer experience analytics pipeline for Ethiopian fintech apps based on the 10 Academy Week 2 challenge. The project is structured around the four assignment tasks:

1. Scrape Google Play reviews for Commercial Bank of Ethiopia, Bank of Abyssinia, and Dashen Bank.
2. Clean and standardize the review dataset.
3. Run sentiment and theme analysis.
4. Prepare PostgreSQL-ready outputs, plots, and stakeholder-facing summaries.

## Assignment Scope

The challenge brief asks for:

- 400+ reviews per bank, or 1,200+ total reviews
- a clean CSV with `review`, `rating`, `date`, `bank`, and `source`
- sentiment labels and scores per review
- recurring theme extraction
- PostgreSQL schema and insert workflow
- business-ready insights and visualizations

This repository now includes code for each part of that workflow. When the required dependencies are installed and network access is available, the main pipeline can scrape directly from Google Play. If scraping is unavailable in the current environment, the rest of the pipeline can still run from a previously exported CSV.

## Project Structure

```text
fintech-review-analytics/
├── .github/workflows/unittests.yml
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── scripts/
│   ├── __init__.py
│   ├── README.md
│   └── run_pipeline.py
├── sql/
│   └── schema.sql
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── preprocessor.py
│   ├── reporting.py
│   ├── scraper.py
│   ├── sentiment.py
│   └── themes.py
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_preprocessor.py
│   ├── test_sentiment.py
│   └── test_themes.py
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

## Review Sources

The pipeline is configured for these Google Play app identifiers:

- `com.combanketh.mobilebanking` for Commercial Bank of Ethiopia
- `com.boa.boaMobileBanking` for Bank of Abyssinia
- `com.cr2.amolelight` for Dashen Bank

These app ids were matched from Google Play app listings that were discoverable on May 14, 2026.

## Methodology

### 1. Scraping

The scraper uses `google-play-scraper` to collect:

- review text
- star rating
- review date
- bank and app metadata
- source label

Target collection is 500 reviews per bank so the final cleaned dataset still clears the 400-review minimum after preprocessing.

### 2. Preprocessing

The cleaning logic:

- drops rows missing review text or rating
- removes duplicate `review_id` values
- strips and normalizes review whitespace
- removes empty reviews after cleaning
- normalizes dates to `YYYY-MM-DD`
- filters ratings outside the `1-5` range
- outputs the required five-column clean dataset

### 3. Sentiment and Theme Analysis

The repository includes a modular baseline pipeline for:

- assigning sentiment labels and scores
- extracting recurring review themes
- exporting an analysis-ready CSV

The current implementation uses a tested local lexicon fallback so the codebase remains runnable in constrained environments. The requirements file also includes the libraries needed to upgrade the sentiment stage to VADER, TextBlob, or a transformer-based workflow in a fuller environment.

### 4. Database Engineering

The PostgreSQL layer includes:

- a `banks` table
- a `reviews` table
- schema SQL
- a Python loader that prepares insert-ready frames
- verification queries for integrity checks

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline by scraping fresh data:

```bash
python scripts/run_pipeline.py --count-per-bank 500
```

Run the pipeline from an existing CSV instead of scraping:

```bash
python scripts/run_pipeline.py --input-csv path/to/raw_reviews.csv
```

Optional PostgreSQL load after analysis:

```bash
set BANK_REVIEWS_DSN=postgresql://username:password@localhost:5432/bank_reviews
python scripts/run_pipeline.py --input-csv path/to/raw_reviews.csv --load-postgres
```

## Outputs

The pipeline writes, by default:

- `data/raw/bank_reviews_raw.csv`
- `data/processed/bank_reviews_clean.csv`
- `data/processed/bank_reviews_analysis.csv`
- `data/processed/bank_theme_summary.csv`
- `reports/figures/*.png`
- `reports/preprocessing_report.md`

These outputs are intentionally ignored by Git to match the assignment requirement not to commit datasets.

## Limitations

- Google Play scraping depends on external network access and the `google-play-scraper` package.
- Transformer-based sentiment analysis is referenced in the assignment but is not hard-coded into tests, so the repo stays lightweight and CI-friendly.
- If Google Play returns fewer than the requested reviews for any bank, the limitation should be documented in the final report together with the date range actually collected.
