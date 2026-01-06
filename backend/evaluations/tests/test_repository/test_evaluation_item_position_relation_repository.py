from uuid import uuid4

from evaluations.domain.employee.entity import PositionEnum
from evaluations.infrastructure.repository.evaluation_item_position_relation import (
    EvaluationItemPositionRelationRepositoryImpl,
)
from evaluations.tests.utils.model_factory import (
    DbEvaluationItemFactory,
    DbEvaluationItemPositionRelationFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class EvaluationItemPositionRelationRepositoryImplTest(MyAPITestCase):
    def test_find_item_ids_by_position(self) -> None:
        with self.subTest("対象なし"):
            repository = EvaluationItemPositionRelationRepositoryImpl()

            result = repository.find_item_ids_by_position(PositionEnum.JUNIOR)

            self.assertEqual(result, [])

        with self.subTest("対象ありで順序が保持されること"):
            repository = EvaluationItemPositionRelationRepositoryImpl()
            item1 = DbEvaluationItemFactory()
            item2 = DbEvaluationItemFactory()
            DbEvaluationItemPositionRelationFactory(
                position=PositionEnum.JUNIOR,
                evaluation_item=item1,
                order=2,
            )
            DbEvaluationItemPositionRelationFactory(
                position=PositionEnum.JUNIOR,
                evaluation_item=item2,
                order=1,
            )
            DbEvaluationItemPositionRelationFactory(
                position=PositionEnum.SECTION_CHIEF,
                evaluation_item=DbEvaluationItemFactory(),
                order=1,
            )

            result = repository.find_item_ids_by_position(PositionEnum.JUNIOR)

            self.assertEqual(result, [item2.uuid, item1.uuid])
