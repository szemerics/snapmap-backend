from odmantic import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.report import ReportStatus
from app.views.report import ReportView
from app.utils.auth import auth

router = APIRouter()
security = HTTPBearer()


@router.get("/", tags=["Admin"])
async def get_all_reports(credentials: HTTPAuthorizationCredentials = Depends(security)):
    '''Retrieves all reports'''
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)

    try:
        reports = await ReportView.get_all_reports(acting_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return reports


@router.post('/report-photo', tags=["Report"])
async def report_photo(target_report: ObjectId, reason: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    '''Reports a photo'''
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)

    try:
      created_report = await ReportView.create_report(target_report, reason, acting_user)
    except PermissionError as e:
      raise HTTPException(status_code=403, detail=str(e))

    return created_report


@router.put("/update-report", tags=["Admin"])
async def update_report(target_report_id: ObjectId, status: ReportStatus, credentials: HTTPAuthorizationCredentials = Depends(security)):
    '''Updates the status of a report'''
    token = credentials.credentials
    acting_user = await auth.get_current_user(token)

    try:
      updated_report = await ReportView.update_report(target_report_id, status, acting_user)
    except PermissionError as e:
      raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
      raise HTTPException(status_code=404, detail=str(e))
    
    return updated_report