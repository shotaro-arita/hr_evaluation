from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from re import S
from uuid import UUID, uuid4

from rest_framework.exceptions import ValidationError


class EvaluationSheetStatus(str, Enum):
    PENDING = "PENDING"
    SELF_EVALUATION_DRAFT = "SELF_EVALUATION_DRAFT"
    SELF_COMPLETED = "SELF_COMPLETED"
    MANAGER_EVALUATION_DRAFT = "MANAGER_EVALUATION_DRAFT"
    MANAGER_COMPLETED = "MANAGER_COMPLETED"
    CANCELLED = "CANCELLED"

    @property
    def text(self) -> str:
        if self.value == EvaluationSheetStatus.PENDING:
            return "未完了"
        elif self.value == EvaluationSheetStatus.SELF_EVALUATION_DRAFT:
            return "自己評価下書き"
        elif self.value == EvaluationSheetStatus.SELF_COMPLETED:
            return "自己評価完了"
        elif self.value == EvaluationSheetStatus.MANAGER_EVALUATION_DRAFT:
            return "管理者評価下書き"
        elif self.value == EvaluationSheetStatus.MANAGER_COMPLETED:
            return "管理者評価完了"
        elif self.value == EvaluationSheetStatus.CANCELLED:
            return "キャンセル"
        else:
            raise ValueError("無効な役割です。")


@dataclass(frozen=True)
class EvaluationSheet:
    uuid: UUID

    period_uuid: UUID
    employee_uuid: UUID

    own_evaluation_score: dict[UUID, int]
    manager_evaluation_score: dict[UUID, int]

    status: EvaluationSheetStatus

    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def initialize(
        cls,
        period_uuid: UUID,
        employee_uuid: UUID,
    ) -> "EvaluationSheet":
        uuid = uuid4()
        return cls(
            uuid=uuid,
            period_uuid=period_uuid,
            employee_uuid=employee_uuid,
            own_evaluation_score={},
            manager_evaluation_score={},
            status=EvaluationSheetStatus.PENDING,
            created_at=None,
            updated_at=None,
        )

    def check_update_own(self, actor_employee_uuid) -> "EvaluationSheet":
        if self.employee_uuid != actor_employee_uuid:
            raise ValidationError("更新者と評価シートの対象者が一致していません。")
        return self

    def _validation_score(self, score: int) -> None:
        if not 1 <= score <= 5:
            raise ValidationError("スコアは1~5で入力してください。")

    def update_own_score(
        self, own_evaluation_score: dict[UUID, int]
    ) -> "EvaluationSheet":
        for score in own_evaluation_score.values():
            self._validation_score(score)
        object.__setattr__(self, "own_evaluation_score", own_evaluation_score)
        return self

    def update_manager_score(
        self, manager_evaluation_score: dict[UUID, int]
    ) -> "EvaluationSheet":
        for score in manager_evaluation_score.values():
            self._validation_score(score)
        object.__setattr__(self, "manager_evaluation_score", manager_evaluation_score)
