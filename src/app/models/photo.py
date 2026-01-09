from odmantic import Field, Model
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.user import UserProfile
from app.models.additional_data import Gear, Settings

class Location(BaseModel):
    lat: float
    lng: float


class Comment(BaseModel):
    user_profile: UserProfile
    comment_date: datetime
    content: str
    likes: int = Field(default=0)
    replies: Optional[List['Comment']] = None  # Allow nested comments


class Photo(Model):
    # Default data
    user_profile: UserProfile
    photo_url: str
    cloudinary_public_id: str  # Store Cloudinary public_id for deletions/updates

    location: Optional[Location] = None

    # Metadata
    date_captured: datetime
    category: str
    gear: Optional[Gear] = None
    settings_used: Optional[Settings] = None

    # Post
    date_posted: datetime
    caption: Optional[str] = None
    likes: int = Field(default=0)
    comments: Optional[List[Comment]] = Field(default=None)

    model_config = {
        "collection": "photos"
    }


class CreatePhoto(BaseModel):
    location: Optional[Location] = None

    # Metadata
    date_captured: datetime
    category: str
    gear: Optional[Gear] = None
    settings_used: Optional[Settings] = None

     # Post
    caption: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True
    }


class UpdatePhoto(BaseModel):
    location: Optional[Location] = None

    # Metadata
    date_captured: Optional[datetime] = None
    category: Optional[str] = None
    gear: Optional[Gear] = None
    settings_used: Optional[Settings] = None

     # Post
    caption: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True
    }
