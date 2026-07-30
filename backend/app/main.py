import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.endpoints import ats

# Setup application logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ats_system")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    Provisions database tables on application start.
    """
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables successfully created/verified.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    
    yield
    
    logger.info("Shutting down application...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# Parse allowed CORS origins from environment variable
origins = [
    origin.strip() 
    for origin in settings.ALLOWED_ORIGINS.split(",") 
    if origin.strip()
]

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(ats.router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health Check"])
def health_check():
    """
    Health check endpoint used by deployment platforms (Render) 
    and monitoring services to verify server status.
    """
    return {
        "status": "healthy",
        "app_name": settings.PROJECT_NAME,
        "environment": settings.APP_ENV
    }