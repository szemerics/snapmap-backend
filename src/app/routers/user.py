from fastapi import APIRouter
from app.views.user import UserView
from app.models.user import User

router = APIRouter()

@router.get("/")
async def get_all_users():
    return await UserView.get_all_users()

@router.post("/")
async def create_user(new_user: User):
    return await UserView.create_user(new_user)