from app.config import engine
from app.models.user import User

class UserView:

  async def get_all_users():
    users = await engine.find(User)

    return users


  async def create_user(user: User):
    new_user = await engine.save(user)

    return new_user