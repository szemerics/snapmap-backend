from app.config import engine
from app.models.user import User

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