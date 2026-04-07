import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "dev").lower()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/?directConnection=true")
DATABASE_NAME = os.getenv("DATABASE_NAME", "snapmap_db")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "dyhnln455")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
CLOUDINARY_UPLOAD_FOLDER = os.getenv(
    "CLOUDINARY_UPLOAD_FOLDER",
    "snapmap-dev" if APP_ENV == "dev" else "snapmap-prod",
)

NSFW_MODE = os.getenv("NSFW_MODE", "local" if APP_ENV == "dev" else "api").lower()
NSFW_LOCAL_MODEL_PATH = os.getenv("NSFW_LOCAL_MODEL_PATH", "./nsfw_model")
NSFW_API_TOKEN = os.getenv("NSFW_API_TOKEN")
