"""
Experiment 07: ATS Hybrid Scoring Engine & AI Recommendations
-------------------------------------------------------------
Goal: Combine Semantic Vector Distance (Phase 6) and Skill Match Ratio (Phase 5)
      into a single calibrated ATS Score with auto-generated feedback.
"""

import sys
import re
from pathlib import Path
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure 'backend' directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import directly from production services
from app.services.skill_extractor import SkillExtractorService
from app.services.embedder import EmbedderService


class HybridATSScorer:
    """
    Engine combining dense semantic search with explicit skill overlap heuristics.
    """

    def __init__(self, semantic_weight: float = 0.60, skill_weight: float = 0.40):
        self.semantic_weight = semantic_weight
        self.skill_weight = skill_weight
        self.skill_extractor = SkillExtractorService()
        self.embedder = EmbedderService()

    def generate_suggestions(
        self, missing_skills: list[str], overall_score: float, semantic_score: float
    ) -> list[str]:
        """
        Generates actionable suggestions to help the applicant optimize their resume.
        """
        suggestions = []

        if missing_skills:
            top_missing = ", ".join([f"'{s.upper()}'" for s in missing_skills[:4]])
            suggestions.append(f"Add key missing technical skills: {top_missing}.")

        if semantic_score < 60.0:
            suggestions.append(
                "Align your project descriptions and responsibilities more closely with the terminology used in the job description."
            )

        if overall_score >= 80.0:
            suggestions.append("Strong match! Ensure your relevant impact metrics (e.g., performance improvements, percentages) are highlighted.")
        elif overall_score < 50.0:
            suggestions.append("Low overall match score. Consider tailoring your resume heavily for this target position.")

        return suggestions

    def evaluate(self, resume_text: str, job_text: str) -> dict:
        # Step 1: Extract Skills & Calculate Skill Score
        skill_analysis = self.skill_extractor.analyze_skill_gap(resume_text, job_text)
        skill_score = skill_analysis["skill_score"]
        matched = skill_analysis["matched_skills"]
        missing = skill_analysis["missing_skills"]

        # Step 2: Calculate Semantic Vector Similarity Score
        semantic_score = self.embedder.calculate_similarity(resume_text, job_text)

        # Step 3: Compute Hybrid Weighted Overall Score
        overall_score = round(
            (semantic_score * self.semantic_weight) + (skill_score * self.skill_weight), 2
        )

        # Step 4: Generate Suggestions
        suggestions = self.generate_suggestions(missing, overall_score, semantic_score)

        return {
            "overall_score": overall_score,
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "suggestions": suggestions,
        }


def run_ats_scoring_experiment(input_path: Path) -> None:
    print(f"[INFO] Ingesting dataset from: {input_path}")
    df = pd.read_csv(input_path)
    scorer = HybridATSScorer(semantic_weight=0.60, skill_weight=0.40)

    print("\n=======================================================")
    print("               FINAL ATS HYBRID REPORT                 ")
    print("=======================================================\n")

    for idx, row in df.iterrows():
        res = scorer.evaluate(str(row["cleaned_resume"]), str(row["cleaned_job"]))

        print(f"--- Record ID: {row['id']} | Category: {row['category']} ---")
        print(f"OVERALL ATS SCORE : {res['overall_score']}%")
        print(f"  ├─ Semantic Fit : {res['semantic_score']}% (Weight: 60%)")
        print(f"  └─ Skill Match  : {res['skill_score']}% (Weight: 40%)")
        print(f"Matched Skills    : {res['matched_skills']}")
        print(f"Missing Skills    : {res['missing_skills']}")
        print("Suggestions:")
        for s in res["suggestions"]:
            print(f"  • {s}")
        print("\n" + "-" * 55 + "\n")


if __name__ == "__main__":
    PROCESSED_DATA_PATH = BASE_DIR / "datasets" / "processed" / "cleaned_resumes.csv"
    run_ats_scoring_experiment(PROCESSED_DATA_PATH)