from datetime import datetime
from odmantic import Field, Model
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class Camera(BaseModel):
    brand: str
    model: str
    type: str 

class Gear(BaseModel):
    camera: Camera
    lens: str
    extra_attachment: Optional[str] = None


class UserRole(str, Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(Model):
    username: str = Field(min_length=3, unique=True)
    email: EmailStr = Field(unique=True)
    password_hash: str
    role: UserRole = Field(default=UserRole.USER)
    gears: Optional[list[Gear]] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "collection": "users"
    }


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str