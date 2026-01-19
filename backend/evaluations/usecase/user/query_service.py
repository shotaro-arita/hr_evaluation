from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from evaluations.domain.user.entity import User


@dataclass(frozen=True)
class UserRetrieveModel:
    user_uuid: UUID
    employee_uuid: UUID
    employee_code: str
    name: str
    position: str
    job_type: str
    is_manager: bool
    manager_target_count: int


class UserQueryService(ABC):
    @abstractmethod
    def get_user(self, user: User) -> UserRetrieveModel | None:
        raise NotImplementedError
