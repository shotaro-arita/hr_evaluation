from uuid import UUID

from evaluations.domain.evaluation_item_position_relation.repository import (
    EvaluationItemPositionRelationRepository,
)
from evaluations.domain.evaluation_assignment.repository import (
    EvaluationAssignmentRepository,
)
from evaluations.domain.employee.repository import EmployeeRepository
from evaluations.domain.evaluation_sheet.entity import EvaluationSheet
from evaluations.domain.evaluation_sheet.repository import EvaluationSheetRepository
from evaluations.domain.employee.entity import Employee
from evaluations.domain.evaluation_assignment.entity import EvaluationAssignment
from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.user.entity import User


class EvaluationSheetRepositoryMock(EvaluationSheetRepository):
    def find_by_id(self, user: User, id: UUID) -> EvaluationSheet | None:
        raise NotImplementedError

    def get_by_employee_period(
        self, user: User, employee_id: UUID, period_id: UUID
    ) -> EvaluationSheet:
        raise NotImplementedError

    def create(self, evaluation_sheet: EvaluationSheet) -> EvaluationSheet:
        return evaluation_sheet

    def update(self, evaluation_sheet: EvaluationSheet) -> EvaluationSheet:
        return evaluation_sheet


class EmployeeRepositoryMock(EmployeeRepository):
    def find_by_id(self, id: UUID) -> Employee | None:
        raise NotImplementedError


class EvaluationAssignmentRepositoryMock(EvaluationAssignmentRepository):
    def find_by_target_employee_id(
        self, target_employee_id: UUID
    ) -> EvaluationAssignment | None:
        raise NotImplementedError


class EvaluationItemPositionRelationRepositoryMock(
    EvaluationItemPositionRelationRepository
):
    def find_item_ids_by_position(self, position: PositionEnum) -> list[UUID]:
        raise NotImplementedError
