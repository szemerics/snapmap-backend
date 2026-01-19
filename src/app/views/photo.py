from datetime import datetime
from app.config import engine
from app.models.photo import Photo, CreatePhoto, UpdatePhoto
from app.models.user import User, UserSummary, UserRole
from app.utils.images import CloudinaryService
from fastapi import File
from odmantic import ObjectId
from PIL import Image
import io
from app.utils.nsfw_model import nsfw_pipeline
from app.models.user import PhotoSummary


class PhotoView:
  async def delete_all_photos():
    """
    Delete all photos from the database. For testing purposes only.
    """
    photos = await engine.find(Photo)

    for photo in photos:
      CloudinaryService.delete_image(photo.cloudinary_public_id)
      await engine.delete(photo)

    return {"message": "All photos deleted successfully"}


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
  

  async def get_photos_by_user(username: str):
    """
    Retrieve all photos posted by a specific user.
    """
    photos = await engine.find(Photo, Photo.user_summary.username == username)

    return photos
  

  async def create_photo(new_photo: CreatePhoto, uploaded_file: File, acting_user: User):
    """
    Create a new photo entry in the database with image upload to Cloudinary.
    NSFW check is performed using the Falconsai/nsfw_image_detection model from huggingface.
    """
    file_content = await uploaded_file.read()

    # Convert raw bytes to a PIL image for classification
    try:
        image = Image.open(io.BytesIO(file_content))
    except Exception as e:
        print(f"Error loading image: {e}")
        raise ValueError("Uploaded file is not a valid image")

    classifications = nsfw_pipeline(image)

    if (classifications[0]["label"].lower() == "nsfw") and (classifications[0]["score"] > 0.7):
      raise ValueError("Uploaded image is classified as NSFW")

    upload_result = CloudinaryService.upload_image(file_content, 'snapmap')

    # upload_result = {
    #   "secure_url": "https://res.cloudinary.com/demo/image/upload/v1697040000/sample.jpg",
    #   "public_id": "sample_public_id"
    # }

    user_summary = UserSummary(
      user_id=acting_user.id,
      username=acting_user.username,
      profile_picture_url=acting_user.profile_picture_url,
      bio=acting_user.bio
    )

    photo = Photo(
        user_summary=user_summary,
        photo_url=str(upload_result["secure_url"]),
        cloudinary_public_id=str(upload_result["public_id"]),
        location=new_photo.location,
        date_captured=new_photo.date_captured,
        category=new_photo.category,
        gear=new_photo.gear,
        settings_used=new_photo.settings_used,
        date_posted=datetime.now(),
        caption=new_photo.caption,
    )

    saved_photo = await engine.save(photo)
    acting_user.photo_summaries.append(PhotoSummary(photo_id=saved_photo.id, photo_url=saved_photo.photo_url))
    await engine.save(acting_user)

    return saved_photo


  async def update_photo(photo_id: ObjectId, update_data: UpdatePhoto, acting_user: User):
    """
    Update photo metadata in the database.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)
    
    if not photo:
      raise ValueError(f'Photo with id {photo_id} not found')
    
    if photo.user_summary.user_id != acting_user.id:
      if (acting_user.role == UserRole.USER):
        raise PermissionError('You have no right to delete this photo')
    
    # Update only the metadata fields that were provided
    if update_data.location is not None:
      photo.location = update_data.location
    if update_data.category is not None:
      photo.category = update_data.category
    if update_data.gear is not None:
      photo.gear = update_data.gear
    if update_data.settings_used is not None:
      photo.settings_used = update_data.settings_used
    if update_data.caption is not None:
      photo.caption = update_data.caption
    if update_data.date_captured is not None:
      photo.date_captured = update_data.date_captured
    
    # Save the updated photo
    updated_photo = await engine.save(photo)
    
    return updated_photo


  async def delete_photo(photo_id: ObjectId, acting_user: User): 
    """
    Delete a photo from the database and remove the image from Cloudinary.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)

    if not photo:
      raise ValueError(f'Photo with id {photo_id} not found')

    if photo.user_summary.user_id != acting_user.id:
      if (acting_user.role == UserRole.USER):
        raise PermissionError('You have no permission to delete this photo')
    
    CloudinaryService.delete_image(photo.cloudinary_public_id)
    
    acting_user.photo_summaries = [p for p in acting_user.photo_summaries if p.photo_id != photo_id]
    await engine.save(acting_user)
    
    await engine.delete(photo)
    
    return {"message": "Photo deleted successfully"}