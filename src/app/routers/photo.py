from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.photo import CreatePhoto, UpdatePhoto, Photo
from app.utils.auth import auth
from app.views.photo import PhotoView
from odmantic import ObjectId
from typing import Optional

router = APIRouter()
security = HTTPBearer()

@router.get("/", tags=["Photos"])
async def get_all_photos():
    return await PhotoView.get_all_photos() 


@router.get("/user-photos", response_model=list[Photo], tags=["Photos"])
async def get_photos_by_user(user_id: Optional[ObjectId] = None, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    if user_id is None:
        token = credentials.credentials
        acting_user = await auth.get_current_user(token)
        user_id = acting_user.id

    photos = await PhotoView.get_photos_by_user(user_id)

    if not photos:
        raise HTTPException(status_code=404, detail="No photos found for this user")

    return photos


@router.get("/{photo_id}", response_model=Photo, tags=["Photos"])
async def get_photo_by_id(photo_id: ObjectId):
    photo = await PhotoView.get_photo_by_id(photo_id)

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return photo


@router.post("/", response_model=Photo, tags=["Photos"])
async def create_photo(photo_data: str = Form(...), uploaded_file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Depends(security)):
  token = credentials.credentials
  acting_user = await auth.get_current_user(token)

  photo = CreatePhoto.model_validate_json(photo_data)

  return await PhotoView.create_photo(photo, uploaded_file, acting_user)


@router.put("/{photo_id}", response_model=Photo, tags=["Photos"])
async def update_photo(photo_id: ObjectId, photo_data: UpdatePhoto, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)

    try:
        result = await PhotoView.update_photo(photo_id, photo_data, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    return result


@router.delete("/{photo_id}", tags=["Photos"])
async def delete_photo(photo_id: ObjectId, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)
    
    try:
        result = await PhotoView.delete_photo(photo_id, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    return result


@router.delete("/", tags=["Admin"])
async def delete_all_photos():
    return await PhotoView.delete_all_photos()