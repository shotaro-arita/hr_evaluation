from django.contrib import admin

from evaluations.models.evaluation_assignment import DbEvaluationAssignment


@admin.register(DbEvaluationAssignment)
class DbEvaluationAssignmentAdmin(admin.ModelAdmin):
    list_filter = ["role"]
    list_display = ["__str__", "target_employee_uuid", "manager_employee_uuid", "role"]
