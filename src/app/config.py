import os
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from dotenv import load_dotenv
import cloudinary
load_dotenv()

# MongoDB config
__mongodb_uri = os.getenv('MONGODB_URI')
__database = os.getenv('DATABASE_NAME')
__client = AsyncIOMotorClient(__mongodb_uri, tlsAllowInvalidCertificates=True)

engine = AIOEngine(client=__client, database=__database)

# Cloudinary config
__cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY')
__cloudinary_api_secret = os.getenv('CLOUDINARY_API_SECRET')

def configure_cloudinary():

  cloudinary.config(
    cloud_name="dyhnln455",
    api_key = __cloudinary_api_key,
    api_secret = __cloudinary_api_secret,
    secure = True
  )
