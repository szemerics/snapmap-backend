from fastapi import FastAPI
from app.routers.comment import router as comment_router
from app.routers.photo import router as map_router
from app.routers.user import router as user_router

app = FastAPI()

app.include_router(comment_router, prefix='/api/comments', tags=['Comments'])
app.include_router(map_router, prefix='/api/photos', tags=['Map'])
app.include_router(user_router, prefix='/api/users', tags=['Users'])