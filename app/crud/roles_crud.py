from sqlalchemy.future import select
from app.db.models import Role
from sqlalchemy.ext.asyncio import AsyncSession

# Get role by name
async def get_role_by_name_db(session: AsyncSession, role_name: str) -> Role:
    result = await session.execute(select(Role).filter(Role.name == role_name))
    return result.scalars().first()
