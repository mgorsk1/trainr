from dataclasses import dataclass


@dataclass
class SystemSettingInputApiModel:
    setting_value: str


@dataclass
class SystemSettingInfoApiModel(SystemSettingInputApiModel):
    setting_name: str
