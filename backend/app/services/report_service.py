import csv
import io
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from openpyxl import Workbook
from app.models.environmental import CarbonTransaction
from app.models.social import CSRActivity
from app.models.governance import ComplianceIssue, Audit
from app.models.esg_score import DepartmentScore


def generate_csv(data: list[dict]) -> bytes:
    if not data:
        return b""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue().encode()


def generate_excel(data: list[dict], sheet_name: str = "Report") -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    if not data:
        output = io.BytesIO()
        wb.save(output)
        return output.getvalue()
    headers = list(data[0].keys())
    ws.append(headers)
    for row in data:
        ws.append([str(row.get(h, "")) for h in headers])
    output = io.BytesIO()
    wb.save(output)
    return output.getvalue()


def generate_pdf(title: str, data: list[dict]) -> bytes:
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles["Title"]), Spacer(1, 20)]

    if data:
        headers = list(data[0].keys())
        table_data = [headers] + [[str(row.get(h, "")) for h in headers] for row in data]
        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))
        elements.append(table)

    doc.build(elements)
    return output.getvalue()


def get_environmental_report(db: Session, department_id: int = None):
    q = db.query(CarbonTransaction)
    if department_id:
        q = q.filter(CarbonTransaction.department_id == department_id)
    rows = q.order_by(CarbonTransaction.date.desc()).all()
    return [
        {
            "id": r.id,
            "department_id": r.department_id,
            "source_type": r.source_type.value,
            "quantity": r.quantity,
            "co2_equivalent": r.co2_equivalent,
            "auto_generated": r.auto_generated,
            "date": str(r.date),
        }
        for r in rows
    ]


def get_social_report(db: Session, department_id: int = None):
    q = db.query(CSRActivity)
    if department_id:
        q = q.filter(CSRActivity.department_id == department_id)
    rows = q.all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "department_id": r.department_id,
            "xp_reward": r.xp_reward,
            "start_date": str(r.start_date),
        }
        for r in rows
    ]


def get_governance_report(db: Session):
    issues = db.query(ComplianceIssue).all()
    return [
        {
            "id": i.id,
            "title": i.title,
            "status": i.status.value,
            "severity": i.severity,
            "due_date": str(i.due_date),
        }
        for i in issues
    ]


def get_esg_summary_report(db: Session):
    scores = db.query(DepartmentScore).order_by(DepartmentScore.calculated_at.desc()).all()
    return [
        {
            "department_id": s.department_id,
            "environmental_score": s.environmental_score,
            "social_score": s.social_score,
            "governance_score": s.governance_score,
            "total_score": s.total_score,
            "period": s.period,
        }
        for s in scores
    ]
