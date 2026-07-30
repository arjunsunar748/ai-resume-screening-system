"""
Experiment 04: Skill Extraction & Keyword Matching Engine
---------------------------------------------------------
Goal: Build a deterministic phrase-aware skill extraction engine.
      Detect matched vs. missing skills between resumes and job descriptions.
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas as pd

# Comprehensive Skill Taxonomy grouped by Domain
SKILL_TAXONOMY: Dict[str, List[str]] = {
    "programming_languages": [
        "python", "javascript", "typescript", "c++", "c#", "java", "ruby", "go", "rust", "bash", "sql", "html", "css"
    ],
    "frameworks_and_libraries": [
        "react", "node.js", "nodejs", "express", "fastapi", "flask", "django", "pytorch", "tensorflow",
        "scikit-learn", "pandas", "numpy", "tailwind", "tailwind css", "matplotlib", "tableau"
    ],
    "devops_and_cloud": [
        "docker", "kubernetes", "terraform", "aws", "azure", "gcp", "ci/cd", "git", "bash scripting",
        "linux", "prometheus", "grafana"
    ],
    "databases_and_tools": [
        "postgresql", "postgres", "mongodb", "redis", "mysql", "excel", "rest api", "restful api"
    ],
    "ai_and_data_science": [
        "machine learning", "natural language processing", "nlp", "transformers", "data analysis",
        "business intelligence", "deep learning"
    ]
}


class SkillExtractor:
    """
    Extracts skills using phrase boundary matching and computes overlap statistics.
    """

    def __init__(self, taxonomy: Dict[str, List[str]]):
        # Flatten skills into a set for fast lookup and sort by length descending 
        # (longest phrases first to prevent sub-string collision, e.g., 'tailwind css' before 'css')
        all_skills = [skill for skills in taxonomy.values() for skill in skills]
        self.sorted_skills = sorted(list(set(all_skills)), key=len, reverse=True)

    def extract_skills(self, cleaned_text: str) -> Set[str]:
        """
        Extracts known tech skills from cleaned text using boundary-aware regex matching.
        """
        detected_skills = set()
        if not cleaned_text or not isinstance(cleaned_text, str):
            return detected_skills

        # Match skills using word boundaries or special character boundaries
        for skill in self.sorted_skills:
            # Escape special regex characters in skill names like 'c++' or 'c#'
            escaped_skill = re.escape(skill)
            pattern = rf"(?:\b|\s|^){escaped_skill}(?:\b|\s|$)"

            if re.search(pattern, cleaned_text):
                detected_skills.add(skill)

        return detected_skills

    def compare_skills(self, resume_skills: Set[str], job_skills: Set[str]) -> Tuple[Set[str], Set[str], float]:
        """
        Computes matched skills, missing skills, and the skill overlap percentage.
        """
        matched = resume_skills.intersection(job_skills)
        missing = job_skills.difference(resume_skills)

        # Calculate Skill Match Percentage
        if not job_skills:
            score = 100.0
        else:
            score = round((len(matched) / len(job_skills)) * 100.0, 2)

        return matched, missing, score


def run_skill_extraction_experiment(input_path: Path) -> None:
    print(f"[INFO] Ingesting cleaned dataset from: {input_path}")
    df = pd.read_csv(input_path)

    extractor = SkillExtractor(SKILL_TAXONOMY)

    print("\n=======================================================")
    print("           SKILL EXTRACTION & MATCHING REPORT          ")
    print("=======================================================\n")

    for idx, row in df.iterrows():
        resume_text = str(row["cleaned_resume"])
        job_text = str(row["cleaned_job"])

        resume_skills = extractor.extract_skills(resume_text)
        job_skills = extractor.extract_skills(job_text)

        matched, missing, skill_score = extractor.compare_skills(resume_skills, job_skills)

        print(f"--- Record ID: {row['id']} | Category: {row['category']} ---")
        print(f"Extracted Resume Skills ({len(resume_skills)}): {sorted(list(resume_skills))}")
        print(f"Extracted Job Skills    ({len(job_skills)}): {sorted(list(job_skills))}")
        print(f"Matched Skills          ({len(matched)}): {sorted(list(matched))}")
        print(f"Missing Skills          ({len(missing)}): {sorted(list(missing))}")
        print(f"Skill Match Score       : {skill_score}%\n")


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    PROCESSED_DATA_PATH = BASE_DIR / "datasets" / "processed" / "cleaned_resumes.csv"

    run_skill_extraction_experiment(PROCESSED_DATA_PATH)