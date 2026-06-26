from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from guardian.database import Base


class Restore(Base):

    __tablename__ = "restores"

    id = Column(Integer, primary_key=True)

    backup = Column(String)

    started = Column(DateTime)

    finished = Column(DateTime)

    duration = Column(Integer)

    success = Column(Boolean)

    rollback = Column(Boolean)
