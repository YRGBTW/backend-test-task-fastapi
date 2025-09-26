from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.crud.posts_crud import get_posts_db, get_post_by_slug_db

router = APIRouter(tags=["posts"])

@router.get("/posts")
async def get_posts(db: AsyncSession = Depends(get_db)):
    posts = await get_posts_db(db)

    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "author": post.author.email,
            "category": post.category.title if post.category else None
        })

    return result

@router.get("/posts/{slug}")
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    post = await get_post_by_slug_db(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "content": post.content,
            "author": post.author.email,
            "category": post.category.title if post.category else None
        }