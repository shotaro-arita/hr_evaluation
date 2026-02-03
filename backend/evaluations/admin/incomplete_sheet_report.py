from django.contrib import admin

from evaluations.models.incomplete_sheet_report import DbIncompleteSheetReport


@admin.register(DbIncompleteSheetReport)
class IncompleteSheetReportAdmin(admin.ModelAdmin):
    list_display = ["__str__", "period", "total", "created_at"]
    list_filter = ["period"]
    search_fields = ["period__name"]
