from app.config import engine
from app.models.user import User, UserRole
from odmantic import ObjectId

class UserView:

  async def get_all_users():
    """
    Get all users from the database.
    """
    users = await engine.find(User)

    return users
  

  async def get_user_by_email(email: str):
    """
    Get a user by their email from the database
    """
    user = await engine.find_one(User, User.email == email)

    return user
  

  async def set_role(target_user_id: str, role: UserRole, acting_user: User):
    if acting_user.role != UserRole.ADMIN:
      raise PermissionError("You have no permission to change user roles.")

    user = await engine.find_one(User, User.id == ObjectId(target_user_id))
    if user is None:
      return None

    user.role = role
    await engine.save(user)

    return user