from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.evaluation_item.entity import EvaluationItemCategory


@dataclass(frozen=True)
class EvaluationWeightPolicy:
    uuid: UUID
    period_uuid: UUID
    position: PositionEnum
    category: EvaluationItemCategory
    weight: int
    created_at: datetime
    updated_at: datetime
