from __future__ import annotations

from datetime import datetime

from sqlalchemy import select

from database.db import get_session
from database.models import AnalysisResult


class AnalysisRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def store_result(self, patient_id, examination_id=None, prediction_id=None, result_type="OTHER",
                     result_version=None, result_data=None):
        result = AnalysisResult(
            patient_id=patient_id,
            examination_id=examination_id,
            prediction_id=prediction_id,
            result_type=result_type,
            result_version=result_version,
            result_data=result_data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result

    def get_by_prediction(self, prediction_id):
        stmt = select(AnalysisResult).where(AnalysisResult.prediction_id == prediction_id)
        return self.session.execute(stmt).scalars().all()

    def get_by_patient(self, patient_id):
        stmt = select(AnalysisResult).where(AnalysisResult.patient_id == patient_id)
        return self.session.execute(stmt).scalars().all()

    def get_by_examination(self, examination_id):
        stmt = select(AnalysisResult).where(AnalysisResult.examination_id == examination_id)
        return self.session.execute(stmt).scalars().all()
