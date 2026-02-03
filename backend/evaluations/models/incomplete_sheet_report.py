from django.db import models

from evaluations.domain.incomplete_sheet_report.entity import IncompleteSheetReport
from evaluations.models.period import DbPeriod


class DbIncompleteSheetReport(models.Model):
    uuid = models.UUIDField(primary_key=True)
    period = models.ForeignKey(
        DbPeriod, on_delete=models.CASCADE, related_name="incomplete_sheet_reports"
    )
    total = models.IntegerField()
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.period_id}:{self.created_at.isoformat()}"

    def to_entity(self) -> IncompleteSheetReport:
        return IncompleteSheetReport(
            uuid=self.uuid,
            period_uuid=self.period_id,
            total=self.total,
            payload=self.payload,
            created_at=self.created_at,
        )
