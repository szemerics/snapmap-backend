from datetime import datetime
from bson import ObjectId
from odmantic import EmbeddedModel, Field, Model
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum

from app.models.additional_data import Gear


class PhotoSummary(EmbeddedModel):
    photo_id: ObjectId
    photo_url: str


class UserRole(str, Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(Model):
    username: str = Field(min_length=3, unique=True)
    email: EmailStr = Field(unique=True)
    password_hash: str
    role: UserRole = Field(default=UserRole.USER)
    gears: Optional[List[Gear]] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    photo_summaries: List[PhotoSummary] = Field(default_factory=list)

    model_config = {
        "collection": "users"
    }


class UserSummary(EmbeddedModel):
     user_id: ObjectId
     username: str = Field(min_length=3, unique=True)
     profile_picture_url: Optional[str] = None
     bio: Optional[str] = None


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str