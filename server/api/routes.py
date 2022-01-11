from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from server.config import Settings
from server.config.di import resolve

from . import auth, datasets

router = APIRouter()


@router.get("/", response_class=RedirectResponse, include_in_schema=False)
def index(settings: Settings = Depends(lambda: resolve(Settings))) -> str:
    return settings.docs_url


router.include_router(auth.router)
router.include_router(datasets.router)
