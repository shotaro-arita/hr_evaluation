from uuid import uuid4

from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.infrastructure.query_service.evaluation_weight_policy import (
    EvaluationWeightPolicyQueryServiceImpl,
)
from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.model_factory import (
    DbEvaluationWeightPolicyFactory,
    DbPeriodFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class EvaluationWeightPolicyQueryServiceImplTest(MyAPITestCase):
    def test_get_weights(self) -> None:
        query_service = EvaluationWeightPolicyQueryServiceImpl()
        user = UserFactory()
        period = DbPeriodFactory()
        other_period = DbPeriodFactory()

        DbEvaluationWeightPolicyFactory(
            period=period,
            position=PositionEnum.JUNIOR,
            category=EvaluationItemCategory.PERFORMANCE_RESULTS,
            weight=60,
        )
        DbEvaluationWeightPolicyFactory(
            period=period,
            position=PositionEnum.JUNIOR,
            category=EvaluationItemCategory.ATTITUDE_SKILLS,
            weight=40,
        )
        DbEvaluationWeightPolicyFactory(
            period=period,
            position=PositionEnum.ENGINEER,
            category=EvaluationItemCategory.PERFORMANCE_RESULTS,
            weight=50,
        )
        DbEvaluationWeightPolicyFactory(
            period=other_period,
            position=PositionEnum.JUNIOR,
            category=EvaluationItemCategory.PERFORMANCE_RESULTS,
            weight=10,
        )

        result = query_service.get_weights(user, period.uuid, PositionEnum.JUNIOR)

        self.assertEqual(result.period_uuid, period.uuid)
        self.assertEqual(result.position, PositionEnum.JUNIOR)
        self.assertEqual(len(result.weights), 2)
        categories = {weight.category: weight.weight for weight in result.weights}
        self.assertEqual(categories[EvaluationItemCategory.PERFORMANCE_RESULTS], 60)
        self.assertEqual(categories[EvaluationItemCategory.ATTITUDE_SKILLS], 40)
