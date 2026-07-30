from typing import List, Optional
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """
    Request model for raw text ATS evaluation.
    """
    resume_text: str = Field(..., description="Raw or preprocessed text extracted from candidate resume.")
    job_description: str = Field(..., description="Target job description text.")

    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "Experienced Senior Data Scientist skilled in Python, PyTorch, SQL, and FastAPI...",
                "job_description": "Looking for a Data Scientist proficient in Python, PyTorch, Transformers, and Docker..."
            }
        }


class SkillBreakdown(BaseModel):
    """
    Detailed breakdown of skill matches.
    """
    matched_skills: List[str]
    missing_skills: List[str]
    resume_skills: List[str]
    job_skills: List[str]


class AnalysisResponse(BaseModel):
    """
    Response model returned after ATS processing.
    """
    overall_score: float = Field(..., description="Hybrid ATS match score (0.0 to 100.0%).")
    semantic_score: float = Field(..., description="Semantic vector similarity score (60% weight).")
    skill_score: float = Field(..., description="Deterministic skill overlap percentage (40% weight).")
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    cleaned_resume: Optional[str] = None
    cleaned_job: Optional[str] = None


class PDFParseResponse(BaseModel):
    """
    Response model for raw PDF text extraction.
    """
    filename: str
    extracted_text: str
    character_count: int
    word_count: int