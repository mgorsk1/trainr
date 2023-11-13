from dataclasses import dataclass

from datalite import datalite

from trainr.utils import SystemMode


@datalite(db_path="trainr.db")
@dataclass
class SystemModeState:
    value: str
