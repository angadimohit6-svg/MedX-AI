from __future__ import annotations

from datetime import datetime

from sqlalchemy import select

from database.db import get_session
from database.models import Experiment, ExperimentMetric


class ExperimentRepository:
    def __init__(self, session=None):
        self.session = session or get_session()

    def create_experiment(self, experiment_name, dataset_name=None, model_name=None, model_version=None,
                          configuration=None, notes=None, status="PLANNED"):
        experiment = Experiment(
            experiment_name=experiment_name,
            dataset_name=dataset_name,
            model_name=model_name,
            model_version=model_version,
            configuration=configuration,
            notes=notes,
            status=status,
            created_at=datetime.utcnow(),
        )
        self.session.add(experiment)
        self.session.commit()
        self.session.refresh(experiment)
        return experiment

    def add_metric(self, experiment_id, metric_name, metric_value=None, metric_unit=None):
        metric = ExperimentMetric(
            experiment_id=experiment_id,
            metric_name=metric_name,
            metric_value=metric_value,
            metric_unit=metric_unit,
            created_at=datetime.utcnow(),
        )
        self.session.add(metric)
        self.session.commit()
        self.session.refresh(metric)
        return metric

    def get_by_id(self, experiment_id):
        return self.session.execute(select(Experiment).where(Experiment.id == experiment_id)).scalar_one_or_none()

    def list(self):
        return self.session.execute(select(Experiment).order_by(Experiment.created_at.desc())).scalars().all()
