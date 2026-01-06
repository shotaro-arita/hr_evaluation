from uuid import uuid4

from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.infrastructure.query_service.evaluation_sheet import (
    EvaluationSheetQueryServiceImpl,
)
from evaluations.tests.utils.model_factory import (
    DbEmployeeFactory,
    DbEvaluationItemFactory,
    DbEvaluationSheetFactory,
    DbEvaluationSheetScoreFactory,
    DbPeriodFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class EvaluationSheetQueryServiceImplTest(MyAPITestCase):
    def test_find_by_id(self) -> None:
        with self.subTest("結果なし"):
            query_service = EvaluationSheetQueryServiceImpl()

            result = query_service.find_by_id(uuid4())

            self.assertIsNone(result)

        with self.subTest("結果あり"):
            query_service = EvaluationSheetQueryServiceImpl()
            period = DbPeriodFactory(name="2024 Q1")
            employee = DbEmployeeFactory(employee_code="EMP001", name="Alice")
            sheet_model = DbEvaluationSheetFactory(
                period=period,
                employee=employee,
                status=EvaluationSheetStatusEnum.SELF_COMPLETED,
            )
            item1 = DbEvaluationItemFactory(
                title="Item 1",
                category=EvaluationItemCategory.PERFORMANCE_RESULTS,
                description="Desc 1",
                criteria_1="c1",
                criteria_2="c2",
                criteria_3="c3",
                criteria_4="c4",
                criteria_5="c5",
            )
            item2 = DbEvaluationItemFactory(
                title="Item 2",
                category=EvaluationItemCategory.ATTITUDE_SKILLS,
                description="Desc 2",
                criteria_1="d1",
                criteria_2="d2",
                criteria_3="d3",
                criteria_4="d4",
                criteria_5="d5",
            )
            DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=item1,
                score=3,
                is_manager=False,
            )
            DbEvaluationSheetScoreFactory(
                evaluation_sheet=sheet_model,
                evaluation_item=item2,
                score=4,
                is_manager=True,
            )

            result = query_service.find_by_id(sheet_model.uuid)

            if result is None:
                raise ValueError("評価シートを取得できませんでした。")
            self.assertEqual(result.uuid, sheet_model.uuid)
            self.assertEqual(result.period_uuid, period.uuid)
            self.assertEqual(result.period_name, "2024 Q1")
            self.assertEqual(result.employee_uuid, employee.uuid)
            self.assertEqual(result.employee_code, "EMP001")
            self.assertEqual(result.employee_name, "Alice")
            self.assertEqual(result.status, EvaluationSheetStatusEnum.SELF_COMPLETED)

            self.assertEqual(len(result.self_evaluation_score), 1)
            self.assertEqual(result.self_evaluation_score[0].title, "Item 1")
            self.assertEqual(
                result.self_evaluation_score[0].category,
                EvaluationItemCategory.PERFORMANCE_RESULTS,
            )
            self.assertEqual(result.self_evaluation_score[0].description, "Desc 1")
            self.assertEqual(result.self_evaluation_score[0].criteria_1, "c1")
            self.assertEqual(result.self_evaluation_score[0].criteria_2, "c2")
            self.assertEqual(result.self_evaluation_score[0].criteria_3, "c3")
            self.assertEqual(result.self_evaluation_score[0].criteria_4, "c4")
            self.assertEqual(result.self_evaluation_score[0].criteria_5, "c5")
            self.assertEqual(result.self_evaluation_score[0].score, 3)

            self.assertEqual(len(result.manager_evaluation_score), 1)
            self.assertEqual(result.manager_evaluation_score[0].title, "Item 2")
            self.assertEqual(result.manager_evaluation_score[0].score, 4)

    def test_get_list_by_employee_id(self) -> None:
        with self.subTest("結果あり"):
            query_service = EvaluationSheetQueryServiceImpl()
            employee = DbEmployeeFactory()
            other_employee = DbEmployeeFactory()
            period1 = DbPeriodFactory()
            period2 = DbPeriodFactory()
            sheet1 = DbEvaluationSheetFactory(period=period1, employee=employee)
            sheet2 = DbEvaluationSheetFactory(period=period2, employee=employee)
            DbEvaluationSheetFactory(period=period1, employee=other_employee)

            result = query_service.get_list_by_employee_id(employee.uuid)

            result_ids = {sheet.uuid for sheet in result}
            self.assertEqual(result_ids, {sheet1.uuid, sheet2.uuid})
