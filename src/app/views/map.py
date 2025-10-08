from app.database import engine
from app.models.map import Photo

class PhotoViews:

  async def get_all_photos():
    photos = await engine.find(Photo)

    return photos
  
  async def create_photo(new_photo: Photo):
    saved_photo = await engine.save(new_photo)

    return saved_photo
