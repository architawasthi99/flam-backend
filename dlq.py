from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.dlq_service import *

router = APIRouter(
    prefix="/dlq",
    tags=["DLQ"]
)


@router.get("/")

def dead_jobs(db: Session = Depends(get_db)):

    return get_dead_jobs(db)


@router.post("/{job_id}")

def retry(job_id: str, db: Session = Depends(get_db)):

    return retry_dead_job(db, job_id)
