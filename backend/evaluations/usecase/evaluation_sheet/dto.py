from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class EvaluationSheetIdDto:
    uuid: UUID


@dataclass(frozen=True)
class EvaluationSheetEmployeeIdDto:
    employee_id: UUID


@dataclass(frozen=True)
class EvaluationSheetCreateDto:
    employee_id: UUID
    period_id: UUID


@dataclass(frozen=True)
class EvaluationSheetScoreDto:
    evaluation_item_id: UUID
    score: int | None


@dataclass(frozen=True)
class EvaluationSheetUpdateDto:
    uuid: UUID
    actor_employee_uuid: UUID
    sheet_scores: list[EvaluationSheetScoreDto]
    is_temporary: bool
