from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.roles_crud import get_role_by_name_db
from app.crud.users_crud import get_user_by_email_db, create_user_db, get_user_by_id_db
from app.schemas.user_schemas import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse
from app.db.database import get_db
from app.utils.auth_utils import verify_password, create_access_token, create_refresh_token, verify_token
from app.config import config
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model= UserCreateResponse)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    email = data.email
    existing_user = await get_user_by_email_db(db, email)
    if existing_user:
        raise HTTPException(status_code=403, detail="User already exists")

    if data.admin_key == config.ADMIN_KEY:
        role = await get_role_by_name_db(db, "ADMIN")
    else:
        role = await get_role_by_name_db(db, "USER")

    if not role:
        raise HTTPException(status_code=500, detail="Role not found")

    user = await create_user_db(db, data.email, data.password, role.id)
    return {"message": "User registered successfully", "user_id": user.id}


@router.post("/login", response_model= UserLoginResponse)
async def login_user(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email_db(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=403, detail="Wrong password")

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh")
async def refresh_token(payload: dict = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id_db(db, payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(user)
    return {"access_token": new_access_token}