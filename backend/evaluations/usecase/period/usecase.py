import inject
from django.utils import timezone

from evaluations.domain.user.entity import User
from evaluations.usecase.period.query_service import PeriodListModel, PeriodQueryService


class PeriodUsecase:
    @inject.autoparams()
    def __init__(self, period_query_service: PeriodQueryService):
        self.period_query_service = period_query_service

    def get_periods(self, request_user: User) -> PeriodListModel:
        return self.period_query_service.get_list(request_user, timezone.now())
