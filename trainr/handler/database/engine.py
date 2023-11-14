import os

from sqlalchemy import create_engine

from trainr.handler.model import Base

db_url = os.getenv('DB_URL', 'sqlite:///trainr.db')

engine = create_engine(db_url, echo=False)


def init_db():
    Base.metadata.create_all(engine)
