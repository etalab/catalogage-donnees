from fastapi.security import APIKeyHeader

# XXX: Temporary password-less identification mechanism.
# Must be replaced with a regular user-password authentication mechanism later on
# (e.g. OAuth bearer, token auth, etc).
email_security = APIKeyHeader(name="X-Email")
