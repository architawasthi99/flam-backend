import time

from app.database.database import SessionLocal

from app.models.job import Job

from app.utils.executor import execute_command

from app.services.retry_service import retry_delay

def worker():

    db = SessionLocal()

    print("Worker Started")

    while True:

        job = (
            db.query(Job)
            .filter(Job.state == "pending")
            .first()
        )

        if not job:

            time.sleep(2)

            continue

        job.state = "processing"

        db.commit()

        result = execute_command(job.command)

        if result["success"]:

            job.state = "completed"

            db.commit()

            print("Completed :", job.id)

            continue

        job.attempts += 1

        if job.attempts <= job.max_retries:

            print(
                f"Retry {job.attempts} for {job.id}"
            )

            retry_delay(job.attempts)

            job.state = "pending"

            db.commit()

        else:

            job.state = "dead"

            db.commit()

            print("Moved to DLQ :", job.id)
