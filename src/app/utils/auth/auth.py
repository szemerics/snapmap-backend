from dotenv import load_dotenv
from bcrypt import checkpw, hashpw, gensalt
from fastapi import Depends, HTTPException, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.models.user import UserLogin, UserRegister, User
from app.utils.auth.token import AuthResponse, TokenService
from app.config import engine


load_dotenv()
security = HTTPBearer()


class AuthService:
  def __init__(self):
    self.token_service = TokenService()


  async def register_auth(self, user_data: UserRegister, response: Response):
    is_existing = await engine.find_one(
      User,
      (User.username == user_data.username) | (User.email == user_data.email)
    )

    if is_existing:
      raise ValueError("User already exists")
    
    new_user = User(
      username=user_data.username,
      email=user_data.email,
      password_hash=self.__get_password_hash(user_data.password)
    )

    access_token = await self.token_service.generate_token(user=new_user, token_use="access")
    refresh_token = await self.token_service.generate_token(user=new_user, token_use="refresh")

    await self.token_service.set_refresh_cookie(response, refresh_token)

    await engine.save(new_user)
    
    return AuthResponse(
      access_token=access_token,
      user=new_user
    )


  async def login_auth(self, user_data: UserLogin, response: Response):
    user = await self.__authenticate_user(user_data.email, user_data.password)

    if not user:
      raise ValueError("Invalid credentials")
      
    access_token = await self.token_service.generate_token(user=user, token_use="access")
    refresh_token = await self.token_service.generate_token(user=user, token_use="refresh")

    await self.token_service.set_refresh_cookie(response, refresh_token)

    return AuthResponse(
      access_token=access_token, 
      user=user
    )


  async def logout_auth(self, response: Response):
    try:
      await self.token_service.delete_refresh_cookie(response)
    except Exception as e:
      raise ValueError(str(e))

    return {"message": "Logged out successfully"}


  async def refresh_auth(self, response: Response, request: Request):
    try:
      refresh_token = request.cookies.get("refresh_token")

      if not refresh_token:
          raise ValueError("No refresh token provided")

      payload = await self.token_service.decode_token(refresh_token)
      user = await engine.find_one(User, User.email == payload.get("email"))

      if not user:
          raise ValueError("User not found")

      new_access_token = await self.token_service.generate_token(user, token_use="access")

      return AuthResponse(
        access_token=new_access_token,
        user=user
      )

    except Exception as e:
        raise Exception(str(e))


  async def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)): 
    try: 
      token = credentials.credentials
      payload = await self.token_service.decode_token(token)
      user = await engine.find_one(User, User.email == payload.get("email"))

      if not user:
        raise ValueError("User not found")

    except ValueError as e:
      raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

    return user


  async def __authenticate_user(self, email: str, password: str):
    user = await engine.find_one(User, User.email == email)

    if not user:
      return False
    if not self.__verify_password(password, user.password_hash):
      return False
    
    return user
    

  def __verify_password(self, plain_password: str, hashed_password: str) -> bool:
    try:
      return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
      return False
    

  def __get_password_hash(self, password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')


auth = AuthService()
