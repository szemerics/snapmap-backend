from app.config import engine
from app.models.photo import Photo, CreatePhoto, UpdatePhoto
from app.utils.images import CloudinaryService
from fastapi import File
from odmantic import ObjectId
from typing import Optional

class PhotoViews:

  async def get_all_photos():
    """
    Get all photos from the database.
    """
    photos = await engine.find(Photo)

    return photos


  async def get_photo_by_id(photo_id: ObjectId):
    """
    Retrieve a photo by its ID from the database.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)

    return photo
  

  async def create_photo(new_photo: CreatePhoto, uploaded_file:  File):
    """
    Create a new photo entry in the database with image upload to Cloudinary.
    """
    file_content = await uploaded_file.read()
    upload_result = CloudinaryService.upload_image(file_content, 'snapmap')

    photo = Photo(
        user_id=new_photo.user_id,
        location=new_photo.location,
        date=new_photo.date,
        category=new_photo.category,
        gear=new_photo.gear,
        settings_used=new_photo.settings_used,
        photo_url=str(upload_result["secure_url"]),
        cloudinary_public_id=str(upload_result["public_id"])
    )

    saved_photo = await engine.save(photo)

    return saved_photo


  async def update_photo(photo_id: ObjectId, update_data: UpdatePhoto):
    """
    Update photo metadata in the database.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)
    
    if not photo:
      return {"error": "Photo not found"}
    
    # Update only the metadata fields that were provided
    if update_data.location is not None:
      photo.location = update_data.location
    if update_data.date is not None:
      photo.date = update_data.date
    if update_data.category is not None:
      photo.category = update_data.category
    if update_data.gear is not None:
      photo.gear = update_data.gear
    if update_data.settings_used is not None:
      photo.settings_used = update_data.settings_used
    
    # Save the updated photo
    updated_photo = await engine.save(photo)
    
    return updated_photo


  async def delete_photo(photo_id: ObjectId): 
    """
    Delete a photo from the database and remove the image from Cloudinary.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)
    
    CloudinaryService.delete_image(photo.cloudinary_public_id)
    
    await engine.delete(photo)
    
    return {"message": "Photo deleted successfully"}