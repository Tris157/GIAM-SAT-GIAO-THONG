"""Script to check and create test user"""
import asyncio
from app.db.base import get_db_session_factory
from app.models.user import User
from app.utils.password import hash_password

async def check_and_create_user():
    """Check existing users and create test user if needed"""
    db_factory = get_db_session_factory()

    async with db_factory() as db:
        # Query all users
        from sqlalchemy import select
        result = await db.execute(select(User))
        users = result.scalars().all()

        print(f"[*] So user hien co: {len(users)}")
        for u in users:
            print(f"  - {u.username} ({u.email}) - Active: {u.is_active}")

        # Check if admin user exists
        admin_result = await db.execute(select(User).where(User.username == "admin"))
        admin_user = admin_result.scalar_one_or_none()

        if not admin_user:
            print("\n[+] Tao user admin mac dinh...")
            admin_user = User(
                username="admin",
                email="admin@smarttraffic.vn",
                password=hash_password("admin123"),
                full_name="Administrator",
                role_id=1,
                is_active=True
            )
            db.add(admin_user)
            await db.commit()
            print("[OK] Da tao user: admin / admin123")
        else:
            print(f"\n[OK] User admin da ton tai: {admin_user.username}")

        # Check test user
        test_result = await db.execute(select(User).where(User.username == "tridev"))
        test_user = test_result.scalar_one_or_none()

        if not test_user:
            print("\n[+] Tao user test...")
            test_user = User(
                username="tridev",
                email="tridev@test.com",
                password=hash_password("123456"),
                full_name="Tri Dev Test",
                role_id=2,
                is_active=True
            )
            db.add(test_user)
            await db.commit()
            print("[OK] Da tao user: tridev / 123456")
        else:
            print(f"\n[OK] User tridev da ton tai: {test_user.username}")

if __name__ == "__main__":
    asyncio.run(check_and_create_user())
