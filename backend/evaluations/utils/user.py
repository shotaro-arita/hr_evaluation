from django.contrib.auth.models import AbstractBaseUser

from evaluations.domain.user.entity import User


def to_user_entity(user: AbstractBaseUser) -> User:
    return User(
        uuid=user.pk,
        employee_uuid=user.employee_id,
        employee_code=user.employee_code,
        password=user.password,
        is_active=user.is_active,
        name=user.name,
    )
