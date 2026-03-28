from datetime import datetime
from odmantic import Model, ObjectId, Field


class Follow(Model):
    follower_id: ObjectId
    followee_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "collection": "follows"
    }
