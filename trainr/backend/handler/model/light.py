from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from trainr.backend.handler.model import Base


class LightStateHandlerModel(Base):
    __tablename__ = "lightstate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    color = Column(String(32), nullable=False)
    display_name = Column(String(32), nullable=False)
    is_on = Column(Boolean, nullable=False)
