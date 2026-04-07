from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import cloudinary
from app import settings

# MongoDB config
__client = AsyncIOMotorClient(settings.MONGODB_URI, tlsAllowInvalidCertificates=True)

engine = AIOEngine(client=__client, database=settings.DATABASE_NAME)

# Cloudinary config
def configure_cloudinary():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )
