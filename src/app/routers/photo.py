from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.photo import CreatePhoto, UpdatePhoto, Photo
from app.views.photo import PhotoViews
from odmantic import ObjectId
from typing import Optional

router = APIRouter()

@router.get("/")
async def get_all_photos():
    return await PhotoViews.get_all_photos() 


@router.post("/", response_model=Photo)
async def create_photo(photo_data: str = Form(...), uploaded_file: UploadFile = File(...)):
  photo = CreatePhoto.model_validate_json(photo_data)

  return await PhotoViews.create_photo(photo, uploaded_file)


@router.put("/{photo_id}", response_model=Photo)
async def update_photo(photo_id: str, photo_data: str = Form(...)):
    try:
        object_id = ObjectId(photo_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid photo ID format")
    
    update_data = UpdatePhoto.model_validate_json(photo_data)
    result = await PhotoViews.update_photo(object_id, update_data)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.delete("/{photo_id}")
async def delete_photo(photo_id: str):
    try:
        object_id = ObjectId(photo_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid photo ID format")
    
    result = await PhotoViews.delete_photo(object_id)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result