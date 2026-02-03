from uuid import uuid4

from evaluations.domain.incomplete_sheet_report.entity import IncompleteSheetReport
from evaluations.infrastructure.repository.incomplete_sheet_report import (
    IncompleteSheetReportRepositoryImpl,
)
from evaluations.tests.utils.model_factory import DbPeriodFactory
from evaluations.tests.utils.testcase import MyAPITestCase


class IncompleteSheetReportRepositoryImplTest(MyAPITestCase):
    def test_create(self) -> None:
        with self.subTest("作成できること"):
            period = DbPeriodFactory()
            repo = IncompleteSheetReportRepositoryImpl()
            report = IncompleteSheetReport(
                uuid=uuid4(),
                period_uuid=period.uuid,
                total=2,
                payload=[{"sheet_uuid": "s1"}, {"sheet_uuid": "s2"}],
                created_at=None,
            )

            saved = repo.create(report)

            self.assertEqual(saved.uuid, report.uuid)
            self.assertEqual(saved.period_uuid, report.period_uuid)
            self.assertEqual(saved.total, 2)
            self.assertEqual(saved.payload, report.payload)
            self.assertIsNotNone(saved.created_at)
