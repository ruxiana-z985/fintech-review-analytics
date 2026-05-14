"""Run the end-to-end fintech review analytics pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database import insert_reviews_to_postgres, prepare_database_frames
from src.preprocessor import preprocess_dataframe, write_preprocessing_report
from src.reporting import generate_all_plots
from src.scraper import ScraperUnavailableError, save_dataframe, scrape_all_banks
from src.sentiment import build_analysis_dataset
from src.themes import build_theme_summary, annotate_themes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape, clean, analyze, and export Ethiopian bank app reviews."
    )
    parser.add_argument(
        "--count-per-bank",
        type=int,
        default=500,
        help="Target number of reviews to collect per bank when scraping.",
    )
    parser.add_argument(
        "--input-csv",
        type=Path,
        help="Path to an existing raw review CSV. If provided, scraping is skipped.",
    )
    parser.add_argument(
        "--raw-output",
        type=Path,
        default=Path("data/raw/bank_reviews_raw.csv"),
        help="Where to save the raw scraped reviews.",
    )
    parser.add_argument(
        "--clean-output",
        type=Path,
        default=Path("data/processed/bank_reviews_clean.csv"),
        help="Where to save the cleaned five-column dataset.",
    )
    parser.add_argument(
        "--analysis-output",
        type=Path,
        default=Path("data/processed/bank_reviews_analysis.csv"),
        help="Where to save sentiment and theme outputs.",
    )
    parser.add_argument(
        "--theme-summary-output",
        type=Path,
        default=Path("data/processed/bank_theme_summary.csv"),
        help="Where to save the bank theme summary.",
    )
    parser.add_argument(
        "--report-output",
        type=Path,
        default=Path("reports/preprocessing_report.md"),
        help="Where to save the preprocessing report.",
    )
    parser.add_argument(
        "--plots-dir",
        type=Path,
        default=Path("reports/figures"),
        help="Directory where plots should be written.",
    )
    parser.add_argument(
        "--load-postgres",
        action="store_true",
        help="Load the analysis output into PostgreSQL using BANK_REVIEWS_DSN.",
    )
    return parser.parse_args()


def load_raw_reviews(args: argparse.Namespace) -> pd.DataFrame:
    if args.input_csv:
        return pd.read_csv(args.input_csv)

    try:
        raw_df = scrape_all_banks(count_per_bank=args.count_per_bank)
    except ScraperUnavailableError as exc:
        raise SystemExit(
            f"{exc}\n"
            "Install the project requirements and make sure network access is "
            "available, or pass --input-csv with an existing raw review export."
        ) from exc

    save_dataframe(raw_df, args.raw_output)
    return raw_df


def main() -> None:
    args = parse_args()

    raw_df = load_raw_reviews(args)
    clean_df, report = preprocess_dataframe(raw_df)
    analysis_df = build_analysis_dataset(clean_df)
    analysis_df = annotate_themes(analysis_df)
    theme_summary_df = build_theme_summary(analysis_df)

    save_dataframe(clean_df, args.clean_output)
    save_dataframe(analysis_df, args.analysis_output)
    save_dataframe(theme_summary_df, args.theme_summary_output)
    write_preprocessing_report(report, args.report_output)
    generated_plots = generate_all_plots(analysis_df, args.plots_dir)

    if args.load_postgres:
        banks_df, reviews_df = prepare_database_frames(analysis_df)
        inserted_rows = insert_reviews_to_postgres(banks_df, reviews_df)
        print(f"Loaded {inserted_rows} rows into PostgreSQL.")

    print(
        f"Raw reviews: {report['raw_count']} | "
        f"Clean reviews: {report['clean_count']} | "
        f"Theme rows: {len(theme_summary_df)} | "
        f"Plots: {len(generated_plots)}"
    )


if __name__ == "__main__":
    main()
