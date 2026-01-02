from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class EvaluationSheetIdDto:
    uuid: UUID


@dataclass(frozen=True)
class EvaluationSheetEmployeeIdDto:
    employee_id: UUID


@dataclass(frozen=True)
class EvaluationSheetEmployeeCreateDto:
    employee_id: UUID
    period_id: UUID


@dataclass(frozen=True)
class EvaluationSheetEmployeeUpdateDto:
    uuid: UUID
    actor_employee_uuid: UUID
    scores: dict[UUID, int]
