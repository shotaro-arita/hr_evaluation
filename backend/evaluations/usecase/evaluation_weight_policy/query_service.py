from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.user.entity import User


@dataclass(frozen=True)
class EvaluationWeightModel:
    category: EvaluationItemCategory
    weight: int


@dataclass(frozen=True)
class EvaluationWeightPolicyListModel:
    period_uuid: UUID
    position: PositionEnum
    weights: list[EvaluationWeightModel]


class EvaluationWeightPolicyQueryService(ABC):
    @abstractmethod
    def get_weights(
        self, user: User, period_id: UUID, position: PositionEnum
    ) -> EvaluationWeightPolicyListModel:
        raise NotImplementedError
