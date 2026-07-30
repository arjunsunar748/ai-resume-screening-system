from fastapi import APIRouter
from app.api.v1.endpoints import resume, job, ats

api_router = APIRouter()

# Mount endpoints under specific resource tags
api_router.include_router(resume.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(job.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(ats.router, prefix="/ats", tags=["ATS Analysis"])