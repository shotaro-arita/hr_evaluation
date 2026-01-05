from django.core.exceptions import ValidationError
from django.db import models

from evaluations.domain.period.entity import Period


class PeriodManager(models.Manager["DbPeriod"]):
    def get_queryset(self) -> models.QuerySet["DbPeriod"]:
        return super().get_queryset().prefetch_related()


class DbPeriod(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PeriodManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def to_entity(self) -> Period:
        return Period(
            uuid=self.uuid,
            name=self.name,
            start_date=self.start_date,
            end_date=self.end_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def clean(self) -> None:
        # Validate via entity in admin updates.
        try:
            self.to_entity()
        except Exception as e:
            raise ValidationError(str(e)) from e
