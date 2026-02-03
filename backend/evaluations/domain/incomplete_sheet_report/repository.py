from abc import ABC, abstractmethod

from evaluations.domain.incomplete_sheet_report.entity import (
    IncompleteSheetReport,
)


class IncompleteSheetReportRepository(ABC):
    @abstractmethod
    def create(self, report: IncompleteSheetReport) -> IncompleteSheetReport:
        raise NotImplementedError
