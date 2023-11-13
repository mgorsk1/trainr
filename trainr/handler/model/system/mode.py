from dataclasses import dataclass

from datalite import datalite


@datalite(db_path="trainr.db")
@dataclass
class SystemModeHandlerModel:
    value: str
