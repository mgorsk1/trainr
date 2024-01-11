from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from trainr.backend.handler.model import Base


class FanStateHandlerModel(Base):
    __tablename__ = "fanstate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    speed = Column(Integer, nullable=False)
    display_name = Column(String(32), nullable=False)
    is_on = Column(Boolean, nullable=False)
