from odmantic import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from app.models.report import ReportStatus
from app.models.user import User
from app.views.report import ReportView
from app.utils.auth import auth

router = APIRouter()


@router.get("/", tags=["Admin"])
async def get_all_reports(acting_user: User = Depends(auth.get_current_user)):
    '''Retrieves all reports'''
    try:
        reports = await ReportView.get_all_reports(acting_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return reports


@router.post('/report-photo', tags=["Report"])
async def report_photo(
    target_report: ObjectId,
    reason: str,
    acting_user: User = Depends(auth.get_current_user),
):
    '''Reports a photo'''
    try:
        created_report = await ReportView.create_report(target_report, reason, acting_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return created_report


@router.put("/update-report", tags=["Admin"])
async def update_report(
    target_report_id: ObjectId,
    status: ReportStatus,
    acting_user: User = Depends(auth.get_current_user),
):
    '''Updates the status of a report'''
    try:
        updated_report = await ReportView.update_report(target_report_id, status, acting_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_report