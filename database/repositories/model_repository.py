from __future__ import annotations

from datetime import datetime

from sqlalchemy import select

from database.db import get_session
from database.models import ModelRegistry


class ModelRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def register_model(self, model_name, version, file_reference=None, framework=None, device=None,
                       description=None, status="ACTIVE"):
        model = ModelRegistry(
            model_name=model_name,
            version=version,
            file_reference=file_reference,
            framework=framework,
            device=device,
            description=description,
            status=status,
            created_at=datetime.utcnow(),
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def get_by_id(self, model_id):
        return self.session.execute(select(ModelRegistry).where(ModelRegistry.id == model_id)).scalar_one_or_none()

    def get_by_name_version(self, model_name, version):
        stmt = select(ModelRegistry).where((ModelRegistry.model_name == model_name) & (ModelRegistry.version == version))
        return self.session.execute(stmt).scalars().first()

    def list(self):
        return self.session.execute(select(ModelRegistry).order_by(ModelRegistry.created_at.desc())).scalars().all()
