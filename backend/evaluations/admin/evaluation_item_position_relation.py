from django.contrib import admin

from evaluations.models.evaluation_item_position_relation import (
    DbEvaluationItemPositionRelation,
)


@admin.register(DbEvaluationItemPositionRelation)
class DbEvaluationItemPositionRelationAdmin(admin.ModelAdmin):
    list_filter = ["position"]
    list_display = ["__str__", "position", "order"]
