from uuid import uuid4
from typing import Any, Generic, TypeVar
from datetime import timedelta

import factory

from evaluations.domain.employee.entity import JobTypeEnum, PositionEnum
from evaluations.domain.evaluation_assignment.entity import AssignmentRoleEnum
from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.evaluation_sheet.entity import EvaluationSheetStatusEnum
from evaluations.models.employee import DbEmployee
from evaluations.models.evaluation_assignment import DbEvaluationAssignment
from evaluations.models.evaluation_item import DbEvaluationItem
from evaluations.models.evaluation_item_position_relation import (
    DbEvaluationItemPositionRelation,
)
from evaluations.models.evaluation_sheet import (
    DbEvaluationSheet,
    DbEvaluationSheetScore,
)
from evaluations.models.period import DbPeriod
from evaluations.models.user import DbUser
from evaluations.tests.utils.entity_factory import (
    Counter,
    get_random_datetime,
    get_random_string,
)


T = TypeVar("T")


# https://github.com/FactoryBoy/factory_boy/issues/468
class BaseFactory(factory.django.DjangoModelFactory, Generic[T]):
    @classmethod
    def create(cls, **kwargs: Any) -> T:
        return super().create(**kwargs)


class DbEmployeeFactory(BaseFactory[DbEmployee]):
    class Meta:
        model = DbEmployee

    uuid = factory.LazyFunction(uuid4)
    employee_code = factory.LazyFunction(get_random_string)
    name = factory.LazyFunction(get_random_string)
    position = factory.LazyFunction(lambda: list(PositionEnum).pop())
    job_type = factory.LazyFunction(lambda: list(JobTypeEnum).pop())
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)


class DbEvaluationItemFactory(BaseFactory[DbEvaluationItem]):
    class Meta:
        model = DbEvaluationItem

    uuid = factory.LazyFunction(uuid4)
    title = factory.LazyFunction(get_random_string)
    category = factory.LazyFunction(lambda: list(EvaluationItemCategory).pop())
    description = factory.LazyFunction(get_random_string)
    criteria_1 = factory.LazyFunction(get_random_string)
    criteria_2 = factory.LazyFunction(get_random_string)
    criteria_3 = factory.LazyFunction(get_random_string)
    criteria_4 = factory.LazyFunction(get_random_string)
    criteria_5 = factory.LazyFunction(get_random_string)
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)


class DbEvaluationItemPositionRelationFactory(
    BaseFactory[DbEvaluationItemPositionRelation]
):
    class Meta:
        model = DbEvaluationItemPositionRelation

    uuid = factory.LazyFunction(uuid4)
    position = factory.LazyFunction(lambda: list(PositionEnum).pop())
    evaluation_item = factory.SubFactory(DbEvaluationItemFactory)
    order = factory.LazyFunction(Counter.get)
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)


class DbEvaluationAssignmentFactory(BaseFactory[DbEvaluationAssignment]):
    class Meta:
        model = DbEvaluationAssignment

    uuid = factory.LazyFunction(uuid4)
    target_employee = factory.SubFactory(DbEmployeeFactory)
    manager_employee = factory.SubFactory(DbEmployeeFactory)
    role = factory.LazyFunction(lambda: list(AssignmentRoleEnum).pop())
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)


class DbPeriodFactory(BaseFactory[DbPeriod]):
    class Meta:
        model = DbPeriod

    uuid = factory.LazyFunction(uuid4)
    name = factory.LazyFunction(get_random_string)
    start_date = factory.LazyFunction(get_random_datetime)
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=30))
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)


class DbEvaluationSheetFactory(BaseFactory[DbEvaluationSheet]):
    class Meta:
        model = DbEvaluationSheet

    uuid = factory.LazyFunction(uuid4)
    period = factory.SubFactory(DbPeriodFactory)
    employee = factory.SubFactory(DbEmployeeFactory)
    status = EvaluationSheetStatusEnum.PENDING
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)


class DbEvaluationSheetScoreFactory(BaseFactory[DbEvaluationSheetScore]):
    class Meta:
        model = DbEvaluationSheetScore

    uuid = factory.LazyFunction(uuid4)
    evaluation_sheet = factory.SubFactory(DbEvaluationSheetFactory)
    evaluation_item = factory.SubFactory(DbEvaluationItemFactory)
    score = factory.LazyFunction(lambda: Counter.get() % 5 + 1)
    is_manager = False
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)


class DbUserFactory(BaseFactory[DbUser]):
    class Meta:
        model = DbUser

    uuid = factory.LazyFunction(uuid4)
    employee = factory.SubFactory(DbEmployeeFactory)
    employee_code = factory.LazyFunction(get_random_string)
    name = factory.LazyFunction(get_random_string)
    password = factory.LazyFunction(get_random_string)
    is_staff = False
    is_active = True
    created_at = factory.LazyFunction(get_random_datetime)
    updated_at = factory.LazyFunction(get_random_datetime)
