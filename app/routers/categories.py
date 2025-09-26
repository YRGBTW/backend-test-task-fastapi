from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import  AsyncSession

from app.db.database import get_db
from app.crud.categories_crud import get_categories_db
from app.crud.posts_crud import get_posts_by_category_db

router = APIRouter(tags=["categories"])

@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    categories = await get_categories_db(db)

    result = []
    for category in categories:
        result.append({
            "id": category.id,
            "title": category.title,
            "slug": category.slug,
        })

    return result

@router.get("/categories/{slug}/posts")
async def get_category_posts(slug: str, db: AsyncSession = Depends(get_db)):
    posts = await get_posts_by_category_db(db, slug)

    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "author": post.author.email,
            "category": post.category.title
        })

    return result
