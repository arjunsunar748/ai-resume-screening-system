import re
from typing import Dict, List, Set, Tuple

# Standardized default Skill Taxonomy
DEFAULT_SKILL_TAXONOMY: Dict[str, List[str]] = {
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


class SkillExtractorService:
    """
    Production-grade service for extracting skills and computing skill match metrics.
    """

    def __init__(self, taxonomy: Dict[str, List[str]] = DEFAULT_SKILL_TAXONOMY):
        self.taxonomy = taxonomy
        # Flatten taxonomy skills into a deduplicated list
        all_skills = [skill for skills in self.taxonomy.values() for skill in skills]
        # Sort by length descending to match longer multi-word phrases first
        self.sorted_skills = sorted(list(set(all_skills)), key=len, reverse=True)

    def extract_skills(self, cleaned_text: str) -> List[str]:
        """
        Extracts skills present in the cleaned text string.
        
        Args:
            cleaned_text (str): Preprocessed text string.
            
        Returns:
            List[str]: List of unique detected skill keywords.
        """
        detected_skills: Set[str] = set()
        if not cleaned_text or not isinstance(cleaned_text, str):
            return []

        for skill in self.sorted_skills:
            escaped_skill = re.escape(skill)
            # Match skill surrounded by word boundaries or whitespace
            pattern = rf"(?:\b|\s|^){escaped_skill}(?:\b|\s|$)"

            if re.search(pattern, cleaned_text):
                detected_skills.add(skill)

        return sorted(list(detected_skills))

    def analyze_skill_gap(
        self, resume_cleaned_text: str, job_cleaned_text: str
    ) -> Dict[str, object]:
        """
        Compares skills extracted from a resume against those extracted from a job description.

        Args:
            resume_cleaned_text (str): Cleaned resume text.
            job_cleaned_text (str): Cleaned job description text.

        Returns:
            Dict containing:
                - matched_skills: List[str]
                - missing_skills: List[str]
                - skill_score: float (0.0 to 100.0)
        """
        resume_skills = set(self.extract_skills(resume_cleaned_text))
        job_skills = set(self.extract_skills(job_cleaned_text))

        matched = sorted(list(resume_skills.intersection(job_skills)))
        missing = sorted(list(job_skills.difference(resume_skills)))

        if not job_skills:
            skill_score = 100.0
        else:
            skill_score = round((len(matched) / len(job_skills)) * 100.0, 2)

        return {
            "matched_skills": matched,
            "missing_skills": missing,
            "skill_score": skill_score,
            "resume_skills": sorted(list(resume_skills)),
            "job_skills": sorted(list(job_skills))
        }


# Global singleton instance for injection across API endpoints
skill_extractor_service = SkillExtractorService()
