from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.roles_crud import get_role_by_name_db
from app.utils.auth_utils import hash_password
from app.db.models import User

async def create_user_db(session: AsyncSession, email:str, password:str, role_id: int):
    user = User(email=email, password=hash_password(password=password), role_id = role_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

async def get_users_db(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()

async def get_user_by_email_db(session: AsyncSession, email: str) -> User:
    result = await session.execute(
        select(User)
        .options(selectinload(User.role))
        .filter(User.email == email)
    )
    return result.scalar_one_or_none()

async def get_user_by_id_db(session: AsyncSession, id: int) -> User:
    result = await session.execute(
        select(User)
        .options(selectinload(User.role))
        .filter(User.id == id)
    )
    return result.scalar_one_or_none()

async def update_user_role_db(session: AsyncSession, id: int, role:str) -> User:
    user = await get_user_by_id_db(session, id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = await get_role_by_name_db(session, role)

    if not user:
        raise HTTPException(status_code=404, detail="Role not found")

    user.role = role

    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_register_code_db(session: AsyncSession, code: str):
    result = await session.execute(select(User).filter(User.register_code == code))
    return result.scalar_one_or_none()
