"""Plotting helpers for stakeholder-facing review analytics outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

try:
    import seaborn as sns
except ModuleNotFoundError:  # pragma: no cover - optional style dependency
    sns = None


def _apply_plot_style() -> None:
    if sns is not None:
        sns.set_theme(style="whitegrid")


def generate_all_plots(analysis_df: pd.DataFrame, output_dir: Path) -> list[Path]:
    """Generate the standard assignment plots and return their output paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    _apply_plot_style()
    generated_paths = [
        plot_sentiment_distribution(analysis_df, output_dir / "sentiment_distribution.png"),
        plot_rating_distribution(analysis_df, output_dir / "rating_distribution.png"),
        plot_theme_frequency(analysis_df, output_dir / "theme_frequency.png"),
    ]

    if not analysis_df.empty:
        generated_paths.append(
            plot_sentiment_trend(analysis_df, output_dir / "sentiment_trend.png")
        )

    return [path for path in generated_paths if path is not None]


def plot_sentiment_distribution(analysis_df: pd.DataFrame, destination: Path) -> Path | None:
    if analysis_df.empty:
        return None
    data = (
        analysis_df.groupby(["bank", "sentiment_label"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )
    ax = data.plot(kind="bar", stacked=True, figsize=(10, 5))
    ax.set_title("Sentiment Distribution by Bank")
    ax.set_xlabel("Bank")
    ax.set_ylabel("Review Count")
    plt.tight_layout()
    plt.savefig(destination)
    plt.close()
    return destination


def plot_rating_distribution(analysis_df: pd.DataFrame, destination: Path) -> Path | None:
    if analysis_df.empty:
        return None
    pivot = (
        analysis_df.groupby(["bank", "rating"])
        .size()
        .unstack(fill_value=0)
        .sort_index(axis=1)
    )
    ax = pivot.T.plot(kind="bar", figsize=(10, 5))
    ax.set_title("Rating Distribution per Bank")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Review Count")
    plt.tight_layout()
    plt.savefig(destination)
    plt.close()
    return destination


def plot_theme_frequency(analysis_df: pd.DataFrame, destination: Path) -> Path | None:
    if analysis_df.empty:
        return None
    theme_counts = (
        analysis_df.groupby(["bank", "identified_theme"])
        .size()
        .reset_index(name="count")
        .sort_values(["bank", "count"], ascending=[True, False])
    )
    ax = plt.figure(figsize=(11, 6)).gca()
    if sns is not None:
        sns.barplot(data=theme_counts, x="count", y="identified_theme", hue="bank", ax=ax)
    else:  # pragma: no cover - exercised only without seaborn
        for bank_name, bank_df in theme_counts.groupby("bank"):
            ax.barh(bank_df["identified_theme"], bank_df["count"], label=bank_name)
    ax.set_title("Theme Frequency by Bank")
    ax.set_xlabel("Review Count")
    ax.set_ylabel("Theme")
    ax.legend(title="Bank")
    plt.tight_layout()
    plt.savefig(destination)
    plt.close()
    return destination


def plot_sentiment_trend(analysis_df: pd.DataFrame, destination: Path) -> Path | None:
    if analysis_df.empty:
        return None
    trend_df = analysis_df.copy()
    trend_df["date"] = pd.to_datetime(trend_df["date"])
    daily = (
        trend_df.groupby(["date", "bank"])["sentiment_polarity"]
        .mean()
        .reset_index()
        .sort_values("date")
    )
    ax = plt.figure(figsize=(11, 5)).gca()
    if sns is not None:
        sns.lineplot(data=daily, x="date", y="sentiment_polarity", hue="bank", marker="o", ax=ax)
    else:  # pragma: no cover - exercised only without seaborn
        for bank_name, bank_df in daily.groupby("bank"):
            ax.plot(bank_df["date"], bank_df["sentiment_polarity"], marker="o", label=bank_name)
    ax.set_title("Average Sentiment Polarity Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Sentiment Polarity")
    ax.legend(title="Bank")
    plt.tight_layout()
    plt.savefig(destination)
    plt.close()
    return destination
