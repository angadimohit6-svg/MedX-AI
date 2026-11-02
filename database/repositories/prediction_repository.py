from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database.db import get_session
from database.models import Prediction


class PredictionRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def create_prediction(self, patient_id, examination_id=None, image_id=None, class_id=None, class_name=None,
                         confidence=None, x1=None, y1=None, x2=None, y2=None, model_id=None, model_name=None,
                         model_version=None, inference_device=None, inference_timestamp=None):
        if confidence is not None and not (0 <= confidence <= 1):
            raise ValueError("Confidence must be between 0 and 1")
        if x1 is not None and x2 is not None and x2 <= x1:
            raise ValueError("x2 must be greater than x1")
        if y1 is not None and y2 is not None and y2 <= y1:
            raise ValueError("y2 must be greater than y1")

        prediction = Prediction(
            patient_id=patient_id,
            examination_id=examination_id,
            image_id=image_id,
            class_id=class_id,
            class_name=class_name,
            confidence=confidence,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            model_id=model_id,
            model_name=model_name,
            model_version=model_version,
            inference_device=inference_device,
            inference_timestamp=inference_timestamp or datetime.utcnow(),
        )
        try:
            self.session.add(prediction)
            self.session.commit()
            self.session.refresh(prediction)
            return prediction
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError("Invalid prediction payload") from exc

    def get_by_id(self, prediction_id):
        return self.session.execute(select(Prediction).where(Prediction.id == prediction_id)).scalar_one_or_none()

    def get_by_image(self, image_id):
        stmt = select(Prediction).where(Prediction.image_id == image_id)
        return self.session.execute(stmt).scalars().all()

    def get_by_patient(self, patient_id):
        stmt = select(Prediction).where(Prediction.patient_id == patient_id)
        return self.session.execute(stmt).scalars().all()
