from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .apps import auth, datasets
from .conf import settings

router = APIRouter()


@router.get("/", response_class=RedirectResponse, include_in_schema=False)
def index() -> str:
    return settings.docs_url


router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(datasets.router)
