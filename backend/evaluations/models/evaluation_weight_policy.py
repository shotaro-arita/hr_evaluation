from django.core.exceptions import ValidationError
from django.db import models

from evaluations.domain.employee.entity import PositionEnum
from evaluations.domain.evaluation_item.entity import EvaluationItemCategory
from evaluations.domain.evaluation_weight_policy.entity import EvaluationWeightPolicy
from evaluations.models.model_fields import ChoiceField
from evaluations.models.period import DbPeriod


class DbEvaluationWeightPolicy(models.Model):
    uuid = models.UUIDField(primary_key=True)
    period = models.ForeignKey(
        DbPeriod, on_delete=models.CASCADE, related_name="weight_policies"
    )
    position = ChoiceField(max_length=2, choices=PositionEnum.choices())
    category = ChoiceField(max_length=32, choices=EvaluationItemCategory.choices())
    weight = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["period", "position", "category"],
                name="unique_weight_policy_period_position_category",
            )
        ]

    def __str__(self) -> str:
        return f"{self.period_id}:{self.position}:{self.category}"

    def to_entity(self) -> EvaluationWeightPolicy:
        return EvaluationWeightPolicy(
            uuid=self.uuid,
            period_uuid=self.period_id,
            position=PositionEnum(self.position),
            category=EvaluationItemCategory(self.category),
            weight=self.weight,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e
