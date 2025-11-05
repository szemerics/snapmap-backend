from app.config import engine
from app.models.user import User

class UserView:

  async def get_all_users():
    """
    Get all users from the database.
    """
    users = await engine.find(User)

    return users


  async def create_user(user: User):
    """
    Create a new user in the database.
    """
    new_user = await engine.save(user)

    return new_user