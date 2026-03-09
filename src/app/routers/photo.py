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
async def get_photos(photo_type: Optional[PhotoTypeFilter] = None, username: Optional[str] = None, photo_id: Optional[ObjectId] = None):
    return await PhotoView.get_photos(photo_type.value if photo_type else None, username, photo_id) 


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


@router.post("/{photo_id}/like", tags=["Photos"])
async def like_photo(
    photo_id: ObjectId,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.like_photo(photo_id, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@router.delete("/{photo_id}/unlike", tags=["Photos"])
async def unlike_photo(
    photo_id: ObjectId,
    acting_user: User = Depends(auth.get_current_user),
):
    try:
        result = await PhotoView.unlike_photo(photo_id, acting_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return result


@router.post("/{photo_id}/comments", response_model=Photo, tags=["Comments"])
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


@router.post("/{photo_id}/comments/{comment_id}/reply", response_model=Photo, tags=["Comments"])
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