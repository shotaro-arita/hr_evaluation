from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from evaluations.domain.employee.entity import PositionEnum


@dataclass(frozen=True)
class EvaluationItemPositionRelation:
    uuid: UUID
    position: PositionEnum
    evaluation_item_uuid: UUID
    order: int
    created_at: datetime
    updated_at: datetime
