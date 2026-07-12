from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services import report_service

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _send(data, fmt, filename, title):
    if fmt == "csv":
        content = report_service.generate_csv(data)
        return Response(content=content, media_type="text/csv",
                        headers={"Content-Disposition": f"attachment; filename={filename}.csv"})
    elif fmt == "xlsx":
        content = report_service.generate_excel(data, title)
        return Response(content=content,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        headers={"Content-Disposition": f"attachment; filename={filename}.xlsx"})
    else:
        content = report_service.generate_pdf(title, data)
        return Response(content=content, media_type="application/pdf",
                        headers={"Content-Disposition": f"attachment; filename={filename}.pdf"})


@router.get("/environmental")
def environmental_report(
    department_id: int = None,
    fmt: str = Query("json", regex="^(json|csv|xlsx|pdf)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    data = report_service.get_environmental_report(db, department_id)
    if fmt == "json":
        return data
    return _send(data, fmt, "environmental_report", "Environmental Report")


@router.get("/social")
def social_report(
    department_id: int = None,
    fmt: str = Query("json", regex="^(json|csv|xlsx|pdf)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    data = report_service.get_social_report(db, department_id)
    if fmt == "json":
        return data
    return _send(data, fmt, "social_report", "Social Report")


@router.get("/governance")
def governance_report(
    fmt: str = Query("json", regex="^(json|csv|xlsx|pdf)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    data = report_service.get_governance_report(db)
    if fmt == "json":
        return data
    return _send(data, fmt, "governance_report", "Governance Report")


@router.get("/summary")
def summary_report(
    fmt: str = Query("json", regex="^(json|csv|xlsx|pdf)$"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    data = report_service.get_esg_summary_report(db)
    if fmt == "json":
        return data
    return _send(data, fmt, "esg_summary", "ESG Summary Report")
