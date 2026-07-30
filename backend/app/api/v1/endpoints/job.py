from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_jobs_placeholder():
    return {"message": "Jobs endpoint operational"}