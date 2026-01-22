from inject import Binder


from evaluations.domain.employee.repository import EmployeeRepository
from evaluations.domain.evaluation_assignment.repository import (
    EvaluationAssignmentRepository,
)
from evaluations.domain.evaluation_item_position_relation.repository import (
    EvaluationItemPositionRelationRepository,
)
from evaluations.domain.evaluation_sheet.repository import (
    EvaluationSheetRepository,
)
from evaluations.tests.repository import (
    EmployeeRepositoryMock,
    EvaluationAssignmentRepositoryMock,
    EvaluationItemPositionRelationRepositoryMock,
    EvaluationSheetRepositoryMock,
)
from evaluations.tests.query_service import (
    EvaluationAssignmentQueryServiceMock,
    EvaluationSheetQueryServiceMock,
    EvaluationWeightPolicyQueryServiceMock,
    PeriodQueryServiceMock,
    UserQueryServiceMock,
)
from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
)
from evaluations.usecase.evaluation_assignment.query_service import (
    EvaluationAssignmentQueryService,
)
from evaluations.usecase.evaluation_weight_policy.query_service import (
    EvaluationWeightPolicyQueryService,
)
from evaluations.usecase.period.query_service import PeriodQueryService
from evaluations.usecase.user.query_service import UserQueryService


def mock_injection_config(binder: Binder) -> None:
    # repository
    binder.bind(EvaluationSheetRepository, EvaluationSheetRepositoryMock)
    binder.bind(EmployeeRepository, EmployeeRepositoryMock)
    binder.bind(EvaluationAssignmentRepository, EvaluationAssignmentRepositoryMock)
    binder.bind(
        EvaluationItemPositionRelationRepository,
        EvaluationItemPositionRelationRepositoryMock,
    )

    # query_service
    binder.bind(EvaluationSheetQueryService, EvaluationSheetQueryServiceMock)
    binder.bind(
        EvaluationAssignmentQueryService, EvaluationAssignmentQueryServiceMock
    )
    binder.bind(
        EvaluationWeightPolicyQueryService, EvaluationWeightPolicyQueryServiceMock
    )
    binder.bind(PeriodQueryService, PeriodQueryServiceMock)
    binder.bind(UserQueryService, UserQueryServiceMock)
