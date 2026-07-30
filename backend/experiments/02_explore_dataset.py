"""
Experiment 02: Dataset Exploration & Corpus Diagnostics
-------------------------------------------------------
Goal: Compute text statistical metrics (word counts, vocabulary size, length distribution)
      to inform downstream text preprocessing and model sequence length limits.
"""

from pathlib import Path
import pandas as pd


def compute_text_diagnostics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates word counts, character counts, and average word lengths for resume and job texts.
    """
    print("[INFO] Computing text statistics for Resumes and Job Descriptions...")

    # Resume metrics
    df["resume_char_len"] = df["resume_text"].apply(len)
    df["resume_word_count"] = df["resume_text"].apply(lambda x: len(x.split()))
    
    # Job Description metrics
    df["job_char_len"] = df["job_description"].apply(len)
    df["job_word_count"] = df["job_description"].apply(lambda x: len(x.split()))

    return df


def print_corpus_insights(df: pd.DataFrame) -> None:
    """
    Prints aggregated statistical insights across categories and text features.
    """
    print("\n=========================================")
    print("        CORPUS STATISTICAL INSIGHTS       ")
    print("=========================================")

    print("\n--- Category Breakdown ---")
    print(df["category"].value_counts())

    print("\n--- Resume Word Count Metrics ---")
    print(df["resume_word_count"].describe())

    print("\n--- Job Description Word Count Metrics ---")
    print(df["job_word_count"].describe())

    # Calculate overall unique word vocabulary across raw corpus
    all_resume_words = " ".join(df["resume_text"]).lower().split()
    unique_words = set(all_resume_words)
    
    print("\n--- Vocabulary Statistics ---")
    print(f"Total Word Tokens in Resumes: {len(all_resume_words)}")
    print(f"Unique Vocabulary Count:      {len(unique_words)}")
    print(f"Lexical Diversity Ratio:     {len(unique_words) / len(all_resume_words):.2f}")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATASET_PATH = BASE_DIR / "datasets" / "raw" / "sample_resumes.csv"

    # Ingest
    df = pd.read_csv(DATASET_PATH)

    # Compute diagnostics
    df_analyzed = compute_text_diagnostics(df)

    # Output analysis report
    print_corpus_insights(df_analyzed)