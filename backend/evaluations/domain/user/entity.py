from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class User:
    uuid: UUID
    # admin専用ユーザは従業員に紐づかないためnullを許容
    employee_uuid: UUID | None
    employee_code: str
    password: str
    is_active: bool
    name: str
