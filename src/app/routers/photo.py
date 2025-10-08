from fastapi import APIRouter
from app.models.photo import CreatePhoto
from app.views.photo import PhotoViews

router = APIRouter()

@router.get("/")
async def get_all_photos():
    return await PhotoViews.get_all_photos() 


@router.post("/")
async def create_photo(photo: CreatePhoto):
  return await PhotoViews.create_photo(photo)