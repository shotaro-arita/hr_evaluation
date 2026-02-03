from celery import shared_task


@shared_task
def generate_incomplete_sheet_report() -> str | None:
    from evaluations.usecase.incomplete_sheet_report.usecase import (
        IncompleteSheetReportUsecase,
    )

    return IncompleteSheetReportUsecase().generate_current_period_report()
