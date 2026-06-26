from typing import Optional

from sqlmodel import SQLModel, Field


class Service(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str

    compose_path: str

    enabled: bool = True

    auto_restart: bool = True
