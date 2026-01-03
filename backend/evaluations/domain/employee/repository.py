from abc import ABC, abstractmethod
from uuid import UUID

from evaluations.domain.employee.entity import Employee


class EmployeeRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: UUID) -> Employee | None:
        raise NotImplementedError
