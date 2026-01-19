from unittest.mock import patch
from uuid import uuid4

from rest_framework import status

from evaluations.tests.utils.model_factory import DbUserFactory
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.evaluation_assignment.query_service import ManagerTargetModel
from evaluations.usecase.evaluation_assignment.usecase import (
    EvaluationAssignmentUsecase,
)


class EvaluationAssignmentViewSetTests(MyAPITestCase):
    url = "/api/evaluations/evaluation_assignments"

    def test_list(self) -> None:
        with patch.object(
            EvaluationAssignmentUsecase, "get_manager_targets"
        ) as mock:
            user = DbUserFactory()
            self.client.force_authenticate(user=user)
            mock.return_value = [
                ManagerTargetModel(
                    employee_uuid=uuid4(),
                    employee_code="EMP100",
                    name="Alice",
                    position="EN",
                    job_type="SD",
                    role="MANAGER",
                )
            ]
            user_entity = user.to_entity()

            response = self.client.get(f"{self.url}/")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(mock.call_args[0][0], user_entity)
