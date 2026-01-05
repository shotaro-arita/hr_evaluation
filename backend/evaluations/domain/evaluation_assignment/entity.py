from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID


class AssignmentRoleEnum(str, Enum):
    SELF = "SELF"
    MANAGER = "MANAGER"

    @property
    def text(self) -> str:
        if self.value == AssignmentRoleEnum.SELF:
            return "本人"
        elif self.value == AssignmentRoleEnum.MANAGER:
            return "管理者"
        else:
            raise ValueError("無効な役割です。")

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(s.value, s.text) for s in cls]


@dataclass(frozen=True)
class EvaluationAssignment:
    uuid: UUID
    # 一旦評価者は時期によって変わらないかつ一人の仕様
    # period_uuid: UUID
    target_employee_uuid: UUID
    manager_employee_uuid: UUID
    role: AssignmentRoleEnum
    created_at: datetime
    updated_at: datetime
