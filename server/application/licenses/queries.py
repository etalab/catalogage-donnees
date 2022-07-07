from typing import List

from server.seedwork.application.queries import Query


class GetLicenseSet(Query[List[str]]):
    pass
