from datetime import timedelta, datetime
import os
from fastapi import Response
import jwt
from odmantic import ObjectId
from pydantic import BaseModel
from app.config import engine
from app.models.user import User, UserRole
from dotenv import load_dotenv

load_dotenv()

class TokenUser(BaseModel):
    id: ObjectId
    username: str
    email: str
    role: UserRole

class AuthResponse(BaseModel):
    access_token: str
    user: TokenUser


class TokenService: 
    def __init__(self):
        self.SECRET_KEY = os.getenv('JWT_SECRET_KEY')
        self.APP_ENV = os.getenv('APP_ENV')
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 10
        self.REFRESH_TOKEN_EXPIRE_DAYS = 30


    async def generate_token(self, user: User):
        payload = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role.value,
        }

        to_encode = payload.copy()
        expire = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    
    async def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    
    async def set_refresh_cookie(self, response: Response, refresh_token: str):
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=self.APP_ENV == "prod",
            samesite="none" if self.APP_ENV == "prod" else "lax",
            max_age=self.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )

    async def delete_refresh_cookie(self, response: Response):
        response.delete_cookie(key="refresh_token")