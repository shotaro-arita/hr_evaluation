from evaluations.domain.incomplete_sheet_report.entity import (
    IncompleteSheetReport,
)
from evaluations.domain.incomplete_sheet_report.repository import (
    IncompleteSheetReportRepository,
)
from evaluations.models.incomplete_sheet_report import DbIncompleteSheetReport
from evaluations.models.period import DbPeriod


class IncompleteSheetReportRepositoryImpl(IncompleteSheetReportRepository):
    def create(self, report: IncompleteSheetReport) -> IncompleteSheetReport:
        period = DbPeriod.objects.get(uuid=report.period_uuid)
        model = DbIncompleteSheetReport.objects.create(
            uuid=report.uuid,
            period=period,
            total=report.total,
            payload=report.payload,
        )
        return model.to_entity()
