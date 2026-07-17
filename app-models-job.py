import uuid

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from app.database.database import Base


class Job(Base):

    __tablename__ = "jobs"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    command = Column(
        String(500),
        nullable=False
    )

    state = Column(
        String(20),
        default="pending"
    )

    attempts = Column(
        Integer,
        default=0
    )

    max_retries = Column(
        Integer,
        default=3
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
