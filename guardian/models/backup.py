from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Backup(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    service: str

    filename: str

    size: str

    created: datetime = Field(default_factory=datetime.utcnow)
