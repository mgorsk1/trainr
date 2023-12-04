from dataclasses import dataclass
from enum import Enum


class Coach(str, Enum):
    GORDON_RAMSAY = 'gordon_ramsay'
    MORGAN_FREEMAN = 'morgan_freeman'
    SNOOP_DOGG = 'snoop_dogg'


@dataclass
class MotivationInputApiModel:
    coach: Coach

@dataclass
class MotivationInfoApiModel(MotivationInputApiModel):
    text: str
