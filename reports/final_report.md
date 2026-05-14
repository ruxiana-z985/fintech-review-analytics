# Customer Experience Analytics for Ethiopian Fintech Apps

## Executive Summary

This project analyzed 1,350 Google Play reviews across three Ethiopian banking apps: Commercial Bank of Ethiopia, Bank of Abyssinia, and Dashen Bank. Each bank contributed 450 recent reviews. The dataset was cleaned into a standardized five-column structure, enriched with sentiment labels, grouped into recurring themes, and prepared for PostgreSQL storage.

The strongest overall performer in this run was Commercial Bank of Ethiopia, which posted the highest average rating at 4.14 and the highest positive review share. Dashen Bank followed closely with a 4.06 average rating. Bank of Abyssinia trailed with a 3.61 average rating and the largest negative-review share, which suggests a higher volume of unresolved friction in the customer experience.

Across all three apps, the most visible business issues were transaction speed, app stability, and account-access friction. These issues appeared in different proportions by bank, but they were consistent enough to support concrete product recommendations.

## Data Collection and Quality

- Source: Google Play
- Collection date: 2026-05-14
- Total reviews collected: 1,350
- Reviews per bank: 450
- Clean reviews retained: 1,350
- Retention rate: 100.0%
- Date range: 2022-12-07 to 2026-05-13

The preprocessing stage normalized dates, validated ratings, removed empty text, and preserved the assignment-ready columns `review`, `rating`, `date`, `bank`, and `source`.

## Sentiment Findings

### Commercial Bank of Ethiopia

- Average rating: 4.14
- Positive reviews: 354
- Neutral reviews: 28
- Negative reviews: 68

Commercial Bank of Ethiopia showed the strongest satisfaction profile in the dataset. Many positive comments were short but favorable, often describing the app as good, nice, or useful. Negative comments were fewer, but they consistently mentioned slowness and moments of poor service experience.

### Bank of Abyssinia

- Average rating: 3.61
- Positive reviews: 298
- Neutral reviews: 17
- Negative reviews: 135

Bank of Abyssinia had the weakest sentiment distribution in the comparison. The negative-review volume was materially higher than the other banks, and sample complaints frequently referenced errors, instability, and trust concerns. This app appears to carry the highest short-term product risk among the three.

### Dashen Bank

- Average rating: 4.06
- Positive reviews: 350
- Neutral reviews: 26
- Negative reviews: 74

Dashen Bank remained broadly positive overall, but its complaint profile leaned more heavily toward login and account-access issues than the other two banks. That pattern matters because access failures tend to interrupt basic customer trust more sharply than cosmetic issues.

## Theme Analysis

Five recurring themes were used to organize the feedback:

1. Account Access Issues
2. Transaction Performance
3. UI and App Stability
4. Customer Support
5. Feature Requests

### Common Themes Across Banks

- **Transaction Performance**: slow transfers, delayed transactions, and performance complaints appeared across all three apps.
- **UI and App Stability**: users mentioned updates, opening problems, and crashes or freezes.
- **Account Access Issues**: especially visible in Dashen Bank reviews, with repeated complaints about login and password friction.

### Bank-Level Theme Signals

- **Commercial Bank of Ethiopia**: strongest secondary issues were customer support and transaction speed.
- **Bank of Abyssinia**: the most concerning secondary issues were transaction performance and app stability.
- **Dashen Bank**: account-access problems stood out more clearly than in the other banks.

## Satisfaction Drivers and Pain Points

### Commercial Bank of Ethiopia

Drivers:
- generally strong user satisfaction and favorable star ratings
- many short positive reviews indicating acceptable everyday usability

Pain points:
- slow experience during some banking actions
- frustration with service responsiveness in negative reviews

### Bank of Abyssinia

Drivers:
- a meaningful base of positive reviews still exists
- some users explicitly describe the app as good or the bank as strong

Pain points:
- much higher negative-review share than peers
- repeated error and reliability complaints

### Dashen Bank

Drivers:
- strong overall positive sentiment
- positive comments on usefulness and transaction support

Pain points:
- login and password friction
- slow access and update-related complaints

## Recommendations

### Commercial Bank of Ethiopia

1. Investigate slow transfer or request-handling paths with product and engineering logs.
2. Pair app issue monitoring with customer-support escalation tagging to catch service-linked dissatisfaction faster.

### Bank of Abyssinia

1. Prioritize reliability fixes before new feature work, especially around recurring error states.
2. Launch a focused stability sprint and track whether negative review volume drops in the next review cycle.

### Dashen Bank

1. Treat login, password, and access problems as the highest-priority trust issue.
2. Review update flow and session handling to reduce repeated friction at app entry.

## Database Design Overview

The project includes a normalized PostgreSQL schema with separate `banks` and `reviews` tables, plus a loader script that prepares insert-ready data and verification queries for counts, averages, and null checks.

## Visual Deliverables

The project generated four figures:

- `reports/figures/sentiment_distribution.png`
- `reports/figures/rating_distribution.png`
- `reports/figures/theme_frequency.png`
- `reports/figures/sentiment_trend.png`

These support comparison across banks and can be used directly in a final write-up or presentation.

## Limitations

- The current sentiment implementation is a modular baseline rather than a transformer model.
- Theme assignment is rule-based and therefore less nuanced than a full NLP topic-modeling workflow.
- PostgreSQL loading in this session was blocked by missing database credentials, although the schema and loader are complete.

## Next Steps

1. Upgrade the sentiment stage to a transformer model for stronger classification.
2. Replace the keyword theme mapper with TF-IDF plus manual validation or topic modeling.
3. Load the final analysis dataset into PostgreSQL using local credentials and run the verification queries.
