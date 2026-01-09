
from typing import Optional
from pydantic import BaseModel


class Camera(BaseModel):
    brand: str
    model: str
    type: str 


class Gear(BaseModel):
    camera: Camera
    lens: str
    extra_attachment: Optional[str] = None


class Settings(BaseModel):
    iso: int
    shutter_speed: str
    aperture: str
