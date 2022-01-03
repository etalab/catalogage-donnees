from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.db import get_db

from . import queries, schemas
from .authentication import authenticate
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

    return await queries.create_user(
        db,
        email=data.email,
        password=data.password,
        full_name=data.full_name,
    )


@router.post(
    "/tokens/",
    response_model=schemas.TokenCreateResponse,
    status_code=201,
    responses={
        400: {
            "content": {
                "application/json": {"example": {"detail": "string"}},
            },
        }
    },
)
async def create_token(
    data: schemas.TokenCreate,
    db: AsyncSession = Depends(get_db),
) -> schemas.TokenCreateResponse:
    """
    Return a Bearer token for use in authenticated API requests,
    creating a new one for the authenticated user if necessary.
    """
    user = await authenticate(db, data.email, data.password)

    if user is None:
        raise HTTPException(400, detail="Invalid credentials")

    token, _ = await queries.get_or_create_token(db, user)

    return schemas.TokenCreateResponse(token=token.key)


@router.get("/check/")
async def check_auth(
    _: User = Depends(get_current_user),
) -> schemas.CheckAuthResponse:
    """
    Verify the request is authenticated.
    """
    return schemas.CheckAuthResponse()
