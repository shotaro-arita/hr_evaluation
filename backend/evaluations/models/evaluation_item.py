from django.core.exceptions import ValidationError
from django.db import models

from evaluations.domain.evaluation_item.entity import (
    EvaluationItem,
    EvaluationItemCategory,
)
from evaluations.models.model_fields import ChoiceField


def _category_choices() -> list[tuple[str, str]]:
    return [(category.value, category.text) for category in EvaluationItemCategory]


class EvaluationItemManager(models.Manager["DbEvaluationItem"]):
    def get_queryset(self) -> models.QuerySet["DbEvaluationItem"]:
        return super().get_queryset().prefetch_related()


class DbEvaluationItem(models.Model):
    uuid = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    category = ChoiceField(max_length=32, choices=_category_choices())
    description = models.TextField()
    criteria_1 = models.TextField()
    criteria_2 = models.TextField()
    criteria_3 = models.TextField()
    criteria_4 = models.TextField()
    criteria_5 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EvaluationItemManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def to_entity(self) -> EvaluationItem:
        return EvaluationItem(
            uuid=self.uuid,
            title=self.title,
            category=EvaluationItemCategory(self.category),
            description=self.description,
            criteria_1=self.criteria_1,
            criteria_2=self.criteria_2,
            criteria_3=self.criteria_3,
            criteria_4=self.criteria_4,
            criteria_5=self.criteria_5,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        # Validate via entity in admin updates.
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e
