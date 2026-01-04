from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
    EvaluationSheetRetrieveModel,
)
from uuid import UUID


class EvaluationSheetQueryServiceMock(EvaluationSheetQueryService):
    def find_by_id(self, id: UUID) -> EvaluationSheetRetrieveModel | None:
        raise NotImplementedError

    def get_list_by_employee_id(
        self, employee_id: UUID
    ) -> list[EvaluationSheetRetrieveModel]:
        raise NotImplementedError
