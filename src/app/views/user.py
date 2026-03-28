from typing import Optional, List
from fastapi import File
from app.config import engine
from app.models.user import User, UserRole, UserUpdate, ProfilePicture, FollowUser, FollowCounts
from app.models.photo import Comment, Photo
from app.models.follow import Follow
from odmantic import ObjectId

from app.utils.images import CloudinaryService


class UserView:

  @staticmethod
  def _build_follow_user(user: User) -> FollowUser:
    return FollowUser(
      user_id=str(user.id),
      username=user.username,
      profile_picture=user.profile_picture,
      bio=user.bio
    )

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

    photos: List[Photo] = await engine.find(Photo)

    for photo in photos:
      _update_user_summary(photo.user_summary)

      if photo.likes:
        for like in photo.likes:
          _update_user_summary(like)

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


  async def follow_user(target_user_id: ObjectId, acting_user: User):
    """
    Follow another user.
    """
    if target_user_id == acting_user.id:
      raise ValueError("You cannot follow yourself")

    target_user = await engine.find_one(User, User.id == target_user_id)
    if target_user is None:
      raise ValueError("User not found")

    existing_follow = await engine.find_one(
      Follow,
      (Follow.follower_id == acting_user.id) & (Follow.followee_id == target_user_id)
    )
    if existing_follow:
      raise ValueError("You already follow this user")

    follow = Follow(
      follower_id=acting_user.id,
      followee_id=target_user_id
    )
    await engine.save(follow)

    return {"message": "User followed successfully"}


  async def unfollow_user(target_user_id: ObjectId, acting_user: User):
    """
    Unfollow a user.
    """
    follow = await engine.find_one(
      Follow,
      (Follow.follower_id == acting_user.id) & (Follow.followee_id == target_user_id)
    )
    if follow is None:
      raise ValueError("You do not follow this user")

    await engine.delete(follow)

    return {"message": "User unfollowed successfully"}


  async def get_followers(user_id: ObjectId):
    """
    Get users that follow the target user.
    """
    user = await engine.find_one(User, User.id == user_id)
    if user is None:
      raise ValueError("User not found")

    follows = await engine.find(Follow, Follow.followee_id == user_id)
    followers: List[FollowUser] = []

    for follow in follows:
      follower = await engine.find_one(User, User.id == follow.follower_id)
      if follower:
        followers.append(UserView._build_follow_user(follower))

    return followers


  async def get_following(user_id: ObjectId):
    """
    Get users that the target user follows.
    """
    user = await engine.find_one(User, User.id == user_id)
    if user is None:
      raise ValueError("User not found")

    follows = await engine.find(Follow, Follow.follower_id == user_id)
    following: List[FollowUser] = []

    for follow in follows:
      followed_user = await engine.find_one(User, User.id == follow.followee_id)
      if followed_user:
        following.append(UserView._build_follow_user(followed_user))

    return following


  async def get_follow_counts(user_id: ObjectId):
    """
    Get follower and following counts for a user.
    """
    user = await engine.find_one(User, User.id == user_id)
    if user is None:
      raise ValueError("User not found")

    followers = await engine.find(Follow, Follow.followee_id == user_id)
    following = await engine.find(Follow, Follow.follower_id == user_id)

    return FollowCounts(
      followers=len(followers),
      following=len(following)
    )
  

  async def get_follow_state(target_user_id: ObjectId, acting_user: User):
    """
    Get the follow state between the acting user and the target user.
    """
    if target_user_id == acting_user.id:
      raise ValueError("You cannot follow yourself")

    target_user = await engine.find_one(User, User.id == target_user_id)
    if target_user is None:
      raise ValueError("User not found")

    existing_follow = await engine.find_one(
      Follow,
      (Follow.follower_id == acting_user.id) & (Follow.followee_id == target_user_id)
    )

    return {"is_following": existing_follow is not None}