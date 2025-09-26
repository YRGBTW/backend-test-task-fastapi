from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.categories_crud import get_category_by_id
from app.db.models import Post, Category
from app.schemas.post_schemas import PostUpdate


async def get_posts_db(session: AsyncSession):
    q = select(Post).options(
        selectinload(Post.author),
        selectinload(Post.category),
    )
    result = await session.execute(q)
    return result.scalars().all()

async def get_posts_by_category_db(session: AsyncSession, category_slug: str):
    result = await session.execute(
        select(Post)
        .join(Post.category)
        .options(selectinload(Post.author), selectinload(Post.category))
        .filter(Category.slug == category_slug)
    )
    return result.scalars().all()

async def get_post_by_id_db(session: AsyncSession, id: int):
    result = await session.execute(select(Post).options(selectinload(Post.author)).options(selectinload(Post.category)).filter(Post.id == id))
    return result.scalars().one_or_none()

async def get_post_by_slug_db(session: AsyncSession, slug:str):
    result = await session.execute(select(Post).options(selectinload(Post.author)).options(selectinload(Post.category)).filter(Post.slug == slug))

    return result.scalars().one_or_none()

async def update_post_db(session: AsyncSession, slug: str, data: PostUpdate):
    result = await session.execute(select(Post).filter(Post.slug == slug))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_title = data.title
    new_content = data.content
    new_category_id = data.category_id

    if new_title:
        post.title = new_title
    if new_content:
        post.content = new_content
    if new_category_id or new_category_id == 0:
        cat = await get_category_by_id(session, new_category_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")
        post.category_id = new_category_id

    await session.commit()
    await session.refresh(post)
    return post

async def create_post_db(session: AsyncSession, title: str, content: str, slug:str, user_id: int, category_id: int = None):
    if category_id or category_id == 0:
        cat = await get_category_by_id(session, category_id)
        if not cat:
            raise HTTPException(status_code=404, detail="Category not found")

    post = Post(title=title, slug=slug, content= content, user_id = user_id, category_id = category_id)

    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def delete_post_db(session: AsyncSession, slug:str):
    result = await session.execute(select(Post).filter(Post.slug == slug))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await session.delete(post)
    await session.commit()
    return