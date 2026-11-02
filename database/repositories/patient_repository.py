from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.db import get_session
from database.models import Patient


class PatientRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def _generate_patient_id(self):
        last = self.session.execute(select(Patient).order_by(Patient.created_at.desc())).scalars().first()
        count = 1
        if last and last.patient_id:
            try:
                suffix = int(last.patient_id.split("-")[-1])
                count = suffix + 1
            except (ValueError, IndexError):
                pass
        return f"MEDX-PAT-{count:06d}"

    def create_patient(self, patient_code=None, age=None, sex=None, date_of_birth=None, status="ACTIVE", research_notes=None):
        if patient_code:
            existing = self.session.execute(select(Patient).where(Patient.patient_code == patient_code)).scalar_one_or_none()
            if existing is not None:
                raise ValueError("Patient code must be unique")

        patient_id = self._generate_patient_id()
        patient = Patient(
            patient_id=patient_id,
            patient_code=patient_code,
            age=age,
            sex=sex,
            date_of_birth=date_of_birth,
            status=status,
            research_notes=research_notes,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        try:
            self.session.add(patient)
            self.session.commit()
            self.session.refresh(patient)
            return patient
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError("Duplicate patient record or invalid patient data") from exc

    def get_by_id(self, record_id):
        return self.session.execute(select(Patient).where(Patient.id == record_id)).scalar_one_or_none()

    def get_by_patient_id(self, patient_id):
        return self.session.execute(select(Patient).where(Patient.patient_id == patient_id)).scalar_one_or_none()

    def update_patient(self, patient_id, **kwargs):
        patient = self.get_by_patient_id(patient_id)
        if patient is None:
            raise ValueError("Patient not found")
        for key, value in kwargs.items():
            if hasattr(patient, key):
                setattr(patient, key, value)
        patient.updated_at = datetime.utcnow()
        self.session.commit()
        return patient

    def list(self, limit=None):
        stmt = select(Patient).order_by(Patient.created_at.desc())
        if limit:
            stmt = stmt.limit(limit)
        return self.session.execute(stmt).scalars().all()

    def search(self, query: str):
        like = f"%{query}%"
        stmt = select(Patient).where(
            (Patient.patient_id.like(like)) |
            (Patient.patient_code.like(like)) |
            (Patient.sex.like(like))
        )
        return self.session.execute(stmt).scalars().all()
