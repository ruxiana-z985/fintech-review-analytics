# Task 3: PostgreSQL Database Engineering

## Objective

Prepare the cleaned and enriched review data for relational storage in PostgreSQL.

## Included Database Assets

- Schema file: `sql/schema.sql`
- Python loader: `src/database.py`
- Verification queries included in code:
  - review count per bank
  - average rating per bank
  - null checks for key columns

## Schema Design

### `banks`

- `bank_id` primary key
- `bank_name`
- `app_name`

### `reviews`

- `review_id` primary key
- `bank_id` foreign key
- `review_text`
- `rating`
- `review_date`
- `sentiment_label`
- `sentiment_score`
- `sentiment_polarity`
- `identified_theme`
- `source`

## Load Workflow

The main pipeline supports PostgreSQL loading through:

```bash
python scripts/run_pipeline.py --input-csv path/to/raw_reviews.csv --load-postgres
```

The connection string is expected through:

```bash
BANK_REVIEWS_DSN=postgresql://username:password@localhost:5432/bank_reviews
```

## Local Environment Note

The code and schema are ready, and PostgreSQL is installed locally on this machine, but automated loading from this session stopped at the password-authentication boundary because no database password was available in the environment. The submission still includes the complete schema, loader, and verification logic required by the assignment.
