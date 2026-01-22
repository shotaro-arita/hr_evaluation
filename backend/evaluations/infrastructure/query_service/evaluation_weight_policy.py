from uuid import UUID

from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.user.entity import User
from evaluations.models.evaluation_weight_policy import DbEvaluationWeightPolicy
from evaluations.usecase.evaluation_weight_policy.query_service import (
    EvaluationWeightModel,
    EvaluationWeightPolicyListModel,
    EvaluationWeightPolicyQueryService,
)


class EvaluationWeightPolicyQueryServiceImpl(EvaluationWeightPolicyQueryService):
    def get_weights(
        self, user: User, period_id: UUID, position: PositionEnum
    ) -> EvaluationWeightPolicyListModel:
        weight_models = DbEvaluationWeightPolicy.objects.filter(
            period_id=period_id, position=position.value
        ).order_by("category")
        weights = [
            EvaluationWeightModel(
                category=EvaluationItemCategory(model.category), weight=model.weight
            )
            for model in weight_models
        ]
        return EvaluationWeightPolicyListModel(
            period_uuid=period_id, position=position, weights=weights
        )
