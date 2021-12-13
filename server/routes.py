from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def index() -> dict:
    return {"message": "Hello, world!"}
