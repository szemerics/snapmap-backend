from fastapi import FastAPI
from app.routers.comment import router as comment_router
from app.routers.photo import router as map_router
from app.routers.user import router as user_router
from app.config import configure_cloudinary

from app.utils.images import CloudinaryService

app = FastAPI()
configure_cloudinary()

app.include_router(comment_router, prefix='/api/comments', tags=['Comments'])
app.include_router(map_router, prefix='/api/photos', tags=['Photos'])
app.include_router(user_router, prefix='/api/users', tags=['Users'])