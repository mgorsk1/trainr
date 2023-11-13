from dataclasses import dataclass

from trainr.utils import SystemMode


@dataclass
class SystemModeInfo:
    value: SystemMode
