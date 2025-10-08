from odmantic import Model, EmbeddedModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel
from app.models.user import Gear

class Location(EmbeddedModel):
    lat: float
    lng: float


class Settings(BaseModel):
    iso: int
    shutter_speed: str
    aperture: str


class Photo(Model):
    user_id: ObjectId
    photo_url: str
    location: Location
    date: datetime
    category: str
    gear: Optional[Gear] = Field(default=None)
    settings_used: Optional[Settings] = None


class CreatePhoto(BaseModel):
    user_id: str
    photo_url: str
    location: Location
    date: datetime
    category: str
    gear: Optional[Gear] = Field(default=None)
    settings_used: Optional[Settings] = None

