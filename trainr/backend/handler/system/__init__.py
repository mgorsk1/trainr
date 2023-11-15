from abc import ABC
from abc import abstractmethod

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from trainr.backend.handler.database.engine import engine
from trainr.backend.handler.model.system.settings import \
    SystemSettingsHandlerModel
from trainr.utils import SystemMode


class SystemSettingHandler(ABC):
    @property
    @abstractmethod
    def setting_name(self):
        pass

    @property
    @abstractmethod
    def setting_default_value(self):
        pass

    def __init__(self):
        self.state = None

    def get_state(self) -> SystemSettingsHandlerModel:
        with Session(engine, expire_on_commit=False) as session:
            query_statement = select(SystemSettingsHandlerModel).where(
                SystemSettingsHandlerModel.setting_name == self.setting_name)
            try:
                self.state = session.scalars(query_statement).one()
            except NoResultFound:
                self.state = SystemSettingsHandlerModel(setting_name=self.setting_name,
                                                        setting_value=self.setting_default_value)
                session.add(self.state)
                session.commit()

        return self.state

    def set_mode(self, mode: SystemMode):
        if not self.state:
            self.get_state()

        self.state.setting_value = mode

        with Session(engine) as session:
            session.add(self.state)
            session.commit()
