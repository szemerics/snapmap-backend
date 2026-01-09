import os
from dotenv import load_dotenv
from bcrypt import checkpw, hashpw, gensalt
from app.models.user import UserRegister, User
from app.utils.auth.token import TokenData
from app.views.user import UserView
from datetime import timedelta, datetime
import jwt
from app.utils.auth.token import Token
from app.config import engine


load_dotenv()

__secret_key = os.getenv('JWT_SECRET_KEY')
__algorithm = 'HS256'


async def login_auth(email: str, password: str):
  user = await __authenticate_user(email, password)

  if not user:
    return None

  access_token_expires = timedelta(minutes=1440)
  access_token = await __create_access_token(
      data={"email": user.email, "role": user.role}, expires_delta=access_token_expires
  )

  return Token(access_token=access_token, token_type="bearer")


async def register_auth(user_data: UserRegister):
  is_existing = await engine.find_one(
    User,
    (User.username == user_data.username) | (User.email == user_data.email)
  )

  if is_existing:
    return False
  
  new_user = User(
    username=user_data.username,
    email=user_data.email,
    password_hash=__get_password_hash(user_data.password)
  )

  await engine.save(new_user)
  return new_user


async def get_current_user(token: str):
  try:
    payload = jwt.decode(token, __secret_key, algorithms=__algorithm)
    email = payload.get('email')
    role = payload.get('role')

    if email is None:
      raise ValueError
    
    token_data = TokenData(email=email, role=role)

  except Exception:
    raise ValueError("Could not validate credentials")

  user: User = await UserView.get_user_by_email(token_data.email)

  return user


async def __create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now() + expires_delta
  else:
    expire = datetime.now() + timedelta(minutes=15)

  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, __secret_key, algorithm=__algorithm)
  return encoded_jwt


async def __authenticate_user(email: str, password: str):
  user = await UserView.get_user_by_email(email)

  if not user:
    return False
  if not __verify_password(password, user.password_hash):
    return False
  
  return user
  

def __verify_password(plain_password: str, hashed_password: str) -> bool:
  try:
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
  except:
    return False
  

def __get_password_hash(password: str) -> str:
  return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')