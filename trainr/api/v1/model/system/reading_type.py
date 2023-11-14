from dataclasses import dataclass
from enum import Enum


class ReadingType(str, Enum):
    HR = 'hr'
    FTP = 'ftp'


@dataclass
class SystemReadingTypeInfoApiModel:
    reading_type: ReadingType


@dataclass
class SystemReadingTypeInputApiModel(SystemReadingTypeInfoApiModel):
    pass
