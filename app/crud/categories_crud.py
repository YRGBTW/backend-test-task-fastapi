from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category


async def get_categories_db(session: AsyncSession):
    result = await session.execute(select(Category))
    return result.scalars().all()

async def get_category_by_id(session: AsyncSession, id: int):
    result = await session.execute(select(Category).filter(Category.id == id))
    return result.scalars().one_or_none()

async def get_category_by_slug_db(session: AsyncSession, slug:str):
    result = await session.execute(select(Category).filter(Category.slug == slug))
    return result.scalars().one_or_none()

async def update_category_db(session: AsyncSession, slug: str, title: str):
    result = await session.execute(select(Category).filter(Category.slug == slug))
    category = result.scalars().first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.title = title

    await session.commit()
    await session.refresh(category)
    return category

async def create_category_db(session: AsyncSession, title: str, slug:str):
    category = Category(title=title, slug=slug)

    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

async def delete_category_db(session: AsyncSession, slug:str):
    result = await session.execute(select(Category).filter(Category.slug == slug))
    category = result.scalars().first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await session.delete(category)
    await session.commit()
    return