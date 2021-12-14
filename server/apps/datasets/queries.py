from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas


async def get_dataset(db: AsyncSession, id: int) -> Optional[models.Dataset]:
    stmt = select(models.Dataset).where(models.Dataset.id == id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def list_datasets(db: AsyncSession, *, limit: int = 10) -> List[models.Dataset]:
    stmt = select(models.Dataset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_dataset(
    db: AsyncSession, data: schemas.DatasetCreate
) -> models.Dataset:
    dataset = models.Dataset(name=data.name)
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)
    return dataset
