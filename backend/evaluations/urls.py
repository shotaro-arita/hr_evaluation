from rest_framework.routers import DefaultRouter

from evaluations.adapter.evaluation_sheet.view import EvaluationSheetViewSet


router = DefaultRouter()
router.register(
    "evaluation_sheets", EvaluationSheetViewSet, basename="evaluation_sheets"
)

urlpatterns = router.urls
