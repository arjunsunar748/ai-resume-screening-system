from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_resumes_placeholder():
    return {"message": "Resumes endpoint operational"}