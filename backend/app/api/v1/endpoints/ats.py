from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from app.schemas.ats import AnalysisRequest, AnalysisResponse, PDFParseResponse
from app.services.pdf_parser import pdf_parser_service
from app.services.ats_scorer import ats_scorer_service

router = APIRouter(prefix="/ats", tags=["ATS Engine"])


@router.post(
    "/parse-pdf",
    response_model=PDFParseResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract text from an uploaded PDF resume"
)
async def parse_pdf_resume(file: UploadFile = File(...)):
    """
    Accepts a PDF upload, validates the extension, and extracts plain text content.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a valid PDF document (.pdf)."
        )

    try:
        content_bytes = await file.read()
        extracted_text = pdf_parser_service.extract_text_from_bytes(content_bytes)

        if not extracted_text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract readable text from the uploaded PDF."
            )

        words = extracted_text.split()

        return PDFParseResponse(
            filename=file.filename,
            extracted_text=extracted_text,
            character_count=len(extracted_text),
            word_count=len(words)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while parsing the PDF: {str(e)}"
        )


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze resume text against job description"
)
async def analyze_resume_text(payload: AnalysisRequest):
    """
    Performs complete hybrid ATS analysis given raw resume and job text strings.
    """
    if not payload.resume_text.strip() or not payload.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both 'resume_text' and 'job_description' are required."
        )

    result = ats_scorer_service.analyze(
        raw_resume_text=payload.resume_text,
        raw_job_text=payload.job_description
    )

    return AnalysisResponse(**result)


@router.post(
    "/analyze-file",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload PDF resume + job description for instant ATS evaluation"
)
async def analyze_pdf_file(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    One-shot endpoint accepting a binary PDF file upload along with job description form data.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a PDF document."
        )

    content_bytes = await file.read()
    extracted_text = pdf_parser_service.extract_text_from_bytes(content_bytes)

    if not extracted_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Uploaded PDF appears to be empty or unreadable."
        )

    result = ats_scorer_service.analyze(
        raw_resume_text=extracted_text,
        raw_job_text=job_description
    )

    return AnalysisResponse(**result)