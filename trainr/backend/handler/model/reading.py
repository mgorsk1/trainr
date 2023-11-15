from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from trainr.backend.handler.model import Base


class ReadingZoneHandlerModel(Base):
    __tablename__ = "readingzone"

    zone = Column(Integer, primary_key=True, nullable=False)
    reading_type = Column(String, primary_key=True, nullable=False)
    range_from = Column(Integer, nullable=False)
    range_to = Column(Integer, nullable=False)
    display_name = Column(String, nullable=False)


class ReadingZoneSpecHandlerModel(ReadingZoneHandlerModel):
    pass


class ThresholdHandlerModel(Base):
    __tablename__ = "readingthreshold"

    reading_type = Column(String, primary_key=True,
                          unique=True, nullable=False)
    reading_value = Column(Integer, nullable=False)


class ReadingHandlerModel(Base):
    __tablename__ = "reading"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, default=datetime.now())
    reading_type = Column(Integer, nullable=False)
    reading_value = Column(Integer, nullable=False)
