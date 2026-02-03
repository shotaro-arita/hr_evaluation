from inject import Binder

from evaluations.infrastructure.query_service.evaluation_sheet import (
    EvaluationSheetQueryServiceImpl,
)
from evaluations.infrastructure.query_service.evaluation_assignment import (
    EvaluationAssignmentQueryServiceImpl,
)
from evaluations.infrastructure.query_service.period import PeriodQueryServiceImpl
from evaluations.infrastructure.query_service.user import UserQueryServiceImpl
from evaluations.infrastructure.query_service.evaluation_weight_policy import (
    EvaluationWeightPolicyQueryServiceImpl,
)
from evaluations.infrastructure.repository.employee import (
    EmployeeRepositoryImpl,
)
from evaluations.infrastructure.repository.evaluation_assignment_repository import (
    EvaluationAssignmentRepositoryImpl,
)
from evaluations.infrastructure.repository.evaluation_item_position_relation import (
    EvaluationItemPositionRelationRepositoryImpl,
)
from evaluations.infrastructure.repository.evaluation_sheet import (
    EvaluationSheetRepositoryImpl,
)
from evaluations.infrastructure.repository.incomplete_sheet_report import (
    IncompleteSheetReportRepositoryImpl,
)
from evaluations.usecase.evaluation_sheet.query_service import (
    EvaluationSheetQueryService,
)
from evaluations.usecase.evaluation_assignment.query_service import (
    EvaluationAssignmentQueryService,
)
from evaluations.usecase.period.query_service import PeriodQueryService
from evaluations.usecase.user.query_service import UserQueryService
from evaluations.usecase.evaluation_weight_policy.query_service import (
    EvaluationWeightPolicyQueryService,
)


from evaluations.domain.employee.repository import EmployeeRepository
from evaluations.domain.evaluation_assignment.repository import (
    EvaluationAssignmentRepository,
)
from evaluations.domain.evaluation_item_position_relation.repository import (
    EvaluationItemPositionRelationRepository,
)
from evaluations.domain.evaluation_sheet.repository import EvaluationSheetRepository
from evaluations.domain.incomplete_sheet_report.repository import (
    IncompleteSheetReportRepository,
)


def injection_config(binder: Binder) -> None:
    # Repository
    binder.bind(EvaluationSheetRepository, EvaluationSheetRepositoryImpl())
    binder.bind(EmployeeRepository, EmployeeRepositoryImpl())
    binder.bind(EvaluationAssignmentRepository, EvaluationAssignmentRepositoryImpl())
    binder.bind(
        EvaluationItemPositionRelationRepository,
        EvaluationItemPositionRelationRepositoryImpl(),
    )
    binder.bind(
        IncompleteSheetReportRepository, IncompleteSheetReportRepositoryImpl()
    )

    # QueryService
    binder.bind(EvaluationSheetQueryService, EvaluationSheetQueryServiceImpl())
    binder.bind(
        EvaluationAssignmentQueryService, EvaluationAssignmentQueryServiceImpl()
    )
    binder.bind(
        EvaluationWeightPolicyQueryService, EvaluationWeightPolicyQueryServiceImpl()
    )
    binder.bind(PeriodQueryService, PeriodQueryServiceImpl())
    binder.bind(UserQueryService, UserQueryServiceImpl())
