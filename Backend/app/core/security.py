from passlib.context import CryptContext

# Using rounds=10 for faster performance (default is 12)
# rounds=10 gives 2^10=1024 iterations (still secure, but 4x faster than default)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
