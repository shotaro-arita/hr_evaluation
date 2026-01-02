from abc import ABC, abstractmethod
from uuid import UUID

from evaluations.domain.employee.entity import PositionEnum


class EvaluationItemPositionRelationRepository(ABC):
    @abstractmethod
    def find_item_ids_by_position(self, position: PositionEnum) -> list[UUID]:
        raise NotImplementedError
