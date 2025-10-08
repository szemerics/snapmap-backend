from app.database import engine
from app.models.photo import Photo, CreatePhoto

class PhotoViews:

  async def get_all_photos():
    photos = await engine.find(Photo)

    return photos
  
  
  async def create_photo(new_photo: CreatePhoto):
    new_photo = Photo(**new_photo.model_dump())
    saved_photo = await engine.save(new_photo)

    return saved_photo
