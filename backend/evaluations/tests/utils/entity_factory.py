from dataclasses import dataclass, field
from evaluations.domain.employee.entity import Employee, JobTypeEnum, PositionEnum
from evaluations.domain.evaluation_assignment.entity import (
    AssignmentRoleEnum,
    EvaluationAssignment,
)
from evaluations.domain.evaluation_sheet.entity import (
    EvaluationSheet,
    EvaluationSheetScore,
    EvaluationSheetStatusEnum,
)
from evaluations.domain.user.entity import User
from django.utils.crypto import get_random_string as django_get_random_string
from faker import Faker
from dateutil.tz import gettz
from django.conf import settings
from datetime import datetime
from uuid import UUID, uuid4


fake = Faker()


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


def get_random_datetime() -> datetime:
    d: datetime = fake.date_time_between()
    localized = d.astimezone(gettz(settings.TIME_ZONE))
    return localized


@dataclass(frozen=True)
class EvaluationSheetFactory(EvaluationSheet):
    uuid: UUID = field(default_factory=uuid4)
    period_uuid: UUID = field(default_factory=uuid4)
    employee_uuid: UUID = field(default_factory=uuid4)
    own_scores: list[EvaluationSheetScore] = field(default_factory=list)
    manager_scores: list[EvaluationSheetScore] = field(default_factory=list)
    status: EvaluationSheetStatusEnum = EvaluationSheetStatusEnum.PENDING
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True)
class EvaluationSheetScoreFactory(EvaluationSheetScore):
    uuid: UUID = field(default_factory=uuid4)
    evaluation_item_uuid: UUID = field(default_factory=uuid4)
    score: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True)
class EmployeeFactory(Employee):
    uuid: UUID = field(default_factory=uuid4)
    employee_code: str = field(default_factory=get_random_string)
    name: str = field(default_factory=get_random_string)
    position: PositionEnum = PositionEnum.JUNIOR
    job_type: JobTypeEnum = JobTypeEnum.SOFTWARE_DEVELOPMENT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class EvaluationAssignmentFactory(EvaluationAssignment):
    uuid: UUID = field(default_factory=uuid4)
    target_employee_uuid: UUID = field(default_factory=uuid4)
    manager_employee_uuid: UUID = field(default_factory=uuid4)
    role: AssignmentRoleEnum = AssignmentRoleEnum.MANAGER
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class UserFactory(User):
    uuid: UUID = field(default_factory=uuid4)
    employee_uuid: UUID = field(default_factory=uuid4)
    employee_code: str = field(default_factory=get_random_string)
    password: str = field(default_factory=get_random_string)
    is_active: bool = True
    name: str = field(default_factory=get_random_string)
