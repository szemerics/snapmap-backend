from datetime import datetime
from odmantic import Field, Model
from pydantic import BaseModel, EmailStr
from typing import Optional

class Gear(BaseModel):
    camera: str
    lens: str
    extra_attachment: Optional[str] = None


class User(Model):
    username: str = Field(min_length=3, unique=True)
    email: EmailStr = Field(unique=True)
    password_hash: str
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