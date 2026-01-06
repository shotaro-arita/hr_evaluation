from uuid import uuid4

from evaluations.infrastructure.repository.evaluation_assignment_repository import (
    EvaluationAssignmentRepositoryImpl,
)
from evaluations.tests.utils.model_factory import (
    DbEvaluationAssignmentFactory,
    DbEmployeeFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class EvaluationAssignmentRepositoryImplTest(MyAPITestCase):
    def test_find_by_target_employee_id(self) -> None:
        with self.subTest("結果なし"):
            repository = EvaluationAssignmentRepositoryImpl()

            result = repository.find_by_target_employee_id(uuid4())

            self.assertIsNone(result)

        with self.subTest("結果あり"):
            repository = EvaluationAssignmentRepositoryImpl()
            target_employee = DbEmployeeFactory()
            manager_employee = DbEmployeeFactory()
            assignment_model = DbEvaluationAssignmentFactory(
                target_employee=target_employee,
                manager_employee=manager_employee,
            )

            result = repository.find_by_target_employee_id(target_employee.uuid)

            if result is None:
                raise ValueError("評価者割り当てを取得できませんでした。")
            self.assertEqual(result.uuid, assignment_model.uuid)
            self.assertEqual(result.target_employee_uuid, target_employee.uuid)
            self.assertEqual(result.manager_employee_uuid, manager_employee.uuid)
