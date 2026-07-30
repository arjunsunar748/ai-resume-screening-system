# Import the base class and all domain models
from app.db.session import Base
from app.models.domain.resume import Resume
from app.models.domain.job import JobDescription
from app.models.domain.ats import ATSAnalysis  # We will create this next