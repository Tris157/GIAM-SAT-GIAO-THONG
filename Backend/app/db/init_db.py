"""
Initialize database with tables
Run this script to create all database tables
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.models.user import User
from app.models.traffic_record import TrafficRecord
from app.core.config import settings


async def init_db():
    """Create all database tables"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        # Drop all tables (optional, remove in production)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("✅ Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
