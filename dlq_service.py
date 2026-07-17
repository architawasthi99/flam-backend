from sqlalchemy.orm import Session

from app.models.job import Job


def move_to_dlq(db: Session, job: Job):

    job.state = "dead"

    db.commit()

    db.refresh(job)


def get_dead_jobs(db: Session):

    return db.query(Job).filter(
        Job.state == "dead"
    ).all()


def retry_dead_job(db: Session, job_id):

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        return None

    job.state = "pending"

    job.attempts = 0

    db.commit()

    db.refresh(job)

    return job
