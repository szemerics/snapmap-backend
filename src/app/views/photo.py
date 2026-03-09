from datetime import datetime
from typing import Optional, List
from app.config import engine
from app.models.photo import Photo, CreatePhoto, UpdatePhoto, Comment, CreateComment
from app.models.user import User, UserSummary, UserRole, PhotoSummary
from app.utils.images import CloudinaryService
from fastapi import File
from odmantic import ObjectId


class PhotoView:
  # async def delete_all_photos():
  #   """
  #   Delete all photos from the database. For testing purposes only.
  #   """
  #   photos = await engine.find(Photo)

  #   for photo in photos:
  #     CloudinaryService.delete_image(photo.cloudinary_public_id)
  #     await engine.delete(photo)

  #   return {"message": "All photos deleted successfully"}


  @staticmethod
  def _build_user_summary(acting_user: User) -> UserSummary:
    return UserSummary(
      user_id=acting_user.id,
      username=acting_user.username,
      profile_picture=acting_user.profile_picture,
      bio=acting_user.bio
    )

  
  @staticmethod
  def _find_comment(comments: List[Comment], comment_id: ObjectId) -> Optional[Comment]:
    for comment in comments:
      if comment.comment_id == comment_id:
        return comment
      found = PhotoView._find_comment(comment.replies, comment_id)
      if found:
        return found
    return None


  async def get_photos(photo_type: str = None, username: str = None, photo_id: ObjectId = None):
    """
    Get photos from the database with optional filters.
    Args:
        photo_type: Filter by photo type - 'post' (no location), 'map' (with location), or None (all)
        username: Filter by user
        photo_id: Filter by specific photo ID
    """
    query = []
    
    if photo_type == 'post':
      query.append(Photo.location == None)
    elif photo_type == 'map':
      query.append(Photo.location != None)
    
    if username:
      query.append(Photo.user_summary.username == username)
    if photo_id:
      query.append(Photo.id == photo_id)
    
    if query:
      photos = await engine.find(Photo, *query, sort=Photo.date_posted.desc())
    else:
      photos = await engine.find(Photo, sort=Photo.date_posted.desc())

    return photos


  async def create_photo(new_photo: CreatePhoto, uploaded_file: File, acting_user: User, init_public_id: Optional[str] = None):
    """
    Create a new photo entry in the database with image upload to Cloudinary.
    NSFW check is performed using the Falconsai/nsfw_image_detection model from huggingface.
    # init_public_id sets a fixed public ID for test uploads
    """
    upload_result = await CloudinaryService.upload_image(uploaded_file, 'snapmap', public_id=init_public_id)

    user_summary = PhotoView._build_user_summary(acting_user)

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
    acting_user.photo_summaries.insert(0, PhotoSummary(photo_id=saved_photo.id, photo_url=saved_photo.photo_url))
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
        raise PermissionError('You have no permission to update this photo')
    
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
    
    target_user = acting_user

    if photo.user_summary.user_id != acting_user.id:
      if (acting_user.role == UserRole.USER):
        raise PermissionError('You have no permission to delete this photo')
      
      target_user = await engine.find_one(User, User.id == photo.user_summary.user_id)
    
    CloudinaryService.delete_image(photo.cloudinary_public_id)
    
    target_user.photo_summaries = [p for p in target_user.photo_summaries if p.photo_id != photo_id]
    await engine.save(target_user)
    
    await engine.delete(photo)
    
    return {"message": "Photo deleted successfully"}


  async def like_photo(photo_id: ObjectId, acting_user: User):
    """
    Like a photo.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)
    if not photo:
      raise ValueError(f'Photo with id {photo_id} not found')

    user_summary = PhotoView._build_user_summary(acting_user)
    
    photo.likes.append(user_summary)
    await engine.save(photo)
    return photo


  async def unlike_photo(photo_id: ObjectId, acting_user: User):
    """
    Unlike a photo.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)
    if not photo:
      raise ValueError(f'Photo with id {photo_id} not found')
    
    photo.likes = [like for like in photo.likes if like.user_id != acting_user.id]
    await engine.save(photo)
    return photo


  async def add_comment(photo_id: ObjectId, new_comment: CreateComment, acting_user: User):
    """
    Add a new top-level comment to a photo.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)
    if not photo:
      raise ValueError(f'Photo with id {photo_id} not found')

    user_summary = PhotoView._build_user_summary(acting_user)

    comment = Comment(
      user_summary=user_summary,
      comment_date=datetime.now(),
      content=new_comment.content
    )

    photo.comments.append(comment)
    await engine.save(photo)
    return photo


  async def reply_to_comment(photo_id: ObjectId, comment_id: ObjectId, new_comment: CreateComment, acting_user: User):
    """
    Add a reply to an existing comment on a photo.
    """
    photo = await engine.find_one(Photo, Photo.id == photo_id)
    if not photo:
      raise ValueError(f'Photo with id {photo_id} not found')

    target_comment = PhotoView._find_comment(photo.comments, comment_id)
    if not target_comment:
      raise ValueError(f'Comment with id {comment_id} not found on this photo')

    user_summary = PhotoView._build_user_summary(acting_user)

    reply = Comment(
      user_summary=user_summary,
      comment_date=datetime.now(),
      content=new_comment.content
    )

    target_comment.replies.append(reply)
    await engine.save(photo)
    return photo