from unittest.mock import MagicMock
from uuid import uuid4

from rest_framework.exceptions import ValidationError

from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.user.query_service import UserRetrieveModel
from evaluations.usecase.user.usecase import UserUsecase


class UserUsecaseTest(MyAPITestCase):
    def test_get_user(self) -> None:
        with self.subTest("ユーザーが存在しない場合にエラーになること"):
            usecase = UserUsecase()
            usecase.user_query_service.get_user = MagicMock(return_value=None)
            request_user = UserFactory()

            with self.assertRaises(ValidationError) as e:
                usecase.get_user(request_user)

            self.assertEqual(e.exception.detail, ["ユーザーが存在しません。"])

        with self.subTest("正常に取得できること"):
            usecase = UserUsecase()
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
            usecase.user_query_service.get_user = MagicMock(return_value=expected)
            request_user = UserFactory()

            result = usecase.get_user(request_user)

            self.assertEqual(result, expected)
