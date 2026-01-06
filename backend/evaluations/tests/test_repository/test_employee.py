from uuid import uuid4

from evaluations.tests.utils.model_factory import DbEmployeeFactory
from rest_framework.exceptions import ValidationError

from evaluations.infrastructure.repository.employee import (
    EmployeeRepositoryImpl,
)
from evaluations.tests.utils.testcase import MyAPITestCase


class EmployeeRepositoryImplTest(MyAPITestCase):
    def test_find_by_id(self) -> None:
        with self.subTest("結果なし"):
            repository = EmployeeRepositoryImpl()

            result = repository.find_by_id(uuid4())

            self.assertIsNone(result)

        with self.subTest("結果あり"):
            repository = EmployeeRepositoryImpl()
            employee_model = DbEmployeeFactory()

            result = repository.find_by_id(employee_model.uuid)

            if result is None:
                raise ValueError("従業員を取得できませんでした。")
            self.assertEqual(result.uuid, employee_model.uuid)
