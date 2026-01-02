from abc import ABC, abstractmethod
from uuid import UUID

from evaluations.domain.evaluation_assignment.entity import EvaluationAssignment


class EvaluationAssignmentRepository(ABC):
    @abstractmethod
    def find_by_target_employee_id(
        self, target_employee_id: UUID
    ) -> EvaluationAssignment | None:
        raise NotImplementedError
