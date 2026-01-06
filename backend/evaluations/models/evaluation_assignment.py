from django.core.exceptions import ValidationError
from django.db import models

from evaluations.domain.evaluation_assignment.entity import (
    AssignmentRoleEnum,
    EvaluationAssignment,
)
from evaluations.models.employee import DbEmployee
from evaluations.models.model_fields import ChoiceField


class EvaluationAssignmentManager(models.Manager["DbEvaluationAssignment"]):
    def get_queryset(self) -> models.QuerySet["DbEvaluationAssignment"]:
        return super().get_queryset().prefetch_related()


class DbEvaluationAssignment(models.Model):
    uuid = models.UUIDField(primary_key=True)
    target_employee = models.OneToOneField(
        DbEmployee, on_delete=models.CASCADE, related_name="evaluation_targets"
    )
    manager_employee = models.ForeignKey(
        DbEmployee, on_delete=models.CASCADE, related_name="evaluation_managers"
    )
    role = ChoiceField(max_length=16, choices=AssignmentRoleEnum.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EvaluationAssignmentManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.target_employee_id}:{self.manager_employee_id}"

    def to_entity(self) -> EvaluationAssignment:
        return EvaluationAssignment(
            uuid=self.uuid,
            target_employee_uuid=self.target_employee_id,
            manager_employee_uuid=self.manager_employee_id,
            role=AssignmentRoleEnum(self.role),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        # Validate via entity in admin updates.
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e
