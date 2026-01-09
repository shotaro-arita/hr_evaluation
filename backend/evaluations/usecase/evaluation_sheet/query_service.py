from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from evaluations.domain.user.entity import User
from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.utils.pagination import PaginationQueryDto
from uuid import UUID

from evaluations.domain.evaluation_sheet.entity import (
    EvaluationSheetStatusEnum,
)


@dataclass(frozen=True)
class EvaluationScoreRetrieveModel:
    uuid: UUID

    item_uuid: UUID
    title: str
    category: EvaluationItemCategory
    description: str

    criteria_1: str
    criteria_2: str
    criteria_3: str
    criteria_4: str
    criteria_5: str

    score: int | None


@dataclass(frozen=True)
class EvaluationSheetRetrieveModel:
    uuid: UUID

    period_uuid: UUID
    period_name: str

    employee_uuid: UUID
    employee_code: str
    employee_name: str

    self_evaluation_score: list[EvaluationScoreRetrieveModel]
    manager_evaluation_score: list[EvaluationScoreRetrieveModel]

    status: EvaluationSheetStatusEnum

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
    def find_by_id(self, user: User, id: UUID) -> EvaluationSheetRetrieveModel | None:
        raise NotImplementedError

    @abstractmethod
    def get_list_by_employee_id(
        self, user: User, employee_id: UUID
    ) -> list[EvaluationSheetRetrieveModel]:
        # TODO リスト用のリードモデル作成
        raise NotImplementedError
