from rest_framework.routers import DefaultRouter

from evaluations.adapter.evaluation_assignment.view import EvaluationAssignmentViewSet
from evaluations.adapter.evaluation_sheet.view import EvaluationSheetViewSet
from evaluations.adapter.period.view import PeriodViewSet
from evaluations.adapter.user.view import UserViewSet

router = DefaultRouter()
router.register(
    "evaluation_sheets", EvaluationSheetViewSet, basename="evaluation_sheets"
)
router.register("users", UserViewSet, basename="users")
router.register(
    "evaluation_assignments",
    EvaluationAssignmentViewSet,
    basename="evaluation_assignments",
)
router.register("periods", PeriodViewSet, basename="periods")

urlpatterns = router.urls
