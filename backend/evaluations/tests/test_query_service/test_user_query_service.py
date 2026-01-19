from uuid import uuid4

from evaluations.infrastructure.query_service.user import UserQueryServiceImpl
from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.model_factory import (
    DbEvaluationAssignmentFactory,
    DbUserFactory,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class UserQueryServiceImplTest(MyAPITestCase):
    def test_get_user(self) -> None:
        with self.subTest("結果なし"):
            query_service = UserQueryServiceImpl()
            user = UserFactory()

            result = query_service.get_user(user)

            self.assertIsNone(result)

        with self.subTest("結果あり"):
            query_service = UserQueryServiceImpl()
            db_user = DbUserFactory()
            DbEvaluationAssignmentFactory(manager_employee=db_user.employee)
            user = UserFactory(
                uuid=db_user.uuid,
                employee_uuid=db_user.employee_id,
                employee_code=db_user.employee.employee_code,
                name=db_user.name,
            )

            result = query_service.get_user(user)

            if result is None:
                raise ValueError("ユーザーを取得できませんでした。")
            self.assertEqual(result.user_uuid, db_user.uuid)
            self.assertEqual(result.employee_uuid, db_user.employee_id)
            self.assertEqual(result.employee_code, db_user.employee.employee_code)
            self.assertEqual(result.name, db_user.name)
            self.assertTrue(result.is_manager)
            self.assertEqual(result.manager_target_count, 1)
