"""
Experiment 05: Dense Vector Embedding Generation
------------------------------------------------
Goal: Convert cleaned textual data into 384-dimensional dense vector embeddings 
      using Sentence Transformers (all-MiniLM-L6-v2).
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


def run_embedding_experiment(input_path: Path, model_name: str) -> None:
    print(f"[INFO] Ingesting cleaned dataset from: {input_path}")
    df = pd.read_csv(input_path)

    print(f"[INFO] Loading Hugging Face Model: '{model_name}'...")
    # Load model onto CPU/GPU
    model = SentenceTransformer(model_name)

    print("[INFO] Generating dense embeddings for Resumes...")
    # encode() converts a list of strings into numpy arrays of shape (N, 384)
    resume_embeddings = model.encode(df["cleaned_resume"].tolist(), show_progress_bar=True)

    print("[INFO] Generating dense embeddings for Job Descriptions...")
    job_embeddings = model.encode(df["cleaned_job"].tolist(), show_progress_bar=True)

    print("\n=======================================================")
    print("             VECTOR EMBEDDINGS DIAGNOSTICS             ")
    print("=======================================================")
    print(f"Total Resume Vectors Generated : {len(resume_embeddings)}")
    print(f"Resume Vector Dimension Shape  : {resume_embeddings.shape}")
    print(f"Job Vector Dimension Shape     : {job_embeddings.shape}")
    print(f"Vector Data Type               : {resume_embeddings.dtype}")

    # Inspect the first 5 components of the first vector array
    print(f"\nSample Vector Slice (ID 1, First 5 dims): {resume_embeddings[0][:5]}")
    print("=======================================================\n")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    PROCESSED_DATA_PATH = BASE_DIR / "datasets" / "processed" / "cleaned_resumes.csv"
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    run_embedding_experiment(PROCESSED_DATA_PATH, MODEL_NAME)