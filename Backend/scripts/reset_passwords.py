"""Script to reset all user passwords"""
import asyncio
from app.db.base import get_db_session_factory
from app.models.user import User
from app.utils.password import hash_password
from sqlalchemy import select

async def reset_all_passwords():
    """Reset passwords for all users"""
    db_factory = get_db_session_factory()

    # Default passwords for each user
    password_map = {
        "admin": "admin123",
        "tridev": "123456",
        "testuser2": "test123"
    }

    async with db_factory() as db:
        # Get all users
        result = await db.execute(select(User))
        users = result.scalars().all()

        print(f"[*] Dang reset password cho {len(users)} users...")

        for user in users:
            # Get default password for this user
            new_password = password_map.get(user.username, "123456")

            # Hash new password
            user.password = hash_password(new_password)

            print(f"  [+] Reset password cho user: {user.username} -> {new_password}")

        # Commit all changes
        await db.commit()
        print("\n[OK] Da reset tat ca passwords!")
        print("\n=== LOGIN INFO ===")
        for username, password in password_map.items():
            print(f"  Username: {username}")
            print(f"  Password: {password}")
            print()

if __name__ == "__main__":
    asyncio.run(reset_all_passwords())
