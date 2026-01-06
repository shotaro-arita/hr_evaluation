from uuid import UUID

from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.evaluation_item_position_relation.repository import (
    EvaluationItemPositionRelationRepository,
)
from evaluations.models.evaluation_item_position_relation import (
    DbEvaluationItemPositionRelation,
)


class EvaluationItemPositionRelationRepositoryImpl(
    EvaluationItemPositionRelationRepository
):
    def find_item_ids_by_position(self, position: PositionEnum) -> list[UUID]:
        return list(
            DbEvaluationItemPositionRelation.objects.filter(
                position=position.value
            ).order_by("order").values_list("evaluation_item_uuid", flat=True)
        )
