from fastapi import APIRouter
from app.views.comment import CommentView

router = APIRouter()

@router.get("/")
async def read_root():
    return await CommentView.get_comment_by_name('Mercedes Tyler') 