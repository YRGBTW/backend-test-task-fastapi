from typing import Optional
from pydantic import BaseModel, EmailStr

# User Schema
class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    email: EmailStr
    password: str
    admin_key: Optional[str] = None

class UserCreateResponse(UserBase):
    message: str
    user_id: int

class UserLogin(UserBase):
    email: EmailStr
    password: str

class UserLoginResponse(UserBase):
    access_token: str
    refresh_token: str

class UserInfoResponse(UserBase):
    id: int
    role: str
    email: EmailStr

class UserUpdateRequest(UserBase):
    user_id: int
    new_role: str
