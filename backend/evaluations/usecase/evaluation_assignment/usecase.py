import inject

from evaluations.domain.user.entity import User
from evaluations.usecase.evaluation_assignment.query_service import (
    EvaluationAssignmentQueryService,
    ManagerTargetModel,
)


class EvaluationAssignmentUsecase:
    @inject.autoparams()
    def __init__(
        self, evaluation_assignment_query_service: EvaluationAssignmentQueryService
    ):
        self.evaluation_assignment_query_service = evaluation_assignment_query_service

    def get_manager_targets(self, request_user: User) -> list[ManagerTargetModel]:
        return self.evaluation_assignment_query_service.get_manager_targets(
            request_user
        )
