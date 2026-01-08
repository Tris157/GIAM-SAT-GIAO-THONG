import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import sys
import os

# Add Backend to path
sys.path.append(os.path.join(os.getcwd(), 'Backend'))

from app.models.user import User
from app.utils.password import hash_password

async def create_admin():
    DATABASE_URL = "sqlite+aiosqlite:///Backend/traffic_data.db"
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        # Check if admin exists
        result = await session.execute(select(User).where(User.username == "admin"))
        if result.scalar_one_or_none():
            print("User 'admin' already exists.")
            return

        new_user = User(
            username="admin",
            email="admin@example.com",
            password=hash_password("admin123"),
            full_name="System Administrator",
            role_id=0,  # Admin role
            is_active=1
        )
        db_user = db_user = new_user
        session.add(db_user)
        await session.commit()
        print("Admin user created: admin / admin123")

if __name__ == "__main__":
    asyncio.run(create_admin())
