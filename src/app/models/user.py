from odmantic import Field, Model
from pydantic import BaseModel
from typing import Optional

class Gear(BaseModel):
    camera: str
    lens: str
    extra_attachment: Optional[str] = None

class User(Model):
    name: str = Field(min_length=3)
    gears: Optional[list[Gear]] = None
