from __future__ import annotations

from datetime import datetime

from sqlalchemy import select

from database.db import get_session
from database.models import PatientHistory


class HistoryRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def create_history(self, patient_id, record_date=None, history_type="GENERAL", description=None, notes=None):
        history = PatientHistory(
            patient_id=patient_id,
            record_date=record_date,
            history_type=history_type,
            description=description,
            notes=notes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(history)
        self.session.commit()
        self.session.refresh(history)
        return history

    def get_by_patient(self, patient_id):
        stmt = select(PatientHistory).where(PatientHistory.patient_id == patient_id).order_by(PatientHistory.record_date.desc())
        return self.session.execute(stmt).scalars().all()

    def list(self, patient_id=None):
        stmt = select(PatientHistory)
        if patient_id:
            stmt = stmt.where(PatientHistory.patient_id == patient_id)
        return self.session.execute(stmt).scalars().all()
