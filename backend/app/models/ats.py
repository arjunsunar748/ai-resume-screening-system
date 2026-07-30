from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from datetime import datetime
from app.core.database import Base


class ATSAnalysisLog(Base):
    __tablename__ = "ats_analysis_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=True)
    overall_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False)
    matched_skills = Column(JSON, nullable=False)
    missing_skills = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)