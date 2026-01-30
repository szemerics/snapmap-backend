from fastapi import APIRouter, HTTPException
from app.models.user import UserLogin, UserRegister
from app.utils.auth import auth

router = APIRouter()

@router.post("/login")
async def login_for_access_token(user_data: UserLogin):
    token = await auth.login_auth(user_data)
    if not token:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return token


@router.post("/register")
async def register(user_data: UserRegister):
    new_user = await auth.register_auth(user_data)

    if not new_user:
        raise HTTPException(status_code=400, detail='User already exists')
    
    return new_user
    