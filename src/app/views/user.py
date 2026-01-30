from typing import Optional
from app.config import engine
from app.models.user import User, UserRole
from odmantic import ObjectId

class UserView:

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

    return users
  

  async def set_role(target_user_id: str, role: UserRole, acting_user: User):
    """
    Set the role of a target user.
    """
    if acting_user.role != UserRole.ADMIN:
      raise PermissionError("You have no permission to change user roles.")

    user = await engine.find_one(User, User.id == ObjectId(target_user_id))
    if user is None:
      return None

    user.role = role
    await engine.save(user)

    return user