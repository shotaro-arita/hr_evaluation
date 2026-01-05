from django.core.exceptions import ValidationError
from django.db import models

from evaluations.domain.evaluation_item_position_relation.entity import (
    EvaluationItemPositionRelation,
)
from evaluations.domain.employee.entity import PositionEnum
from evaluations.models.model_fields import ChoiceField


class EvaluationItemPositionRelationManager(
    models.Manager["DbEvaluationItemPositionRelation"]
):
    def get_queryset(self) -> models.QuerySet["DbEvaluationItemPositionRelation"]:
        return super().get_queryset().prefetch_related()


class DbEvaluationItemPositionRelation(models.Model):
    uuid = models.UUIDField(primary_key=True)
    position = ChoiceField(max_length=2, choices=PositionEnum.choices())
    evaluation_item_uuid = models.UUIDField()
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EvaluationItemPositionRelationManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.position}:{self.order}"

    def to_entity(self) -> EvaluationItemPositionRelation:
        return EvaluationItemPositionRelation(
            uuid=self.uuid,
            position=PositionEnum(self.position),
            evaluation_item_uuid=self.evaluation_item_uuid,
            order=self.order,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        # Validate via entity in admin updates.
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e
