# Task 2: Sentiment and Thematic Analysis

## Objective

Assign sentiment to each cleaned review and identify recurring business themes by bank.

## Sentiment Results

### Commercial Bank of Ethiopia

- Reviews analyzed: 450
- Average rating: 4.14
- Positive: 354
- Neutral: 28
- Negative: 68

### Bank of Abyssinia

- Reviews analyzed: 450
- Average rating: 3.61
- Positive: 298
- Neutral: 17
- Negative: 135

### Dashen Bank

- Reviews analyzed: 450
- Average rating: 4.06
- Positive: 350
- Neutral: 26
- Negative: 74

## Theme Highlights

### Commercial Bank of Ethiopia

- Dominant themes: General Feedback, Customer Support, Transaction Performance
- Pain points in sampled reviews: slow experience, transfer complaints, service frustration

### Bank of Abyssinia

- Dominant themes: General Feedback, Transaction Performance, UI and App Stability
- Pain points in sampled reviews: error messages, app reliability issues, slow transactions

### Dashen Bank

- Dominant themes: General Feedback, Account Access Issues, Transaction Performance
- Pain points in sampled reviews: slow login, password/account access friction, update complaints

## Deliverables

- Analysis dataset: `data/processed/bank_reviews_analysis.csv`
- Theme summary: `data/processed/bank_theme_summary.csv`
- Required fields included:
  - `review_id`
  - `review_text`
  - `sentiment_label`
  - `sentiment_score`
  - `identified_theme`

## Method Choice

To keep the pipeline lightweight and reproducible, the repository uses a modular lexicon-based sentiment baseline with rating-aware polarity adjustment. The code is structured so a transformer model can be swapped in later without changing the overall workflow.
