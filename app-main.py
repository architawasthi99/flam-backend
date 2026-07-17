from fastapi import FastAPI

from app.database.database import Base
from app.database.database import engine

app = FastAPI(
    title="QueueCTL",
    version="1.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():

    return {
        "message": "QueueCTL Running"
    }
