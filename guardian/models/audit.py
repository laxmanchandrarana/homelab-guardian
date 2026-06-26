from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from guardian.database import Base


class Audit(Base):

    __tablename__ = "audit"

    id = Column(Integer, primary_key=True)

    created = Column(DateTime)

    action = Column(String)

    user = Column(String)

    details = Column(String)
