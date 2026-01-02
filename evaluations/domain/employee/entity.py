from dataclasses import dataclass
from enum import Enum
from uuid import UUID
from datetime import datetime


class JobTypeEnum(str, Enum):
    SOFTWARE_DEVELOPMENT = "SD"
    INFRASTRUCTURE_ENGINEER = "IF"
    MAINTENANCE_OPERATOR = "MT"

    @property
    def text(self) -> str:
        if self.value == JobTypeEnum.SOFTWARE_DEVELOPMENT:
            return "ソフト開発"
        elif self.value == JobTypeEnum.INFRASTRUCTURE_ENGINEER:
            return "インフラ"
        elif self.value == JobTypeEnum.MAINTENANCE_OPERATOR:
            return "保守運用"
        else:
            raise ValueError("無効な職種です。")

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(s.value, s.text) for s in cls]


class PositionEnum(str, Enum):
    JUNIOR = "JR"
    JUNIOR_S = "JS"
    ASSISTANT_ENGINEER = "AE"
    ENGINEER = "EN"
    SENIOR_ENGINEER = "SE"
    SECTION_CHIEF = "SC"

    @property
    def text(self) -> str:
        if self.value == PositionEnum.JUNIOR:
            return "一般"
        elif self.value == PositionEnum.JUNIOR_S:
            return "一般S"
        elif self.value == PositionEnum.ASSISTANT_ENGINEER:
            return "技師補"
        elif self.value == PositionEnum.ENGINEER:
            return "技師"
        elif self.value == PositionEnum.SENIOR_ENGINEER:
            return "主任"
        elif self.value == PositionEnum.SECTION_CHIEF:
            return "係長"
        else:
            raise ValueError("無効な職位です。")

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(s.value, s.text) for s in cls]


@dataclass(frozen=True)
class Employee:
    uuid: UUID
    employee_code: str
    name: str
    position: PositionEnum
    job_type: JobTypeEnum
    created_at: datetime
    updated_at: datetime
