from app.config import engine
from app.models.comment import Comment

class CommentView:

  async def get_comment_by_name(name: str):
    comment = await engine.find_one(Comment, Comment.name == name)

    return comment