from unittest.mock import MagicMock
from uuid import uuid4

from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.evaluation_assignment.query_service import ManagerTargetModel
from evaluations.usecase.evaluation_assignment.usecase import (
    EvaluationAssignmentUsecase,
)


class EvaluationAssignmentUsecaseTest(MyAPITestCase):
    def test_get_manager_targets(self) -> None:
        usecase = EvaluationAssignmentUsecase()
        expected = [
            ManagerTargetModel(
                employee_uuid=uuid4(),
                employee_code="EMP100",
                name="Alice",
                position="EN",
                job_type="SD",
                role="MANAGER",
            )
        ]
        usecase.evaluation_assignment_query_service.get_manager_targets = MagicMock(
            return_value=expected
        )
        request_user = UserFactory()

        result = usecase.get_manager_targets(request_user)

        self.assertEqual(result, expected)
