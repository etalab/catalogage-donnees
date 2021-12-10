from fastapi import APIRouter

from .apps import datasets

router = APIRouter()


@router.get("/")
def index() -> dict:
    return {"message": "Hello, world!"}


router.include_router(datasets.router)
