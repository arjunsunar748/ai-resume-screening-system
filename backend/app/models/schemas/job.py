from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class JobDescriptionBase(BaseModel):
    title: str
    company: Optional[str] = None
    raw_text: str


class JobDescriptionCreate(JobDescriptionBase):
    cleaned_text: Optional[str] = None


class JobDescriptionResponse(JobDescriptionBase):
    id: int
    cleaned_text: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)