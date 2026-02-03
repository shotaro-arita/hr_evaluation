from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.infrastructure.query_service.evaluation_sheet import (
    EvaluationSheetQueryServiceImpl,
)
from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.model_factory import (
    DbEmployeeFactory,
    DbEvaluationSheetFactory,
    DbPeriodFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class EvaluationSheetIncompleteQueryServiceImplTest(MyAPITestCase):
    def test_get_incomplete_by_period(self) -> None:
        with self.subTest("未完了のみ取得できること"):
            period = DbPeriodFactory()
            other_period = DbPeriodFactory()
            employee_incomplete = DbEmployeeFactory()
            employee_complete = DbEmployeeFactory()

            incomplete_sheet = DbEvaluationSheetFactory(
                period=period,
                employee=employee_incomplete,
                own_status=EvaluationSheetStatusEnum.PENDING.value,
                manager_status=EvaluationSheetStatusEnum.COMPLETED.value,
            )
            DbEvaluationSheetFactory(
                period=period,
                employee=employee_complete,
                own_status=EvaluationSheetStatusEnum.COMPLETED.value,
                manager_status=EvaluationSheetStatusEnum.COMPLETED.value,
            )
            DbEvaluationSheetFactory(
                period=other_period,
                employee=DbEmployeeFactory(),
                own_status=EvaluationSheetStatusEnum.PENDING.value,
                manager_status=EvaluationSheetStatusEnum.PENDING.value,
            )

            service = EvaluationSheetQueryServiceImpl()
            user = UserFactory(employee_uuid=employee_incomplete.uuid)

            results = service.get_incomplete_by_period(user, period.uuid)

            self.assertEqual(len(results), 1)
            row = results[0]
            self.assertEqual(row.sheet_uuid, incomplete_sheet.uuid)
            self.assertEqual(row.employee_uuid, employee_incomplete.uuid)
