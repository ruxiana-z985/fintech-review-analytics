CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(120) NOT NULL UNIQUE,
    app_name VARCHAR(160) NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id TEXT PRIMARY KEY,
    bank_id INTEGER NOT NULL REFERENCES banks(bank_id),
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_date DATE NOT NULL,
    sentiment_label VARCHAR(16),
    sentiment_score DOUBLE PRECISION,
    sentiment_polarity DOUBLE PRECISION,
    identified_theme VARCHAR(128),
    source VARCHAR(32) NOT NULL
);
