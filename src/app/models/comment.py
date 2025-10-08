from odmantic import Model
from datetime import datetime
from bson import ObjectId

class Comment(Model):
    name: str
    email: str
    movie_id: ObjectId
    text: str
    date: datetime

    model_config = {
        "collection": "comments"
    }
