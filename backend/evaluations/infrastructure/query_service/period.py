from datetime import datetime

from evaluations.domain.user.entity import User
from evaluations.models.period import DbPeriod
from evaluations.usecase.period.query_service import (
    PeriodListModel,
    PeriodModel,
    PeriodQueryService,
)


class PeriodQueryServiceImpl(PeriodQueryService):
    def get_list(self, user: User, now: datetime) -> PeriodListModel:
        periods = DbPeriod.objects.all()
        period_models: list[PeriodModel] = []
        current_period_uuid = None
        for period in periods:
            is_current = period.start_date <= now <= period.end_date
            if is_current and current_period_uuid is None:
                current_period_uuid = period.uuid
            period_models.append(
                PeriodModel(
                    uuid=period.uuid,
                    name=period.name,
                    start_date=period.start_date,
                    end_date=period.end_date,
                    is_current=is_current,
                )
            )
        return PeriodListModel(
            periods=period_models, current_period_uuid=current_period_uuid
        )
