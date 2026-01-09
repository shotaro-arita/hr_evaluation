from abc import ABC, abstractmethod
from uuid import UUID

from evaluations.domain.evaluation_sheet.entity import EvaluationSheet
from evaluations.domain.user.entity import User


class EvaluationSheetRepository(ABC):
    @abstractmethod
    def find_by_id(self, user: User, id: UUID) -> EvaluationSheet | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_employee_period(
        self, user: User, employee_id: UUID, period_id: UUID
    ) -> EvaluationSheet | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, evaluation_sheet: EvaluationSheet) -> EvaluationSheet:
        raise NotImplementedError

    @abstractmethod
    def update(self, evaluation_sheet: EvaluationSheet) -> EvaluationSheet:
        raise NotImplementedError
