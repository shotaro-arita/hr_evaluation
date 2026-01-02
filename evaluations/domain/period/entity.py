from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Period:
    uuid: UUID
    name: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
