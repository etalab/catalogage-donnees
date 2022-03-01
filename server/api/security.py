from fastapi.security import HTTPBearer

bearer_security = HTTPBearer(auto_error=False)
