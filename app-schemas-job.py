from pydantic import BaseModel

class JobCreate(BaseModel):
    command: str
    max_retries: int = 3


class JobResponse(BaseModel):
    id: str
    command: str
    state: str
    attempts: int
    max_retries: int

    class Config:
        from_attributes = True
