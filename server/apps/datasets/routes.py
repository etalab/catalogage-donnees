from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.db import get_db

from . import models, queries, schemas

router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
)


@router.post("/", response_model=schemas.Dataset, status_code=201)
async def create_dataset(
    data: schemas.DatasetCreate, db: AsyncSession = Depends(get_db)
) -> models.Dataset:
    return await queries.create_dataset(db, data)


@router.get("/", response_model=List[schemas.Dataset])
async def list_datasets(
    limit: int = 10, db: AsyncSession = Depends(get_db)
) -> List[models.Dataset]:
    return await queries.list_datasets(db, limit=limit)


@router.get(
    "/{id}/",
    response_model=schemas.Dataset,
    responses={404: {}},
)
async def get_dataset(id: int, db: AsyncSession = Depends(get_db)) -> models.Dataset:
    dataset = await queries.get_dataset(db, id)
    if dataset is None:
        raise HTTPException(404)
    return dataset
