from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users_crud import get_user_by_id_db
from app.db.database import get_db
from app.schemas.user_schemas import UserInfoResponse
from app.utils.auth_utils import verify_token

router = APIRouter(tags=["users"])

@router.get("/me", response_model= UserInfoResponse)
async def get_current_user(payload: dict = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id_db(db, payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "role": user.role.name, "email":user.email}