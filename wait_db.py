import os
import asyncio
import asyncpg

from app.config import config

DATABASE_URL = config.DATABASE_URL

async def wait_for_db():
    while True:
        try:
            conn = await asyncpg.connect(
                host="db",
                port=5432,
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "ADMIN"),
                database=os.getenv("POSTGRES_DB", "blog")
            )
            await conn.close()
            print("Database is ready")
            break
        except Exception:
            print("Waiting for database...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(wait_for_db())