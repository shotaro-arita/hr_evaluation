from django.contrib import admin

from evaluations.models.evaluation_weight_policy import DbEvaluationWeightPolicy


@admin.register(DbEvaluationWeightPolicy)
class DbEvaluationWeightPolicyAdmin(admin.ModelAdmin):
    list_display = ["__str__", "period", "position", "category", "weight"]
    list_filter = ["period", "position", "category"]
