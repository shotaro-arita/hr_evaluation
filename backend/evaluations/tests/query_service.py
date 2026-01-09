from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
    EvaluationSheetRetrieveModel,
)
from evaluations.domain.user.entity import User
from uuid import UUID


class EvaluationSheetQueryServiceMock(EvaluationSheetQueryService):
    def find_by_id(self, user: User, id: UUID) -> EvaluationSheetRetrieveModel | None:
        raise NotImplementedError

    def get_list_by_employee_id(
        self, user: User, employee_id: UUID
    ) -> list[EvaluationSheetRetrieveModel]:
        raise NotImplementedError
