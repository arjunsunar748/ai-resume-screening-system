from typing import Dict, List, Any
from app.services.text_cleaner import text_cleaner_service
from app.services.embedder import embedder_service
from app.services.skill_extractor import skill_extractor_service


class ATSScorerService:
    """
    Production-grade service that integrates text cleaning, embedding inference,
    skill gap analysis, and heuristic score weighting.
    """

    def __init__(self, semantic_weight: float = 0.60, skill_weight: float = 0.40):
        self.semantic_weight = semantic_weight
        self.skill_weight = skill_weight

    def _generate_suggestions(
        self, missing_skills: List[str], overall_score: float, semantic_score: float
    ) -> List[str]:
        suggestions = []

        if missing_skills:
            top_missing = ", ".join([f"'{s.upper()}'" for s in missing_skills[:4]])
            suggestions.append(f"Incorporate missing core skills: {top_missing}.")

        if semantic_score < 60.0:
            suggestions.append(
                "Revise bullet points to use context and verbs similar to those in the job description."
            )

        if overall_score >= 85.0:
            suggestions.append("Excellent match profile for this job description!")
        elif overall_score < 50.0:
            suggestions.append("Low overall match score. Consider tailoring your experience and skills to the role.")

        return suggestions

    def analyze(self, raw_resume_text: str, raw_job_text: str) -> Dict[str, Any]:
        """
        Executes the end-to-end evaluation pipeline for a resume against a target job description.

        Args:
            raw_resume_text (str): Extracted text from uploaded PDF.
            raw_job_text (str): Input text from target job description.

        Returns:
            Dict containing scores, skill breakdowns, and suggestions.
        """
        # Step 1: Preprocess texts
        cleaned_resume = text_cleaner_service.clean_for_embeddings(raw_resume_text)
        cleaned_job = text_cleaner_service.clean_for_embeddings(raw_job_text)

        # Step 2: Compute Semantic Vector Similarity Score
        semantic_score = embedder_service.calculate_similarity(cleaned_resume, cleaned_job)

        # Step 3: Compute Skill Extractor Metrics
        skill_analysis = skill_extractor_service.analyze_skill_gap(cleaned_resume, cleaned_job)
        skill_score = skill_analysis["skill_score"]
        matched_skills = skill_analysis["matched_skills"]
        missing_skills = skill_analysis["missing_skills"]

        # Step 4: Calculate Hybrid Score
        overall_score = round(
            (semantic_score * self.semantic_weight) + (skill_score * self.skill_weight), 2
        )

        # Step 5: Generate AI Improvements
        suggestions = self._generate_suggestions(missing_skills, overall_score, semantic_score)

        return {
            "overall_score": overall_score,
            "semantic_score": semantic_score,
            "skill_score": skill_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
            "cleaned_resume": cleaned_resume,
            "cleaned_job": cleaned_job
        }


# Global singleton instance
ats_scorer_service = ATSScorerService()