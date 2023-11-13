from dataclasses import dataclass

from datalite import datalite


@datalite(db_path="trainr.db")
@dataclass
class FanState:
    speed: int
    is_on: bool
    display_name: str

