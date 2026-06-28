from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from guardian.database import Base


class Restore(Base):

    __tablename__ = "restores"

    id = Column(Integer, primary_key=True)

    filename = Column(String)

    started = Column(DateTime)

    completed = Column(DateTime)

    status = Column(String)
