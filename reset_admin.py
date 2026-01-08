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

async def reset_admin():
    DATABASE_URL = "sqlite+aiosqlite:///Backend/traffic_data.db"
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == "admin"))
        user = result.scalar_one_or_none()
        
        if not user:
            print("User 'admin' does not exist. Creating...")
            user = User(
                username="admin",
                email="admin@example.com",
                password=hash_password("admin123"),
                full_name="System Administrator",
                role_id=0,
                is_active=1
            )
            session.add(user)
        else:
            user.password = hash_password("admin123")
            user.is_active = 1
            user.role_id = 0 # Ensure it's admin
            print("User 'admin' password reset to 'admin123'")
            
        await session.commit()

if __name__ == "__main__":
    asyncio.run(reset_admin())
