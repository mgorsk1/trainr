from dataclasses import dataclass

from trainr.utils import SystemMode


@dataclass
class SystemModeInfoApiModel:
    system_mode: SystemMode


@dataclass
class SystemModeInputApiModel(SystemModeInfoApiModel):
    pass