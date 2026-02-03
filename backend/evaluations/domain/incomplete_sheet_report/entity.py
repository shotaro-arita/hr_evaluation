from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class IncompleteSheetReport:
    uuid: UUID
    period_uuid: UUID
    total: int
    payload: list[dict[str, Any]]
    created_at: datetime | None
