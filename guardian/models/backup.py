from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from guardian.database import Base


class Backup(Base):

    __tablename__ = "backups"

    id = Column(Integer, primary_key=True)

    filename = Column(String, unique=True)

    sha256 = Column(String)

    size = Column(Integer)

    created = Column(DateTime)

    verified = Column(Boolean)

    location = Column(String)

    status = Column(String)
