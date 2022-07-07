from server.application.licenses.handlers import get_license_set
from server.application.licenses.queries import GetLicenseSet
from server.seedwork.application.modules import Module


class LicensesModule(Module):
    query_handlers = {
        GetLicenseSet: get_license_set,
    }
