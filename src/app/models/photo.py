from odmantic import Field as ODMField, Model, ObjectId
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.user import UserSummary
from app.models.additional_data import Gear, Settings

class Location(BaseModel):
    lat: float
    lng: float


class Comment(BaseModel):
    comment_id: ObjectId = Field(default_factory=ObjectId)
    user_summary: UserSummary
    comment_date: datetime = Field(default_factory=datetime.now)
    content: str
    replies: List['Comment'] = Field(default_factory=list)

    model_config = {
        "arbitrary_types_allowed": True
    }


class CreateComment(BaseModel):
    content: str


class Photo(Model):
    # Default data
    user_summary: UserSummary
    photo_url: str
    cloudinary_public_id: str  # Store Cloudinary public_id for deletions/updates

    location: Optional[Location] = None

    # Metadata
    date_captured: datetime
    category: str
    gear: Optional[Gear] = None
    settings_used: Optional[Settings] = None

    # Post
    date_posted: datetime = ODMField(default_factory=datetime.now)
    caption: Optional[str] = None
    likes: List[UserSummary] = ODMField(default_factory=list)
    comments: List[Comment] = ODMField(default_factory=list)

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
