from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.photo import router as map_router
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.config import configure_cloudinary

app = FastAPI()
configure_cloudinary()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix='/api/auth', tags=['Auth'])
app.include_router(map_router, prefix='/api/photos', tags=['Photos'])
app.include_router(user_router, prefix='/api/users', tags=['User'])