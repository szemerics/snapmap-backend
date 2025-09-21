from db.db import engine
from schemas.comment import Comment

class CommentService:

  async def get_comment_by_name(name: str):
    comment = await engine.find_one(Comment, Comment.name == name)

    return comment