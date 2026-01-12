
from datetime import datetime
from bson import ObjectId
from app.models.report import Report, ReportStatus
from app.models.user import User, UserRole, UserSummary
from app.config import engine

class ReportView:

  async def get_all_reports(acting_user: User):
    '''Retrieves all reports - only admins and moderators can access'''
    if (acting_user.role == UserRole.USER):
      raise PermissionError('No access')

    reports = await engine.find(Report)

    return reports
  

  async def create_report(target_report: ObjectId, reason: str, acting_user: User):
    '''Reports a photo - any user can submit a report'''
    user_summary = UserSummary(
      user_id=acting_user.id,
      username=acting_user.username,
      profile_picture_url=acting_user.profile_picture_url,
      bio=acting_user.bio
    )

    report = Report(
      target_photo=target_report,
      reporter=user_summary,
      reason=reason,
      status=ReportStatus.PENDING,
      created_at=datetime.now()
    )

    created_report = await engine.save(report)
    return created_report
  

  async def update_report(report_id: ObjectId, status: ReportStatus, acting_user: User):
    '''Updates the status of a report - only admins and moderators can access'''
    if (acting_user.role == UserRole.USER):
      raise PermissionError('No access')
    
    report = await engine.find_one(Report, (Report.id == report_id))

    if not report:
      raise ValueError(f'Report with id {report_id} not found')

    report.status = status
    saved_report = await engine.save(report)

    return saved_report