from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.photo import CreatePhoto, UpdatePhoto, Photo
from app.utils.auth import auth
from app.views.photo import PhotoView
from odmantic import ObjectId
from typing import Optional

router = APIRouter()
security = HTTPBearer()

@router.get("/")
async def get_all_photos():
    return await PhotoView.get_all_photos() 


@router.get("/{photo_id}", response_model=Photo)
async def get_photo_by_id(photo_id: str):
    try:
        object_id = ObjectId(photo_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid photo ID format")

    photo = await PhotoView.get_photo_by_id(object_id)

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return photo


@router.post("/", response_model=Photo)
async def create_photo(photo_data: str = Form(...), uploaded_file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Depends(security)):
  token = credentials.credentials
  acting_user = await auth.get_current_user(token)

  photo = CreatePhoto.model_validate_json(photo_data)

  return await PhotoView.create_photo(photo, uploaded_file, acting_user)


@router.put("/{photo_id}", response_model=Photo)
async def update_photo(photo_id: str, photo_data: str = Form(...), credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)

    try:
        object_id = ObjectId(photo_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid photo ID format")
    
    update_data = UpdatePhoto.model_validate_json(photo_data)
    result = await PhotoView.update_photo(object_id, update_data, acting_user)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.delete("/{photo_id}")
async def delete_photo(photo_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)

    try:
        object_id = ObjectId(photo_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid photo ID format")
    
    try:
        result = await PhotoView.delete_photo(object_id, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    return result


@router.delete("/")
async def delete_all_photos():
    return await PhotoView.delete_all_photos()