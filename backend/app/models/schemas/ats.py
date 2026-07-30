from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict
from app.models.schemas.resume import ResumeResponse
from app.models.schemas.job import JobDescriptionResponse


class ATSAnalysisRequest(BaseModel):
    resume_id: int
    job_description_id: int


class ATSAnalysisResponse(BaseModel):
    id: int
    resume_id: int
    job_description_id: int
    overall_score: float
    semantic_score: float
    skill_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    created_at: datetime

    # Include nested resume and job details if needed
    resume: Optional[ResumeResponse] = None
    job_description: Optional[JobDescriptionResponse] = None

    model_config = ConfigDict(from_attributes=True)