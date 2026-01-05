import sys
from typing import Any, TypeVar

from django.db import models


# https://github.com/typeddjango/django-stubs/issues/285
# __set__ value type
_ST = TypeVar("_ST")
# __get__ return type
_GT = TypeVar("_GT")


# class ChoiceField(models.CharField[T, T], Generic[T]):
class ChoiceField(models.CharField):
    """
    choiceの制御はdb上ではなく、application上で行なっていること。
    makemigrationsの時のみchoicesを無効化する。
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        if "makemigrations" in sys.argv:
            self.choices = None
