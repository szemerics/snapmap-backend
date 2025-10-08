from fastapi import APIRouter
from app.models.map import Photo
from app.views.map import PhotoViews

router = APIRouter()

@router.get("/")
async def get_all_photos():
    return await PhotoViews.get_all_photos() 

@router.post("/")
async def create_photo(photo: Photo):
  return await PhotoViews.create_photo(photo)