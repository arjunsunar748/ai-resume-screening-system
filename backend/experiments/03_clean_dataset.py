"""
Experiment 03: Text Preprocessing & Data Cleaning
-------------------------------------------------
Goal: Build a deterministic text preprocessing pipeline using regular expressions (regex).
      Standardize noisy resume/job description text and save cleaned outputs to disk.
"""

import re
from pathlib import Path
import pandas as pd


class TextCleanerPipeline:
    """
    A modular text cleaning pipeline designed for resumes and job descriptions.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Applies sequential cleaning steps to a raw string:
        1. Lowercasing
        2. Removing URLs and emails
        3. Removing special bullet characters and non-alphanumeric noise
        4. Collapsing redundant whitespaces
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        # Step 1: Lowercase for uniform matching
        cleaned = text.lower()

        # Step 2: Remove URLs
        cleaned = re.sub(r"https?://\S+|www\.\S+", "", cleaned)

        # Step 3: Remove Email Addresses
        cleaned = re.sub(r"\S+@\S+\.\S+", "", cleaned)

        # Step 4: Remove special characters, bullet points, and unusual punctuation
        # Retain standard alphanumeric characters, plus spaces and plus signs (e.g. C++, C#)
        cleaned = re.sub(r"[^\w\s\+#]", " ", cleaned)

        # Step 5: Replace multiple spaces, tabs, or newlines with a single space
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        return cleaned


def run_cleaning_experiment(input_path: Path, output_path: Path) -> pd.DataFrame:
    print(f"[INFO] Ingesting raw dataset from: {input_path}")
    df = pd.read_csv(input_path)

    print("[INFO] Executing text cleaning pipeline...")
    # Apply cleaning to resumes and job descriptions
    df["cleaned_resume"] = df["resume_text"].apply(TextCleanerPipeline.clean_text)
    df["cleaned_job"] = df["job_description"].apply(TextCleanerPipeline.clean_text)

    # Calculate token reduction metrics
    df["raw_resume_word_count"] = df["resume_text"].apply(lambda x: len(x.split()))
    df["cleaned_resume_word_count"] = df["cleaned_resume"].apply(lambda x: len(x.split()))

    print("\n--- Cleaning Metrics ---")
    print(f"Average Raw Resume Word Count:     {df['raw_resume_word_count'].mean():.2f}")
    print(f"Average Cleaned Resume Word Count: {df['cleaned_resume_word_count'].mean():.2f}")

    # Ensure output directory exists and save processed file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Cleaned dataset saved to: {output_path.resolve()}")

    return df


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    RAW_DATA_PATH = BASE_DIR / "datasets" / "raw" / "sample_resumes.csv"
    PROCESSED_DATA_PATH = BASE_DIR / "datasets" / "processed" / "cleaned_resumes.csv"

    cleaned_df = run_cleaning_experiment(RAW_DATA_PATH, PROCESSED_DATA_PATH)

    print("\n--- Direct Comparison Sample (Record ID: 1) ---")
    sample = cleaned_df.iloc[0]
    print(f"RAW RESUME:\n{sample['resume_text']}\n")
    print(f"CLEANED RESUME:\n{sample['cleaned_resume']}")