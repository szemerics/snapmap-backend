from app.config import engine
from app.models.photo import Photo, CreatePhoto
from app.utils.images import CloudinaryService
from fastapi import UploadFile, File

class PhotoViews:

  async def get_all_photos():
    photos = await engine.find(Photo)

    return photos
  
  
  async def create_photo(new_photo: CreatePhoto, uploaded_file:  File):
    file_content = await uploaded_file.read()
    upload_result = CloudinaryService.upload_image(file_content, 'snapmap')

    print (upload_result["secure_url"])

    photo = Photo(
        user_id=new_photo.user_id,
        location=new_photo.location,
        date=new_photo.date,
        category=new_photo.category,
        gear=new_photo.gear,
        settings_used=new_photo.settings_used,
        photo_url='xddd',
    )

    saved_photo = await engine.save(photo)

    return saved_photo
