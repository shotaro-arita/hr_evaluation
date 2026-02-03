from uuid import uuid4

import inject
from django.utils import timezone

from evaluations.domain.incomplete_sheet_report.entity import (
    IncompleteSheetReport,
)
from evaluations.domain.incomplete_sheet_report.repository import (
    IncompleteSheetReportRepository,
)
from evaluations.domain.user.entity import User
from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
)
from evaluations.usecase.period.query_service import PeriodQueryService


class IncompleteSheetReportUsecase:
    @inject.autoparams()
    def __init__(
        self,
        evaluation_sheet_query_service: EvaluationSheetQueryService,
        period_query_service: PeriodQueryService,
        incomplete_sheet_report_repository: IncompleteSheetReportRepository,
    ):
        self.evaluation_sheet_query_service = evaluation_sheet_query_service
        self.period_query_service = period_query_service
        self.incomplete_sheet_report_repository = (
            incomplete_sheet_report_repository
        )

    def _system_user(self) -> User:
        return User(
            uuid=uuid4(),
            employee_uuid=uuid4(),
            employee_code="SYSTEM",
            password="",
            is_active=True,
            name="SYSTEM",
        )

    def generate_current_period_report(self) -> str | None:
        now = timezone.now()
        period_list = self.period_query_service.get_list(self._system_user(), now)
        current_period_uuid = period_list.current_period_uuid
        if current_period_uuid is None:
            return None

        rows = self.evaluation_sheet_query_service.get_incomplete_by_period(
            self._system_user(), current_period_uuid
        )
        payload = [
            {
                "sheet_uuid": str(row.sheet_uuid),
                "employee_uuid": str(row.employee_uuid),
                "employee_code": row.employee_code,
                "employee_name": row.employee_name,
                "own_status": row.own_status.value,
                "manager_status": row.manager_status.value,
            }
            for row in rows
        ]

        report = IncompleteSheetReport(
            uuid=uuid4(),
            period_uuid=current_period_uuid,
            total=len(payload),
            payload=payload,
            created_at=None,
        )
        report = self.incomplete_sheet_report_repository.create(report)
        return str(report.uuid)
