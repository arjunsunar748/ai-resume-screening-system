"""
Experiment 01: Dataset Ingestion & Validation
---------------------------------------------
Goal: Load raw dataset from disk, validate structure, inspect data types,
      and handle null/missing values gracefully.
"""

import os
from pathlib import Path
import pandas as pd


def load_and_validate_dataset(data_path: Path) -> pd.DataFrame:
    """
    Loads a dataset from CSV and verifies core schema compliance.
    """
    print(f"[INFO] Attempting to load dataset from: {data_path.resolve()}")

    if not data_path.exists():
        raise FileNotFoundError(f"[ERROR] Dataset not found at path: {data_path}")

    # Load dataset into pandas DataFrame
    df = pd.read_csv(data_path)

    # Validate non-empty dataset
    if df.empty:
        raise ValueError("[ERROR] Dataset loaded is empty!")

    print(f"[SUCCESS] Loaded {len(df)} records.")
    
    # Check expected schema columns
    required_columns = {"id", "category", "resume_text", "job_description"}
    missing_cols = required_columns - set(df.columns)
    
    if missing_cols:
        raise ValueError(f"[ERROR] Missing required columns in CSV: {missing_cols}")

    print("\n--- Dataset Summary ---")
    print(f"Total Rows: {df.shape[0]}")
    print(f"Total Columns: {df.shape[1]}")
    print("\n--- Missing Values Check ---")
    print(df.isnull().sum())

    return df


if __name__ == "__main__":
    # Resolve project root relative path
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATASET_PATH = BASE_DIR / "datasets" / "raw" / "sample_resumes.csv"

    # Execute ingestion step
    df = load_and_validate_dataset(DATASET_PATH)

    print("\n--- First 2 Records Sample ---")
    for idx, row in df.head(2).iterrows():
        print(f"\n[Record ID: {row['id']} | Category: {row['category']}]")
        print(f"Resume snippet: {row['resume_text'][:120]}...")
        print(f"Job snippet:    {row['job_description'][:120]}...")