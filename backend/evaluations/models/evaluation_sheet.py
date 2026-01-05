from django.core.exceptions import ValidationError
from django.db import models

from evaluations.domain.evaluation_sheet.entity import (
    EvaluationSheet,
    EvaluationSheetScore,
    EvaluationSheetStatusEnum,
)
from evaluations.models.model_fields import ChoiceField


class EvaluationSheetManager(models.Manager["DbEvaluationSheet"]):
    def get_queryset(self) -> models.QuerySet["DbEvaluationSheet"]:
        return super().get_queryset().prefetch_related("scores")


class EvaluationSheetScoreManager(models.Manager["DbEvaluationSheetScore"]):
    def get_queryset(self) -> models.QuerySet["DbEvaluationSheetScore"]:
        return super().get_queryset().prefetch_related()


class DbEvaluationSheet(models.Model):
    uuid = models.UUIDField(primary_key=True)
    period_uuid = models.UUIDField()
    employee_uuid = models.UUIDField()
    status = ChoiceField(max_length=32, choices=EvaluationSheetStatusEnum.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EvaluationSheetManager()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["period_uuid", "employee_uuid"],
                name="unique_evaluation_sheet_period_employee",
            )
        ]

    def __str__(self) -> str:
        return str(self.uuid)

    def to_entity(self) -> EvaluationSheet:
        scores = list(self.scores.all())
        own_scores = [score.to_entity() for score in scores if not score.is_manager]
        manager_scores = [score.to_entity() for score in scores if score.is_manager]
        return EvaluationSheet(
            uuid=self.uuid,
            period_uuid=self.period_uuid,
            employee_uuid=self.employee_uuid,
            own_scores=own_scores,
            manager_scores=manager_scores,
            status=EvaluationSheetStatusEnum(self.status),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        # Validate via entity in admin updates.
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e


class DbEvaluationSheetScore(models.Model):
    uuid = models.UUIDField(primary_key=True)
    evaluation_sheet = models.ForeignKey(
        DbEvaluationSheet, on_delete=models.CASCADE, related_name="scores"
    )
    evaluation_item_uuid = models.UUIDField()
    score = models.IntegerField(null=True)
    is_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EvaluationSheetScoreManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.evaluation_sheet_id}:{self.evaluation_item_uuid}"

    def to_entity(self) -> EvaluationSheetScore:
        return EvaluationSheetScore(
            uuid=self.uuid,
            evaluation_item_uuid=self.evaluation_item_uuid,
            score=self.score,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        # Validate via entity in admin updates.
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e
