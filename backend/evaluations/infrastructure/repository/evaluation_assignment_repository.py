from uuid import UUID

from evaluations.models.evaluation_assignment import DbEvaluationAssignment
from evaluations.domain.evaluation_assignment.entity import EvaluationAssignment
from evaluations.domain.evaluation_assignment.repository import (
    EvaluationAssignmentRepository,
)


class EvaluationAssignmentRepositoryImpl(EvaluationAssignmentRepository):
    def find_by_target_employee_id(
        self, target_employee_id: UUID
    ) -> EvaluationAssignment | None:
        try:
            employee_model = DbEvaluationAssignment.objects.get(
                target_employee_uuid=target_employee_id
            )
        except DbEvaluationAssignment.DoesNotExist:
            return None
        return employee_model.to_entity()
