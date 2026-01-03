from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar


@dataclass(frozen=True)
class PaginationQueryDto:
    page: int = 1
    page_size: int = 10

    def __post_init__(self) -> None:
        object.__setattr__(self, "page_size", min(self.page_size, 100))


T = TypeVar("T")


@dataclass(frozen=True)
class PaginatedResult(Generic[T]):
    count: int
    results: List[T]
    next: Optional[int] = None
    previous: Optional[int] = None
