from .auth.backends.api_gouv import ApiGouvAuthBackend
from .auth.backends.multi import MultiAuthBackend
from .auth.backends.token import TokenAuthBackend

auth_backend = MultiAuthBackend([TokenAuthBackend(), ApiGouvAuthBackend()])
