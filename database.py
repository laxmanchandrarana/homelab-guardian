from sqlmodel import SQLModel
from sqlmodel import create_engine

from guardian.settings import DATABASE

engine = create_engine(f"sqlite:///{DATABASE}")


def init_db():

    SQLModel.metadata.create_all(engine)
