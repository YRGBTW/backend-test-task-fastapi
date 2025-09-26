from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify

from app.crud.categories_crud import create_category_db, update_category_db, delete_category_db
from app.schemas.category_schemas import CategoryBase, CategoryCreate
from app.schemas.post_schemas import PostCreate, PostUpdate
from app.crud.users_crud import get_users_db, update_user_role_db
from app.crud.posts_crud import create_post_db, update_post_db, delete_post_db
from app.db.database import get_db
from app.schemas.user_schemas import UserUpdateRequest
from app.utils.auth_utils import verify_admin

router = APIRouter(prefix="/admin", tags=["admin"])

# Admin router

# Manage users
@router.get("/users")
async def get_users(payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    users = await get_users_db(db)
    return users

@router.patch("/update_user_role/{user_id}")
async def update_user_role(data: UserUpdateRequest, payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    user = await update_user_role_db(db, data.user_id, data.new_role)
    return user


# Posts CRUD
@router.post("/post")
async def create_post(post: PostCreate, payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    slug = slugify(post.title)
    user_id = payload.get("user_id")
    post = await create_post_db(db, post.title, post.content, slug, user_id, post.category_id)
    return post

@router.patch("/update_post/{slug}")
async def update_post(slug: str, data: PostUpdate, payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    post = await update_post_db(db, slug, data)
    return post

@router.delete("/delete_post/{slug}")
async def delete_post(slug: str, payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    await delete_post_db(db, slug)
    return


# Categories CRUD
@router.post("/create_category")
async def create_category(data: CategoryCreate, payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    slug = slugify(data.title)
    category = await create_category_db(db, data.title, slug)
    return category

@router.patch("/update_category/{slug}")
async def update_category(slug: str, title:str, payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    category = await update_category_db(db, slug, title)
    return category

@router.delete("/delete_category/{slug}")
async def delete_category(slug: str, payload: dict = Depends(verify_admin), db: AsyncSession = Depends(get_db)):
    await delete_category_db(db, slug)
    return


