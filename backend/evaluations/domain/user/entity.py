from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class User:
    uuid: UUID
    employee_uuid: UUID
    employee_code: str
    password: str
    is_active: bool
    name: str
