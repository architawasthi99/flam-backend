from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.job import JobCreate
from app.services.queue_service import *

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post("/")
def enqueue(job: JobCreate, db: Session = Depends(get_db)):

    return enqueue_job(
        db,
        job.command,
        job.max_retries
    )


@router.get("/")
def list_jobs(db: Session = Depends(get_db)):

    return get_all_jobs(db)


@router.get("/{job_id}")
def get(job_id: str, db: Session = Depends(get_db)):

    return get_job(db, job_id)


@router.get("/state/{state}")
def state_jobs(state: str, db: Session = Depends(get_db)):

    return get_jobs_by_state(db, state)


@router.get("/status/summary")
def status(db: Session = Depends(get_db)):

    return get_summary(db)
