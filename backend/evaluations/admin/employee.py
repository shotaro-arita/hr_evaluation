from django.contrib import admin

from evaluations.models.employee import DbEmployee


@admin.register(DbEmployee)
class DbEmployeeAdmin(admin.ModelAdmin[DbEmployee]):
    list_filter = ["position", "job_type"]
    list_display = ["__str__", "employee_code", "name"]
