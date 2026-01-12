from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.views.user import UserView
from app.utils.auth import auth
from app.models.user import UserRole

router = APIRouter()
security = HTTPBearer()


@router.get("/", tags=["User"])
async def get_all_users():
    return await UserView.get_all_users()


@router.get("/me", tags=["User"])
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = await auth.get_current_user(token)
    return user


@router.put("/set-role", tags=["Admin"])
async def set_user_role(target_user_id: str, role: UserRole , credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)

    try:
        modified_user = await UserView.set_role(target_user_id, role, acting_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if not modified_user:
        raise HTTPException(status_code=400, detail='No user found')

    return modified_user