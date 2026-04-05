from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from app.models.photo import CreatePhoto, UpdatePhoto, Photo, CreateComment
from app.models.user import User
from app.utils.auth import auth
from app.views.photo import PhotoView
from odmantic import ObjectId
from typing import Optional
from enum import Enum

class PhotoTypeFilter(str, Enum):
    post = "post"
    map = "map"

router = APIRouter()

@router.get("/", tags=["Photos"])
async def get_photos(
    photo_type: Optional[PhotoTypeFilter] = None, 
    username: Optional[str] = None, 
    photo_id: Optional[ObjectId] = None, 
    camera_brand: Optional[str] = None, 
    camera_model: Optional[str] = None, 
    camera_type: Optional[str] = None, 
    lens: Optional[str] = None, 
    iso: Optional[int] = None, 
    shutter_speed: Optional[str] = None, 
    aperture: Optional[str] = None, 
    date_captured_from: Optional[datetime] = None, 
    date_captured_to: Optional[datetime] = None):
    return await PhotoView.get_photos(
        photo_type=photo_type.value if photo_type else None,
        username=username,
        photo_id=photo_id,
        date_captured_from=date_captured_from,
        date_captured_to=date_captured_to,
        camera_brand=camera_brand,
        camera_model=camera_model,
        camera_type=camera_type,
        lens=lens,
        iso=iso,
        shutter_speed=shutter_speed,
        aperture=aperture,
    ) 


@router.get("/following", tags=["Photos"])
async def get_following_photos(acting_user: User = Depends(auth.get_current_user)):
    return await PhotoView.get_following_photos(acting_user)


@router.get("/following", tags=["Photos"])
async def get_following_photos(acting_user: User = Depends(auth.get_current_user)):
    return await PhotoView.get_following_photos(acting_user)


@router.get("/following", tags=["Photos"])
async def get_following_photos(acting_user: User = Depends(auth.get_current_user)):
    return await PhotoView.get_following_photos(acting_user)


@router.post("/", response_model=Photo, tags=["Photos"])
async def create_photo(
    photo_data: str = Form(...),
    uploaded_file: UploadFile = File(...),
    acting_user: User = Depends(auth.get_current_user),
):
    photo = CreatePhoto.model_validate_json(photo_data)

    try:
        return await PhotoView.create_photo(photo, uploaded_file, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{photo_id}", response_model=Photo, tags=["Photos"])
async def update_photo(
    photo_id: ObjectId,
    photo_data: UpdatePhoto,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.update_photo(photo_id, photo_data, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return result


@router.delete("/{photo_id}", tags=["Photos"])
async def delete_photo(
    photo_id: ObjectId,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.delete_photo(photo_id, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return result


@router.post("/like/{photo_id}", tags=["Photos"])
async def like_photo(
    photo_id: ObjectId,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.like_photo(photo_id, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@router.delete("/like/{photo_id}", tags=["Photos"])
async def unlike_photo(
    photo_id: ObjectId,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.unlike_photo(photo_id, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@router.post("/comment/{photo_id}", response_model=Photo, tags=["Comments"])
async def add_comment(
    photo_id: ObjectId,
    comment_data: CreateComment,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.add_comment(photo_id, comment_data, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@router.post("/comment/{photo_id}/reply/{comment_id}", response_model=Photo, tags=["Comments"])
async def reply_to_comment(
    photo_id: ObjectId,
    comment_id: ObjectId,
    comment_data: CreateComment,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.reply_to_comment(photo_id, comment_id, comment_data, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


# @router.delete("/", tags=["Admin"])
# async def delete_all_photos():
#     return await PhotoView.delete_all_photos()