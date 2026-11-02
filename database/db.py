import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DEFAULT_DATABASE_URL = "sqlite:///medx_ai.db"
_engine = None
_session_factory = None


def get_database_url():
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_engine(database_url=None):
    global _engine
    if database_url is not None:
        return create_engine(database_url, future=True, echo=False)
    if _engine is None:
        _engine = create_engine(get_database_url(), future=True, echo=False)
    return _engine


def get_session_factory(database_url=None):
    global _session_factory
    if database_url is not None:
        return sessionmaker(bind=create_engine(database_url, future=True, echo=False), autoflush=False, autocommit=False, expire_on_commit=False)
    if _session_factory is None:
        _session_factory = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, expire_on_commit=False)
    return _session_factory


def get_session(database_url=None):
    return get_session_factory(database_url)()


def init_db(database_url=None):
    from .models import (
        AnalysisResult,
        AuditLog,
        ArchivedRecord,
        Examination,
        Experiment,
        ExperimentMetric,
        MedicalImage,
        ModelRegistry,
        Patient,
        PatientHistory,
        Prediction,
        Report,
    )

    global _engine, _session_factory
    db_url = database_url or get_database_url()
    _engine = create_engine(db_url, future=True, echo=False)
    _session_factory = sessionmaker(bind=_engine, autoflush=False, autocommit=False, expire_on_commit=False)
    Base.metadata.create_all(bind=_engine)
    return _engine
