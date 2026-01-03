from dataclasses import dataclass, field
from evaluations.domain.evaluation_sheet.entity import (
    EvaluationSheet,
    EvaluationSheetScore,
    EvaluationSheetStatus,
)
from django.utils.crypto import get_random_string as django_get_random_string
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class Counter:
    count = 0

    @classmethod
    def get(cls) -> int:
        cls.count += 1
        return cls.count

    @classmethod
    def reset(cls) -> None:
        cls.count = 0


def get_random_string() -> str:
    return django_get_random_string(12)


@dataclass(frozen=True)
class EvaluationSheetFactory(EvaluationSheet):
    uuid: UUID = field(default_factory=uuid4)
    period_uuid: UUID = field(default_factory=uuid4)
    employee_uuid: UUID = field(default_factory=uuid4)
    own_scores: list[EvaluationSheetScore] = field(default_factory=list)
    manager_scores: list[EvaluationSheetScore] = field(default_factory=list)
    status: EvaluationSheetStatus = EvaluationSheetStatus.PENDING
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True)
class EvaluationSheetScoreFactory(EvaluationSheetScore):
    uuid: UUID = field(default_factory=uuid4)
    evaluation_item_uuid: UUID = field(default_factory=uuid4)
    score: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
