from django.core.exceptions import ValidationError
from django.db import models

from evaluations.domain.employee.entity import Employee, JobTypeEnum, PositionEnum
from evaluations.models.model_fields import ChoiceField


class EmployeeManager(models.Manager["DbEmployee"]):
    def get_queryset(self) -> models.QuerySet["DbEmployee"]:
        return super().get_queryset().prefetch_related()


class DbEmployee(models.Model):
    uuid = models.UUIDField(primary_key=True)
    employee_code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    position = ChoiceField(max_length=2, choices=PositionEnum.choices())
    job_type = ChoiceField(max_length=2, choices=JobTypeEnum.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EmployeeManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.employee_code}{self.name}"

    def to_entity(self) -> Employee:
        return Employee(
            uuid=self.uuid,
            employee_code=self.employee_code,
            name=self.name,
            position=PositionEnum(self.position),
            job_type=JobTypeEnum(self.job_type),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        """
        adminでの更新時にentityのvalidationを効かせる。
        """
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e
