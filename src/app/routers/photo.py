from fastapi import APIRouter, UploadFile, File, Form
from app.models.photo import CreatePhoto
from app.views.photo import PhotoViews

router = APIRouter()

@router.get("/")
async def get_all_photos():
    return await PhotoViews.get_all_photos() 


@router.post("/")
async def create_photo(photo_data: str = Form(...), uploaded_file: UploadFile = File(...)):
  photo = CreatePhoto.model_validate_json(photo_data)

  return await PhotoViews.create_photo(photo, uploaded_file)