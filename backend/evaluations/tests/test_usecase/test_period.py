from unittest.mock import MagicMock
from datetime import datetime
from uuid import uuid4

from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.period.query_service import PeriodListModel, PeriodModel
from evaluations.usecase.period.usecase import PeriodUsecase


class PeriodUsecaseTest(MyAPITestCase):
    def test_get_periods(self) -> None:
        usecase = PeriodUsecase()
        expected = PeriodListModel(
            periods=[
                PeriodModel(
                    uuid=uuid4(),
                    name="2024 Q1",
                    start_date=datetime.now(),
                    end_date=datetime.now(),
                    is_current=True,
                )
            ],
            current_period_uuid=uuid4(),
        )
        usecase.period_query_service.get_list = MagicMock(return_value=expected)
        request_user = UserFactory()

        result = usecase.get_periods(request_user)

        self.assertEqual(result, expected)
