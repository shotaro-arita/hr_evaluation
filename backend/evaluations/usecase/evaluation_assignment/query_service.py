from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from evaluations.domain.user.entity import User


@dataclass(frozen=True)
class ManagerTargetModel:
    employee_uuid: UUID
    employee_code: str
    name: str
    position: str
    job_type: str
    role: str


class EvaluationAssignmentQueryService(ABC):
    @abstractmethod
    def get_manager_targets(self, user: User) -> list[ManagerTargetModel]:
        raise NotImplementedError
