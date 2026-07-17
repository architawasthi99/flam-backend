from sqlalchemy.orm import Session
from app.models.job import Job


def enqueue_job(db: Session, command: str, max_retries: int):

    job = Job(
        command=command,
        max_retries=max_retries,
        state="pending",
        attempts=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_all_jobs(db: Session):

    return db.query(Job).all()


def get_job(db: Session, job_id: str):

    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs_by_state(db: Session, state: str):

    return db.query(Job).filter(Job.state == state).all()


def get_summary(db: Session):

    return {
        "pending": db.query(Job).filter(Job.state == "pending").count(),
        "processing": db.query(Job).filter(Job.state == "processing").count(),
        "completed": db.query(Job).filter(Job.state == "completed").count(),
        "failed": db.query(Job).filter(Job.state == "failed").count(),
        "dead": db.query(Job).filter(Job.state == "dead").count(),
    }
