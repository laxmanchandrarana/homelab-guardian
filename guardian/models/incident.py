from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Incident(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    service: str

    status: str

    message: str

    created: datetime = Field(default_factory=datetime.utcnow)
