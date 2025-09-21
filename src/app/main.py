from fastapi import FastAPI
from routes.comment_router import router as comment_router

app = FastAPI()

app.include_router(comment_router, prefix='/api/comments', tags=['Comments'])