from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from evaluations.utils.pagination import PaginationQueryDto
from uuid import UUID

from evaluations.domain.evaluation_sheet.entity import (
    EvaluationSheetStatus,
)


@dataclass(frozen=True)
class EvaluationSheetRetrieveModel:
    uuid: UUID

    period_uuid: UUID
    employee_uuid: UUID

    self_evaluation_score: dict[UUID, int]
    manager_evaluation_score: dict[UUID, int]

    status: EvaluationSheetStatus

    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class EvaluationSheetQueryDto:
    period_ids: list[UUID]


@dataclass(frozen=True)
class EvaluationSheetPaginationQueryDto(
    PaginationQueryDto, EvaluationSheetQueryDto
): ...


class EvaluationSheetQueryService(ABC):
    @abstractmethod
    def find_by_id(self, id: UUID) -> EvaluationSheetRetrieveModel | None:
        raise NotImplementedError

    @abstractmethod
    def get_list_by_employee_id(
        self, employee_id: UUID
    ) -> list[EvaluationSheetRetrieveModel]:
        raise NotImplementedError
