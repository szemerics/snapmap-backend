from fastapi import APIRouter
from services.comment_service import CommentService

router = APIRouter()

@router.get("/")
async def read_root():
    return await CommentService.get_comment_by_name('Mercedes Tyler') 