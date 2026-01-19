from evaluations.infrastructure.query_service.evaluation_assignment import (
    EvaluationAssignmentQueryServiceImpl,
)
from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.model_factory import (
    DbEmployeeFactory,
    DbEvaluationAssignmentFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class EvaluationAssignmentQueryServiceImplTest(MyAPITestCase):
    def test_get_manager_targets(self) -> None:
        query_service = EvaluationAssignmentQueryServiceImpl()
        manager = DbEmployeeFactory(employee_code="MGR001")
        target1 = DbEmployeeFactory(employee_code="EMP001", name="Alice")
        target2 = DbEmployeeFactory(employee_code="EMP002", name="Bob")
        DbEvaluationAssignmentFactory(manager_employee=manager, target_employee=target1)
        DbEvaluationAssignmentFactory(manager_employee=manager, target_employee=target2)
        other_manager = DbEmployeeFactory()
        DbEvaluationAssignmentFactory(
            manager_employee=other_manager, target_employee=DbEmployeeFactory()
        )
        user = UserFactory(employee_uuid=manager.uuid)

        result = query_service.get_manager_targets(user)

        result_ids = {item.employee_uuid for item in result}
        self.assertEqual(result_ids, {target1.uuid, target2.uuid})
