from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine

from app.api.jobs import router as job_router

app = FastAPI(
    title="QueueCTL",
    version="1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(job_router)


@app.get("/")
def home():

    return {
        "message": "QueueCTL Running"
    }
