from unittest.mock import patch
from uuid import uuid4

from rest_framework import status

from evaluations.tests.utils.model_factory import DbUserFactory
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.user.query_service import UserRetrieveModel
from evaluations.usecase.user.usecase import UserUsecase


class UserViewSetTests(MyAPITestCase):
    url = "/api/evaluations/users"

    def test_list(self) -> None:
        with patch.object(UserUsecase, "get_user") as mock:
            user = DbUserFactory()
            self.client.force_authenticate(user=user)
            expected = UserRetrieveModel(
                user_uuid=uuid4(),
                employee_uuid=uuid4(),
                employee_code="EMP001",
                name="Test User",
                position="JR",
                job_type="SD",
                is_manager=False,
                manager_target_count=0,
            )
            mock.return_value = expected
            user_entity = user.to_entity()

            response = self.client.get(f"{self.url}/")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(mock.call_args[0][0], user_entity)
