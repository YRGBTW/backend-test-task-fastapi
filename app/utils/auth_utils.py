from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.db.models import User
from app.config import config

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
REFRESH_TOKEN_EXPIRE_DAYS = config.REFRESH_TOKEN_EXPIRE_DAYS

# Hashing password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verifying password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Creating JWT Token
def create_access_token(user: User, expires_delta: timedelta = timedelta(minutes=15)):
    expire = datetime.now() + expires_delta
    data = {"user_id": user.id, "role": user.role.name, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Verifying JWT Token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Refreshing token
def create_refresh_token(user_id: int):
    expire = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data = {"user_id": user_id, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Checking role
def verify_admin(payload: dict = Depends(verify_token)):
    role = payload.get("role")
    if role != "ADMIN":
        raise HTTPException(status_code=403, detail="Forbidden - admin role required")
    return payload