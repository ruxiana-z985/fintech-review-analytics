# Task 1: Data Collection and Preprocessing

## Objective

Collect Google Play reviews for the three target Ethiopian bank apps and produce a clean five-column dataset for downstream analysis.

## Collection Run

- Collection date: 2026-05-14
- Source: Google Play
- Target apps:
  - Commercial Bank of Ethiopia
  - Bank of Abyssinia
  - Dashen Bank
- Requested reviews per bank: 450
- Collected reviews per bank: 450
- Total raw reviews: 1,350

## Cleaning Output

- Total clean reviews: 1,350
- Retention rate: 100.0%
- Missing review/rating rows dropped: 0
- Duplicate review ids dropped: 0
- Invalid date rows dropped: 0
- Invalid rating rows dropped: 0
- Final date range: 2022-12-07 to 2026-05-13

## Deliverables

- Clean dataset columns: `review`, `rating`, `date`, `bank`, `source`
- Raw export: `data/raw/bank_reviews_raw.csv`
- Clean export: `data/processed/bank_reviews_clean.csv`
- Preprocessing summary: `reports/preprocessing_report.md`

## Notes

The code is written so the project can be rerun with fresh data when network access is available. Datasets are intentionally ignored by Git, per assignment instructions.
