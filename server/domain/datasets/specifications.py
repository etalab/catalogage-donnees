from dataclasses import dataclass
from typing import Optional, Sequence

from .entities import GeographicalCoverage


@dataclass(frozen=True)
class DatasetSearch:
    term: str
    highlight: bool = False


@dataclass(frozen=True)
class DatasetSpec:
    search: Optional[DatasetSearch] = None
    geographical_coverage__in: Optional[Sequence[GeographicalCoverage]] = None
