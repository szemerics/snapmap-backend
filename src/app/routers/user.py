from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.views.user import UserView
from app.utils.auth import auth

router = APIRouter()
security = HTTPBearer()


@router.get("/")
async def get_all_users():
    return await UserView.get_all_users()


@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = await auth.get_current_user(token)
    return user