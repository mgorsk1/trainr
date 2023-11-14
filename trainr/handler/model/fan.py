from sqlalchemy import String, Boolean, Integer, Column

from trainr.handler.model import Base


class FanStateHandlerModel(Base):
    __tablename__ = "fanstate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    speed = Column(Integer, nullable=False)
    display_name = Column(String(32), nullable=False)
    is_on = Column(Boolean, nullable=False)
