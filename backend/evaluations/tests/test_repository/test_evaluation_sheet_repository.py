from uuid import uuid4

from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.infrastructure.repository.evaluation_sheet import (
    EvaluationSheetRepositoryImpl,
)
from evaluations.tests.utils.entity_factory import (
    EvaluationSheetFactory,
    EvaluationSheetScoreFactory,
)
from evaluations.tests.utils.model_factory import (
    DbEmployeeFactory,
    DbEvaluationItemFactory,
    DbEvaluationSheetFactory,
    DbEvaluationSheetScoreFactory,
    DbPeriodFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.models.evaluation_sheet import (
    DbEvaluationSheet,
    DbEvaluationSheetScore,
)


class EvaluationSheetRepositoryImplTest(MyAPITestCase):
    def test_find_by_id(self) -> None:
        with self.subTest("結果なし"):
            repository = EvaluationSheetRepositoryImpl()

            result = repository.find_by_id(uuid4())

            self.assertIsNone(result)

        with self.subTest("結果あり"):
            repository = EvaluationSheetRepositoryImpl()
            period = DbPeriodFactory()
            employee = DbEmployeeFactory()
            sheet_model = DbEvaluationSheetFactory(
                period=period,
                employee=employee,
                status=EvaluationSheetStatusEnum.PENDING,
            )
            own_item = DbEvaluationItemFactory()
            manager_item = DbEvaluationItemFactory()
            DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=own_item,
                score=2,
                is_manager=False,
            )
            DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=manager_item,
                score=4,
                is_manager=True,
            )

            result = repository.find_by_id(sheet_model.uuid)

            if result is None:
                raise ValueError("評価シートを取得できませんでした。")
            self.assertEqual(result.uuid, sheet_model.uuid)
            self.assertEqual(result.period_uuid, period.uuid)
            self.assertEqual(result.employee_uuid, employee.uuid)
            self.assertEqual(len(result.own_scores), 1)
            self.assertEqual(len(result.manager_scores), 1)

    def test_get_by_employee_period(self) -> None:
        with self.subTest("結果なし"):
            repository = EvaluationSheetRepositoryImpl()

            result = repository.get_by_employee_period(uuid4(), uuid4())

            self.assertIsNone(result)

        with self.subTest("結果あり"):
            repository = EvaluationSheetRepositoryImpl()
            period = DbPeriodFactory()
            employee = DbEmployeeFactory()
            sheet_model = DbEvaluationSheetFactory(period=period, employee=employee)

            result = repository.get_by_employee_period(employee.uuid, period.uuid)

            if result is None:
                raise ValueError("評価シートを取得できませんでした。")
            self.assertEqual(result.uuid, sheet_model.uuid)

    def test_create(self) -> None:
        with self.subTest("新規作成できること"):
            repository = EvaluationSheetRepositoryImpl()
            period = DbPeriodFactory()
            employee = DbEmployeeFactory()
            own_item = DbEvaluationItemFactory()
            manager_item = DbEvaluationItemFactory()
            own_score1 = EvaluationSheetScoreFactory(
                evaluation_item_uuid=own_item.uuid, score=3
            )
            own_score2 = EvaluationSheetScoreFactory(
                evaluation_item_uuid=own_item.uuid, score=4
            )
            own_score3 = EvaluationSheetScoreFactory(
                evaluation_item_uuid=own_item.uuid, score=5
            )
            manager_score1 = EvaluationSheetScoreFactory(
                evaluation_item_uuid=manager_item.uuid, score=2
            )
            manager_score2 = EvaluationSheetScoreFactory(
                evaluation_item_uuid=manager_item.uuid, score=1
            )
            entity = EvaluationSheetFactory(
                period_uuid=period.uuid,
                employee_uuid=employee.uuid,
                own_scores=[own_score1, own_score2, own_score3],
                manager_scores=[manager_score1, manager_score2],
                status=EvaluationSheetStatusEnum.SELF_COMPLETED,
            )

            result = repository.create(entity)

            self.assertEqual(result.uuid, entity.uuid)
            self.assertEqual(result.period_uuid, period.uuid)
            self.assertEqual(result.employee_uuid, employee.uuid)
            self.assertEqual(result.status, EvaluationSheetStatusEnum.SELF_COMPLETED)

            self.assertEqual(len(result.own_scores), 3)
            self.assertEqual(result.own_scores[2].uuid, own_score1.uuid)
            self.assertEqual(result.own_scores[2].score, 3)
            self.assertEqual(result.own_scores[1].uuid, own_score2.uuid)
            self.assertEqual(result.own_scores[1].score, 4)
            self.assertEqual(result.own_scores[0].uuid, own_score3.uuid)
            self.assertEqual(result.own_scores[0].score, 5)

            self.assertEqual(len(result.manager_scores), 2)
            self.assertEqual(result.manager_scores[1].uuid, manager_score1.uuid)
            self.assertEqual(result.manager_scores[1].score, 2)
            self.assertEqual(result.manager_scores[0].uuid, manager_score2.uuid)
            self.assertEqual(result.manager_scores[0].score, 1)

    def test_update(self) -> None:
        with self.subTest("スコアが同期されること"):
            repository = EvaluationSheetRepositoryImpl()
            period = DbPeriodFactory()
            employee = DbEmployeeFactory()
            sheet_model = DbEvaluationSheetFactory(
                period=period,
                employee=employee,
                status=EvaluationSheetStatusEnum.PENDING,
            )
            item1 = DbEvaluationItemFactory()
            item2 = DbEvaluationItemFactory()
            item3 = DbEvaluationItemFactory()
            existing_score1 = DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=item1,
                score=1,
                is_manager=False,
            )
            existing_score2 = DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=item2,
                score=2,
                is_manager=False,
            )
            DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=item3,
                score=2,
                is_manager=False,
            )
            DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=item2,
                score=2,
                is_manager=True,
            )

            updated_score1 = EvaluationSheetScoreFactory(
                uuid=existing_score1.uuid,
                evaluation_item_uuid=item1.uuid,
                score=4,
            )
            updated_score2 = EvaluationSheetScoreFactory(
                uuid=existing_score2.uuid,
                evaluation_item_uuid=item2.uuid,
                score=1,
            )
            new_score = EvaluationSheetScoreFactory(
                evaluation_item_uuid=item3.uuid,
                score=5,
            )
            updated_entity = EvaluationSheetFactory(
                uuid=sheet_model.uuid,
                period_uuid=period.uuid,
                employee_uuid=employee.uuid,
                own_scores=[updated_score1, updated_score2],
                manager_scores=[new_score],
                status=EvaluationSheetStatusEnum.MANAGER_COMPLETED,
            )

            result = repository.update(updated_entity)

            self.assertEqual(result.uuid, updated_entity.uuid)
            self.assertEqual(result.status, EvaluationSheetStatusEnum.MANAGER_COMPLETED)

            self.assertEqual(len(result.own_scores), 2)
            self.assertEqual(result.own_scores[1].uuid, existing_score1.uuid)
            self.assertEqual(result.own_scores[1].score, 4)
            self.assertEqual(result.own_scores[1].evaluation_item_uuid, item1.uuid)
            self.assertEqual(result.own_scores[0].uuid, existing_score2.uuid)
            self.assertEqual(result.own_scores[0].score, 1)
            self.assertEqual(result.own_scores[0].evaluation_item_uuid, item2.uuid)

            self.assertEqual(len(result.manager_scores), 1)
            self.assertEqual(result.manager_scores[0].uuid, new_score.uuid)
            self.assertEqual(result.manager_scores[0].score, 5)
            self.assertEqual(result.manager_scores[0].evaluation_item_uuid, item3.uuid)
