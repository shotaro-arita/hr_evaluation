from django.contrib import admin

from evaluations.models.evaluation_item import DbEvaluationItem


@admin.register(DbEvaluationItem)
class DbEvaluationItemAdmin(admin.ModelAdmin[DbEvaluationItem]):
    list_filter = ["category"]
    list_display = ["__str__", "category"]
