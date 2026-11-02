from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.db import get_session
from database.models import Examination


class ExaminationRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def create_examination(self, patient_id, examination_code=None, examination_date=None, modality=None, body_region=None,
                           clinical_context=None, referring_context=None, notes=None, model_version=None):
        exam = Examination(
            patient_id=patient_id,
            examination_code=examination_code,
            examination_date=examination_date,
            modality=modality,
            body_region=body_region,
            clinical_context=clinical_context,
            referring_context=referring_context,
            notes=notes,
            model_version=model_version,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        try:
            self.session.add(exam)
            self.session.commit()
            self.session.refresh(exam)
            return exam
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError("Invalid examination data or duplicate examination code for patient") from exc

    def get_by_id(self, examination_id):
        return self.session.execute(select(Examination).where(Examination.id == examination_id)).scalar_one_or_none()

    def get_by_patient(self, patient_id):
        stmt = select(Examination).where(Examination.patient_id == patient_id).order_by(Examination.examination_date.desc())
        return self.session.execute(stmt).scalars().all()

    def list(self, patient_id=None):
        stmt = select(Examination)
        if patient_id:
            stmt = stmt.where(Examination.patient_id == patient_id)
        return self.session.execute(stmt).scalars().all()
