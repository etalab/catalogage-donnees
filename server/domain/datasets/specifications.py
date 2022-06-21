from dataclasses import dataclass
from typing import Optional, Sequence

from server.domain.common.types import ID

from .entities import GeographicalCoverage


@dataclass(frozen=True)
class DatasetSpec:
    search_term: Optional[str] = None
    geographical_coverage__in: Optional[Sequence[GeographicalCoverage]] = None
    tag__id__in: Optional[Sequence[ID]] = None
