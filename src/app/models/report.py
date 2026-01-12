from odmantic import Model
from bson import ObjectId
from enum import Enum
from app.models.user import UserSummary
from datetime import datetime

class ReportStatus(str, Enum):
  PENDING = 'pending'
  RESOLVED = 'resolved'
  DISMISSED = 'dismissed'


class Report(Model):
  target_photo: ObjectId
  reporter: UserSummary
  reason: str
  status: ReportStatus
  created_at: datetime

  model_config = {
    'collection': 'reports',
    'arbitrary_types_allowed': True
  }