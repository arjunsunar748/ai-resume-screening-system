from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ResumeBase(BaseModel):
    filename: str


class ResumeCreate(ResumeBase):
    file_path: str
    raw_text: Optional[str] = None
    cleaned_text: Optional[str] = None


class ResumeResponse(ResumeBase):
    id: int
    raw_text: Optional[str] = None
    cleaned_text: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    