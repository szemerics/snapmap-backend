
from typing import Optional
from pydantic import BaseModel


class Camera(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    type: Optional[str] = None


class Gear(BaseModel):
    camera: Optional[Camera] = None
    lens: Optional[str] = None
    extra_attachment: Optional[str] = None


class Settings(BaseModel):
    iso: Optional[int] = None
    shutter_speed: Optional[str] = None
    aperture: Optional[str] = None
