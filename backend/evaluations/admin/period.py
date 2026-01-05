from django.contrib import admin

from evaluations.models.period import DbPeriod


@admin.register(DbPeriod)
class DbPeriodAdmin(admin.ModelAdmin):
    list_display = ["__str__", "start_date", "end_date"]
