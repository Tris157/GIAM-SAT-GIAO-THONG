"""
Password hashing utilities using bcrypt
"""
from passlib.context import CryptContext

# Create password context with bcrypt
# Using rounds=10 for faster performance (default is 12)
# rounds=10 gives 2^10=1024 iterations (still secure, but 4x faster than default)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10)


def _truncate_password(password: str) -> str:
    """
    Truncate password to 72 bytes (bcrypt limit)

    Args:
        password: Plain text password

    Returns:
        Truncated password (max 72 bytes)
    """
    # Encode to bytes and truncate to 72 bytes max
    password_bytes = password.encode('utf-8')[:72]
    # Decode back to string
    return password_bytes.decode('utf-8', errors='ignore')


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    # Truncate password to avoid bcrypt 72-byte limit error
    password = _truncate_password(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    try:
        # Truncate password to avoid bcrypt 72-byte limit error
        plain_password = _truncate_password(plain_password)
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False
