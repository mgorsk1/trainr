from sqlalchemy import Column
from sqlalchemy import String

from trainr.backend.handler.model import Base


class SystemSettingsHandlerModel(Base):
    __tablename__ = "settings"

    setting_name = Column(String(32), primary_key=True, unique=True)
    setting_value = Column(String(32), nullable=False)

    def __repr__(self):
        return super(SystemSettingsHandlerModel, self).__repr__()
