from unittest.mock import patch
from uuid import uuid4

from rest_framework import status

from evaluations.tests.utils.model_factory import DbUserFactory
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.period.query_service import PeriodListModel, PeriodModel
from evaluations.usecase.period.usecase import PeriodUsecase


class PeriodViewSetTests(MyAPITestCase):
    url = "/api/evaluations/periods"

    def test_list(self) -> None:
        with patch.object(PeriodUsecase, "get_periods") as mock:
            user = DbUserFactory()
            self.client.force_authenticate(user=user)
            mock.return_value = PeriodListModel(
                periods=[
                    PeriodModel(
                        uuid=uuid4(),
                        name="2024 Q1",
                        start_date=user.created_at,
                        end_date=user.created_at,
                        is_current=True,
                    )
                ],
                current_period_uuid=uuid4(),
            )
            user_entity = user.to_entity()

            response = self.client.get(f"{self.url}/")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(mock.call_args[0][0], user_entity)
