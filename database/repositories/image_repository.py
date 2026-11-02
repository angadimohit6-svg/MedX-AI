from __future__ import annotations

from datetime import datetime

from sqlalchemy import select

from database.db import get_session
from database.models import MedicalImage


class ImageRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def register_image(self, patient_id, examination_id=None, file_reference=None, original_filename=None,
                       stored_filename=None, file_type=None, file_size=None, image_width=None,
                       image_height=None, checksum=None):
        image = MedicalImage(
            patient_id=patient_id,
            examination_id=examination_id,
            file_reference=file_reference,
            original_filename=original_filename,
            stored_filename=stored_filename,
            file_type=file_type,
            file_size=file_size,
            image_width=image_width,
            image_height=image_height,
            checksum=checksum,
            uploaded_at=datetime.utcnow(),
        )
        self.session.add(image)
        self.session.commit()
        self.session.refresh(image)
        return image

    def get_by_id(self, image_id):
        return self.session.execute(select(MedicalImage).where(MedicalImage.id == image_id)).scalar_one_or_none()

    def get_by_examination(self, examination_id):
        stmt = select(MedicalImage).where(MedicalImage.examination_id == examination_id)
        return self.session.execute(stmt).scalars().all()

    def get_by_patient(self, patient_id):
        stmt = select(MedicalImage).where(MedicalImage.patient_id == patient_id)
        return self.session.execute(stmt).scalars().all()
