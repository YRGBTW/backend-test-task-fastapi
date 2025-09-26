import asyncio
from sqlalchemy import select
from app.db.models import Role
from app.db.database import async_session

async def init_roles():
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Role))
            roles = result.scalars().all()
            if not roles:
                session.add_all([Role(name="ADMIN"), Role(name="USER")])
                await session.commit()

if __name__ == "__main__":
    asyncio.run(init_roles())