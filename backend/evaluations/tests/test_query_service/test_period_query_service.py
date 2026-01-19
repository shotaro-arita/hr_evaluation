from datetime import timedelta

from django.utils import timezone

from evaluations.infrastructure.query_service.period import PeriodQueryServiceImpl
from evaluations.tests.utils.entity_factory import UserFactory
from evaluations.tests.utils.model_factory import DbPeriodFactory
from evaluations.tests.utils.testcase import MyAPITestCase


class PeriodQueryServiceImplTest(MyAPITestCase):
    def test_get_list(self) -> None:
        query_service = PeriodQueryServiceImpl()
        now = timezone.now()
        current = DbPeriodFactory(
            name="Current",
            start_date=now - timedelta(days=1),
            end_date=now + timedelta(days=1),
        )
        past = DbPeriodFactory(
            name="Past",
            start_date=now - timedelta(days=10),
            end_date=now - timedelta(days=5),
        )
        user = UserFactory()

        result = query_service.get_list(user, now)

        result_ids = {period.uuid for period in result.periods}
        self.assertEqual(result_ids, {current.uuid, past.uuid})
        self.assertEqual(result.current_period_uuid, current.uuid)
