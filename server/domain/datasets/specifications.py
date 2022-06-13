from dataclasses import dataclass
from typing import Optional, Sequence

from .entities import GeographicalCoverage


@dataclass(frozen=True)
class DatasetSpec:
    geographical_coverage__in: Optional[Sequence[GeographicalCoverage]] = None
