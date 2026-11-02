from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


def utcnow():
    return datetime.now(timezone.utc)


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    patient_code: Mapped[str | None] = mapped_column(String(128), nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sex: Mapped[str | None] = mapped_column(String(32), nullable=True)
    date_of_birth: Mapped[Date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(64), default="ACTIVE", nullable=False)
    research_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    histories: Mapped[list["PatientHistory"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    examinations: Mapped[list["Examination"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    medical_images: Mapped[list["MedicalImage"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    analysis_results: Mapped[list["AnalysisResult"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    audit_logs: Mapped[list["AuditLog"]] = relationship(back_populates="patient", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("age IS NULL OR age >= 0", name="ck_patients_age_positive"),
        UniqueConstraint("patient_id", name="uq_patients_patient_id"),
        UniqueConstraint("patient_code", name="uq_patients_patient_code"),
    )


class PatientHistory(Base):
    __tablename__ = "patient_history"

    history_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(64), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    record_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    history_type: Mapped[str] = mapped_column(String(64), default="GENERAL", nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="histories")


class Examination(Base):
    __tablename__ = "examinations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(64), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    examination_code: Mapped[str] = mapped_column(String(128), nullable=False)
    examination_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    modality: Mapped[str | None] = mapped_column(String(128), nullable=True)
    body_region: Mapped[str | None] = mapped_column(String(128), nullable=True)
    clinical_context: Mapped[str | None] = mapped_column(Text, nullable=True)
    referring_context: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="examinations")
    medical_images: Mapped[list["MedicalImage"]] = relationship(back_populates="examination", cascade="all, delete-orphan")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="examination", cascade="all, delete-orphan")
    reports: Mapped[list["Report"]] = relationship(back_populates="examination", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("patient_id", "examination_code", name="uq_examination_patient_code"),
        Index("ix_examinations_patient_id", "patient_id"),
        Index("ix_examinations_examination_date", "examination_date"),
    )


class MedicalImage(Base):
    __tablename__ = "medical_images"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(64), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    examination_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("examinations.id", ondelete="SET NULL"), nullable=True)
    file_reference: Mapped[str] = mapped_column(String(512), nullable=False)
    original_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    stored_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    image_height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="medical_images")
    examination: Mapped[Examination | None] = relationship(back_populates="medical_images")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="medical_image", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("file_size IS NULL OR file_size >= 0", name="ck_images_file_size"),
        CheckConstraint("image_width IS NULL OR image_width > 0", name="ck_images_width_positive"),
        CheckConstraint("image_height IS NULL OR image_height > 0", name="ck_images_height_positive"),
    )


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(64), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    examination_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("examinations.id", ondelete="SET NULL"), nullable=True)
    image_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("medical_images.id", ondelete="SET NULL"), nullable=True)
    class_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    class_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Numeric(5, 4), nullable=True)
    x1: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    y1: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    x2: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    y2: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    model_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    inference_device: Mapped[str | None] = mapped_column(String(128), nullable=True)
    inference_timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    patient: Mapped[Patient] = relationship(back_populates="predictions")
    examination: Mapped[Examination | None] = relationship(back_populates="predictions")
    medical_image: Mapped[MedicalImage | None] = relationship(back_populates="predictions")
    analysis_results: Mapped[list["AnalysisResult"]] = relationship(back_populates="prediction", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("confidence IS NULL OR (confidence >= 0 AND confidence <= 1)", name="ck_predictions_confidence_range"),
        CheckConstraint("x1 IS NULL OR x1 >= 0", name="ck_predictions_x1_non_negative"),
        CheckConstraint("y1 IS NULL OR y1 >= 0", name="ck_predictions_y1_non_negative"),
        CheckConstraint("x2 IS NULL OR x1 IS NULL OR x2 > x1", name="ck_predictions_x2_gt_x1"),
        CheckConstraint("y2 IS NULL OR y1 IS NULL OR y2 > y1", name="ck_predictions_y2_gt_y1"),
    )


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(64), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    examination_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("examinations.id", ondelete="SET NULL"), nullable=True)
    prediction_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("predictions.id", ondelete="SET NULL"), nullable=True)
    result_type: Mapped[str] = mapped_column(String(64), default="OTHER", nullable=False)
    result_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    result_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="analysis_results")
    prediction: Mapped[Prediction | None] = relationship(back_populates="analysis_results")


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id: Mapped[str] = mapped_column(String(64), ForeignKey("patients.patient_id", ondelete="CASCADE"), nullable=False)
    examination_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("examinations.id", ondelete="SET NULL"), nullable=True)
    report_type: Mapped[str] = mapped_column(String(128), nullable=False)
    report_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    report_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    report_status: Mapped[str] = mapped_column(String(64), default="DRAFT", nullable=False)
    report_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    report_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    report_file_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    report_file_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    report_file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    report_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(128), nullable=True)
    generated_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    patient: Mapped[Patient] = relationship(back_populates="reports")
    examination: Mapped[Examination | None] = relationship(back_populates="reports")

    __table_args__ = (
        CheckConstraint("report_version >= 1", name="ck_reports_version_positive"),
        CheckConstraint("report_file_size IS NULL OR report_file_size >= 0", name="ck_reports_file_size"),
    )


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dataset_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    configuration: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(64), default="PLANNED", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    metrics: Mapped[list["ExperimentMetric"]] = relationship(back_populates="experiment", cascade="all, delete-orphan")


class ExperimentMetric(Base):
    __tablename__ = "experiment_metrics"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    experiment_id: Mapped[str] = mapped_column(String(64), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(128), nullable=False)
    metric_value: Mapped[float | None] = mapped_column(Numeric(18, 6), nullable=True)
    metric_unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    experiment: Mapped[Experiment] = relationship(back_populates="metrics")


class ModelRegistry(Base):
    __tablename__ = "models"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(128), nullable=False)
    file_reference: Mapped[str | None] = mapped_column(String(512), nullable=True)
    framework: Mapped[str | None] = mapped_column(String(128), nullable=True)
    device: Mapped[str | None] = mapped_column(String(128), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(64), default="ACTIVE", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("model_name", "version", name="uq_models_model_version"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    patient_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("patients.patient_id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String(64), default="SUCCESS", nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    patient: Mapped[Patient | None] = relationship(back_populates="audit_logs")


class ArchivedRecord(Base):
    __tablename__ = "archived_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_type: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(128), nullable=False)
    patient_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    archived_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


Index("ix_patient_history_patient_id", PatientHistory.patient_id)
Index("ix_analysis_results_patient_id", AnalysisResult.patient_id)
Index("ix_analysis_results_prediction_id", AnalysisResult.prediction_id)
Index("ix_reports_patient_id", Report.patient_id)
Index("ix_reports_report_type", Report.report_type)
Index("ix_models_model_name", ModelRegistry.model_name)
Index("ix_audit_logs_patient_id", AuditLog.patient_id)
