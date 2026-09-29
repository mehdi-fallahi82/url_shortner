from datetime import timedelta ,datetime,timezone
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def crate_access_token(data:dict) -> str:
    Token_data = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    Token_data.update({"exp": expires})

    return jwt.encode(
        Token_data,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )