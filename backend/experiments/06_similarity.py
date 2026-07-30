"""
Experiment 06: Semantic Similarity Computation
------------------------------------------------
Goal: Compute Cosine Similarity between resume embedding vectors 
      and target job description vectors to quantify contextual fit.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def compute_semantic_similarity(
    resume_texts: list[str], job_texts: list[str], model_name: str
) -> np.ndarray:
    """
    Computes pairwise cosine similarity between each resume vector and its paired job description vector.
    """
    print(f"[INFO] Initializing Transformer model '{model_name}'...")
    model = SentenceTransformer(model_name)

    print("[INFO] Encoding resumes into embedding space...")
    resume_vectors = model.encode(resume_texts)

    print("[INFO] Encoding job descriptions into embedding space...")
    job_vectors = model.encode(job_texts)

    # Compute pairwise cosine similarity between matching index pairs
    similarity_scores = []
    for r_vec, j_vec in zip(resume_vectors, job_vectors):
        # Reshape array for scikit-learn format (1, 384)
        score = cosine_similarity([r_vec], [j_vec])[0][0]
        similarity_scores.append(round(float(score) * 100, 2))

    return np.array(similarity_scores)


def run_similarity_experiment(input_path: Path, model_name: str) -> None:
    df = pd.read_csv(input_path)

    resumes = df["cleaned_resume"].fillna("").tolist()
    jobs = df["cleaned_job"].fillna("").tolist()

    scores = compute_semantic_similarity(resumes, jobs, model_name)
    df["semantic_similarity_score"] = scores

    print("\n=======================================================")
    print("           SEMANTIC SIMILARITY RESULTS REPORT           ")
    print("=======================================================\n")

    for idx, row in df.iterrows():
        print(f"--- Record ID: {row['id']} | Category: {row['category']} ---")
        print(f"Resume Snippet          : {row['resume_text'][:80]}...")
        print(f"Job Snippet             : {row['job_description'][:80]}...")
        print(f"Semantic Similarity Score: {row['semantic_similarity_score']}%\n")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    PROCESSED_DATA_PATH = BASE_DIR / "datasets" / "processed" / "cleaned_resumes.csv"
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    run_similarity_experiment(PROCESSED_DATA_PATH, MODEL_NAME)
    