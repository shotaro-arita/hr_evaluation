from unittest.mock import MagicMock
from uuid import uuid4

from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.tests.utils.testcase import MyAPITestCase
from evaluations.usecase.evaluation_sheet.query_service import (
    IncompleteSheetRowModel,
)
from evaluations.usecase.incomplete_sheet_report.usecase import (
    IncompleteSheetReportUsecase,
)
from evaluations.usecase.period.query_service import PeriodListModel


class IncompleteSheetReportUsecaseTest(MyAPITestCase):
    def test_generate_current_period_report(self) -> None:
        with self.subTest("今期が存在しない場合はNoneを返す"):
            usecase = IncompleteSheetReportUsecase()
            usecase.period_query_service.get_list = MagicMock(
                return_value=PeriodListModel(
                    periods=[], current_period_uuid=None
                )
            )
            usecase.evaluation_sheet_query_service.get_incomplete_by_period = (
                MagicMock(return_value=[])
            )
            usecase.incomplete_sheet_report_repository.create = MagicMock()

            result = usecase.generate_current_period_report()

            self.assertIsNone(result)
            usecase.incomplete_sheet_report_repository.create.assert_not_called()

        with self.subTest("今期が存在する場合はレポートを作成する"):
            period_uuid = uuid4()
            rows = [
                IncompleteSheetRowModel(
                    sheet_uuid=uuid4(),
                    employee_uuid=uuid4(),
                    employee_code="E001",
                    employee_name="Alice",
                    own_status=EvaluationSheetStatusEnum.PENDING,
                    manager_status=EvaluationSheetStatusEnum.COMPLETED,
                )
            ]
            captured_report = {"value": None}

            def capture(report):
                captured_report["value"] = report
                return report

            usecase = IncompleteSheetReportUsecase()
            usecase.period_query_service.get_list = MagicMock(
                return_value=PeriodListModel(
                    periods=[], current_period_uuid=period_uuid
                )
            )
            usecase.evaluation_sheet_query_service.get_incomplete_by_period = (
                MagicMock(return_value=rows)
            )
            usecase.incomplete_sheet_report_repository.create = MagicMock(
                side_effect=capture
            )

            result = usecase.generate_current_period_report()

            self.assertIsNotNone(result)
            report = captured_report["value"]
            if report is None:
                raise ValueError("レポートが作成されていません。")
            self.assertEqual(report.period_uuid, period_uuid)
            self.assertEqual(report.total, 1)
            self.assertEqual(report.payload[0]["employee_code"], "E001")
