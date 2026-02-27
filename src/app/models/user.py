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


class ProfilePicture(EmbeddedModel):
    url: str
    public_id: str


DEFAULT_PROFILE_PICTURE = ProfilePicture(
    url="https://res.cloudinary.com/dyhnln455/image/upload/v1771849294/Default_pfp_oe2fst.svg",
    public_id="default-pfp",
)


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
    profile_picture: ProfilePicture = Field(default=DEFAULT_PROFILE_PICTURE)
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    photo_summaries: List[PhotoSummary] = Field(default_factory=list)

    model_config = {
        "collection": "users"
    }


class UserSummary(EmbeddedModel):
     user_id: ObjectId
     username: str = Field(min_length=3, unique=True)
     profile_picture: ProfilePicture
     bio: Optional[str] = None


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None