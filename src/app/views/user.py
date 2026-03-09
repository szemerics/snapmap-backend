from typing import Optional, List
from fastapi import File
from app.config import engine
from app.models.user import User, UserRole, UserUpdate, ProfilePicture
from app.models.photo import Comment, Photo
from odmantic import ObjectId

from app.utils.images import CloudinaryService


class UserView:

  @staticmethod
  async def _update_user_summaries(user: User):
    """
    Update all photo documents to match the user's latest info.
    """
    def _update_user_summary(summary):
      if summary.user_id == user.id:
        summary.username = user.username
        summary.profile_picture = user.profile_picture
        summary.bio = user.bio

    def _update_comment_tree(comments):
      for comment in comments:
        _update_user_summary(comment.user_summary)
        if comment.replies:
          _update_comment_tree(comment.replies)

    photos: List[Photo] = await engine.find(Photo, Photo.user_summary.user_id == user.id)

    for photo in photos:
      # Update photo owner summary
      _update_user_summary(photo.user_summary)

      # Update likes where this user appears
      if photo.likes:
        for like in photo.likes:
          _update_user_summary(like)

      # Update comments (and nested replies) where this user appears
      if photo.comments:
        _update_comment_tree(photo.comments)

      await engine.save(photo)


  async def get_users(username: Optional[str] = None, email: Optional[str] = None):
    """
    Get users from the database with optional filtering by username or email.
    """
    if email:
      users = await engine.find(User, User.email == email)
    elif username:
      users = await engine.find(User, User.username == username)
    else:
      users = await engine.find(User)

    if len(users) == 0:
      raise ValueError("No users found")

    return users
  

  async def set_role(target_user_id: str, role: UserRole, acting_user: User):
    """
    Set the role of a target user.
    """
    if acting_user.role != UserRole.ADMIN:
      raise PermissionError("You have no permission to change user roles.")

    user = await engine.find_one(User, User.id == ObjectId(target_user_id))

    if user is None:
       raise ValueError("User not found")

    user.role = role
    await engine.save(user)

    return user
    
    
  async def update_profile_picture(uploaded_file: File, acting_user: User):
    """
    Update user's profile picture.
    """
    user = await engine.find_one(User, User.id == acting_user.id)
    if user is None:
       raise ValueError("User not found")

    if user.id != acting_user.id:
      raise PermissionError("You have no permission to update this user.")

    public_id = None
    if user.profile_picture and user.profile_picture.public_id != "default-pfp":
      public_id = user.profile_picture.public_id

    upload_result = await CloudinaryService.upload_image(uploaded_file, 'snapmap-pfps', public_id=public_id)

    user.profile_picture = ProfilePicture(
      url=str(upload_result["secure_url"]),
      public_id=str(upload_result["public_id"]),
    )

    await engine.save(user)

    await UserView._update_user_summaries(user)

    return user


  async def update_profile_data(update_data: UserUpdate, acting_user: User):
    """
    Update user's profile: username, bio
    """
    user = await engine.find_one(User, User.id == acting_user.id)
    if user is None:
      raise ValueError("User not found")

    if user.id != acting_user.id:
      raise PermissionError("You have no permission to update this user.")

    if update_data.username:
      user.username = update_data.username
    if update_data.bio:
      user.bio = update_data.bio

    await engine.save(user)

    await UserView._update_user_summaries(user)

    return user