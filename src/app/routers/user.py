from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from app.views.user import UserView
from app.utils.auth import auth
from app.models.user import User, UserRole, UserUpdate

router = APIRouter()


@router.get("/", tags=["User"])
async def get_users(username: Optional[str] = None, email: Optional[str] = None,):
    try:
        users = await UserView.get_users(username=username, email=email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return users


@router.get("/me", tags=["User"])
async def get_current_user(acting_user: User = Depends(auth.get_current_user)):
    return acting_user


@router.put("/set-role", tags=["Admin"])
async def set_user_role(target_user_id: str, role: UserRole , acting_user: User = Depends(auth.get_current_user)):
    try:
        modified_user = await UserView.set_role(target_user_id, role, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return modified_user


@router.put('/update-profile-picture', tags=["User"])
async def update_profile_picture(
    uploaded_file: UploadFile = File(...),
    acting_user: User = Depends(auth.get_current_user)
):
    try:
        modified_user = await UserView.update_profile_picture(uploaded_file, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return modified_user


@router.put("/update-profile-data", tags=["User"])
async def update_profile_data(
    update_data: UserUpdate,
    acting_user: User = Depends(auth.get_current_user)
):
    try:
        modified_user = await UserView.update_profile_data(update_data, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return modified_user