from django.contrib import admin

from evaluations.models.evaluation_sheet import (
    DbEvaluationSheet,
    DbEvaluationSheetScore,
)


class DbEvaluationSheetScoreInline(admin.TabularInline):
    model = DbEvaluationSheetScore


@admin.register(DbEvaluationSheet)
class DbEvaluationSheetAdmin(admin.ModelAdmin):
    inlines = [DbEvaluationSheetScoreInline]
    list_filter = ["own_status", "manager_status"]
    list_display = ["__str__", "employee", "period", "own_status", "manager_status"]
