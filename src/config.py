"""Shared configuration for bank app analytics."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_LANGUAGE = "en"
DEFAULT_COUNTRY = "et"

RAW_COLUMNS = ["review_id", "review", "rating", "date", "bank", "source", "app_name"]
CLEAN_COLUMNS = ["review", "rating", "date", "bank", "source"]
ANALYSIS_COLUMNS = [
    "review_id",
    "review_text",
    "rating",
    "date",
    "bank",
    "source",
    "sentiment_label",
    "sentiment_score",
    "sentiment_polarity",
    "identified_theme",
]


@dataclass(frozen=True)
class BankApp:
    bank_name: str
    app_name: str
    app_id: str


BANK_APPS = (
    BankApp(
        bank_name="Commercial Bank of Ethiopia",
        app_name="Commercial Bank of Ethiopia",
        app_id="com.combanketh.mobilebanking",
    ),
    BankApp(
        bank_name="Bank of Abyssinia",
        app_name="BoA Mobile",
        app_id="com.boa.boaMobileBanking",
    ),
    BankApp(
        bank_name="Dashen Bank",
        app_name="Dashen Mobile",
        app_id="com.cr2.amolelight",
    ),
)
