import inject
from inject import Binder


from evaluations.domain.employee.repository import EmployeeRepository
from evaluations.domain.evaluation_assignment.repository import (
    EvaluationAssignmentRepository,
)
from evaluations.domain.evaluation_item_position_relation.repository import (
    EvaluationItemPositionRelationRepository,
)
from evaluations.domain.evaluation_sheet.repository import EvaluationSheetRepository


def injection_config(binder: Binder) -> None:
    pass
    # binder.bind(
    #     EvaluationSheetRepository,
    # )
    # binder.bind(
    #     EmployeeRepository,
    # )
    # binder.bind(
    #     EvaluationAssignmentRepository,
    # )
    # binder.bind(
    #     EvaluationItemPositionRelationRepository,
    # )
