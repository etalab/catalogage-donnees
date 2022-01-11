from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.db import get_db

from . import queries, schemas
from .dependencies import get_current_user
from .models import User

router = APIRouter()


@router.post(
    "/users/",
    response_model=schemas.User,
    status_code=201,
    responses={
        400: {
            "content": {
                "application/json": {"example": {"detail": "string"}},
            },
        }
    },
)
async def create_user(
    data: schemas.UserCreate, db: AsyncSession = Depends(get_db)
) -> User:
    """
    Register a new user.
    """
    user = await queries.get_user_by_email(db, data.email)

    if user is not None:
        raise HTTPException(400, detail="Email already exists")

    return await queries.create_user(db, email=data.email)


@router.get("/check/")
async def check_auth(
    _: User = Depends(get_current_user),
) -> schemas.CheckAuthResponse:
    """
    Verify the request is authenticated.
    """
    return schemas.CheckAuthResponse()
