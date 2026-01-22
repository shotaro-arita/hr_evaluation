from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
    EvaluationSheetRawModel,
)
from evaluations.usecase.evaluation_assignment.query_service import (
    EvaluationAssignmentQueryService,
    ManagerTargetModel,
)
from evaluations.usecase.evaluation_weight_policy.query_service import (
    EvaluationWeightPolicyListModel,
    EvaluationWeightPolicyQueryService,
)
from evaluations.usecase.period.query_service import PeriodListModel, PeriodQueryService
from evaluations.usecase.user.query_service import UserQueryService, UserRetrieveModel
from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.user.entity import User
from datetime import datetime
from uuid import UUID


class EvaluationSheetQueryServiceMock(EvaluationSheetQueryService):
    def find_by_id(self, user: User, id: UUID) -> EvaluationSheetRawModel | None:
        raise NotImplementedError

    def get_list_by_employee_id(
        self, user: User, employee_id: UUID
    ) -> list[EvaluationSheetRawModel]:
        raise NotImplementedError


class UserQueryServiceMock(UserQueryService):
    def get_user(self, user: User) -> UserRetrieveModel | None:
        raise NotImplementedError


class EvaluationAssignmentQueryServiceMock(EvaluationAssignmentQueryService):
    def get_manager_targets(self, user: User) -> list[ManagerTargetModel]:
        raise NotImplementedError


class EvaluationWeightPolicyQueryServiceMock(EvaluationWeightPolicyQueryService):
    def get_weights(
        self, user: User, period_id: UUID, position: PositionEnum
    ) -> EvaluationWeightPolicyListModel:
        raise NotImplementedError


class PeriodQueryServiceMock(PeriodQueryService):
    def get_list(self, user: User, now: datetime) -> PeriodListModel:
        raise NotImplementedError
