from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from guardian.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)

    created = Column(DateTime)

    severity = Column(String)

    service = Column(String)

    message = Column(String)

    healed = Column(String)
