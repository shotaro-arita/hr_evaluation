from typing import cast

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from evaluations.models.user import DbUser
from evaluations.domain.user.entity import User


def to_user_entity(user: AbstractBaseUser | AnonymousUser) -> User:
    if isinstance(user, AnonymousUser):
        raise ValueError("User is AnonymousUser")
    return cast(DbUser, user).to_entity
