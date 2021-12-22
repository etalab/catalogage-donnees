from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from .apps import datasets

router = APIRouter()


@router.get("/")
def index():
    return RedirectResponse("/docs")


router.include_router(datasets.router)
