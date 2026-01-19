from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
    EvaluationSheetRetrieveModel,
)
from evaluations.usecase.evaluation_assignment.query_service import (
    EvaluationAssignmentQueryService,
    ManagerTargetModel,
)
from evaluations.usecase.period.query_service import PeriodListModel, PeriodQueryService
from evaluations.usecase.user.query_service import UserQueryService, UserRetrieveModel
from evaluations.domain.user.entity import User
from datetime import datetime
from uuid import UUID


class EvaluationSheetQueryServiceMock(EvaluationSheetQueryService):
    def find_by_id(self, user: User, id: UUID) -> EvaluationSheetRetrieveModel | None:
        raise NotImplementedError

    def get_list_by_employee_id(
        self, user: User, employee_id: UUID
    ) -> list[EvaluationSheetRetrieveModel]:
        raise NotImplementedError


class UserQueryServiceMock(UserQueryService):
    def get_user(self, user: User) -> UserRetrieveModel | None:
        raise NotImplementedError


class EvaluationAssignmentQueryServiceMock(EvaluationAssignmentQueryService):
    def get_manager_targets(self, user: User) -> list[ManagerTargetModel]:
        raise NotImplementedError


class PeriodQueryServiceMock(PeriodQueryService):
    def get_list(self, user: User, now: datetime) -> PeriodListModel:
        raise NotImplementedError
