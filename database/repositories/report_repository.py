from __future__ import annotations

from datetime import datetime

from sqlalchemy import select

from database.db import get_session
from database.models import Report


class ReportRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def create_report(self, patient_id, examination_id=None, report_type=None, report_title=None, report_status="DRAFT",
                      report_date=None, report_reference=None, report_file_path=None, report_file_type=None,
                      report_file_size=None, report_text=None, checksum=None, generated_by=None,
                      model_name=None, model_version=None):
        latest = self.get_latest_report(patient_id, report_type)
        version = 1 if latest is None else latest.report_version + 1
        report = Report(
            patient_id=patient_id,
            examination_id=examination_id,
            report_type=report_type,
            report_title=report_title,
            report_version=version,
            report_status=report_status,
            report_date=report_date,
            report_reference=report_reference,
            report_file_path=report_file_path,
            report_file_type=report_file_type,
            report_file_size=report_file_size,
            report_text=report_text,
            checksum=checksum,
            generated_by=generated_by,
            model_name=model_name,
            model_version=model_version,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(report)
        self.session.commit()
        self.session.refresh(report)
        return report

    def get_by_id(self, report_id):
        return self.session.execute(select(Report).where(Report.id == report_id)).scalar_one_or_none()

    def get_latest_report(self, patient_id, report_type=None):
        stmt = select(Report).where(Report.patient_id == patient_id)
        if report_type:
            stmt = stmt.where(Report.report_type == report_type)
        stmt = stmt.order_by(Report.report_version.desc(), Report.created_at.desc())
        return self.session.execute(stmt).scalars().first()

    def get_report_history(self, patient_id, report_type=None):
        stmt = select(Report).where(Report.patient_id == patient_id)
        if report_type:
            stmt = stmt.where(Report.report_type == report_type)
        stmt = stmt.order_by(Report.report_version.asc(), Report.created_at.asc())
        return self.session.execute(stmt).scalars().all()

    def get_by_examination(self, examination_id):
        stmt = select(Report).where(Report.examination_id == examination_id)
        return self.session.execute(stmt).scalars().all()

    def get_by_type(self, report_type):
        stmt = select(Report).where(Report.report_type == report_type)
        return self.session.execute(stmt).scalars().all()
