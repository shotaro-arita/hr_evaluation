from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from evaluations.domain.user.entity import User


@dataclass(frozen=True)
class PeriodModel:
    uuid: UUID
    name: str
    start_date: datetime
    end_date: datetime
    is_current: bool


@dataclass(frozen=True)
class PeriodListModel:
    periods: list[PeriodModel]
    current_period_uuid: UUID | None


class PeriodQueryService(ABC):
    @abstractmethod
    def get_list(self, user: User, now: datetime) -> PeriodListModel:
        raise NotImplementedError
