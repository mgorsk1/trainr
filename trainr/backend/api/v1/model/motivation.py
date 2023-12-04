from dataclasses import dataclass

from trainr.utils import Coach


@dataclass
class MotivationInputApiModel:
    coach: Coach

@dataclass
class MotivationInfoApiModel(MotivationInputApiModel):
    text: str
