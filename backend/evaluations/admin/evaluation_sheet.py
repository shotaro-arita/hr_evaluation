from django.contrib import admin

from evaluations.models.evaluation_sheet import (
    DbEvaluationSheet,
    DbEvaluationSheetScore,
)


class DbEvaluationSheetScoreInline(
    admin.TabularInline[DbEvaluationSheetScore, DbEvaluationSheet]
):
    model = DbEvaluationSheetScore


@admin.register(DbEvaluationSheet)
class DbEvaluationSheetAdmin(admin.ModelAdmin[DbEvaluationSheet]):
    inlines = [DbEvaluationSheetScoreInline]
    list_filter = ["status"]
    list_display = ["__str__", "employee_uuid", "period_uuid", "status"]
