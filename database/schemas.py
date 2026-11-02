from dataclasses import dataclass
from typing import Any


@dataclass
class PatientCreateSchema:
    patient_code: str | None = None
    age: int | None = None
    sex: str | None = None
    date_of_birth: str | None = None
    status: str = "ACTIVE"
    research_notes: str | None = None


@dataclass
class ExaminationCreateSchema:
    patient_id: str
    examination_code: str
    examination_date: str | None = None
    modality: str | None = None
    body_region: str | None = None
    clinical_context: str | None = None
    referring_context: str | None = None
    notes: str | None = None
    model_version: str | None = None


@dataclass
class PredictionStoreSchema:
    patient_id: str
    examination_id: str | None = None
    image_id: str | None = None
    class_id: int | None = None
    class_name: str | None = None
    confidence: float | None = None
    x1: float | None = None
    y1: float | None = None
    x2: float | None = None
    y2: float | None = None
    model_id: str | None = None
    model_name: str | None = None
    model_version: str | None = None
    inference_device: str | None = None
    inference_timestamp: str | None = None


@dataclass
class AnalysisResultSchema:
    patient_id: str
    examination_id: str | None = None
    prediction_id: str | None = None
    result_type: str = "OTHER"
    result_version: str | None = None
    result_data: dict[str, Any] | None = None


@dataclass
class ReportCreateSchema:
    patient_id: str
    examination_id: str | None = None
    report_type: str
    report_title: str | None = None
    report_status: str = "DRAFT"
    report_date: str | None = None
    report_reference: str | None = None
    report_file_path: str | None = None
    report_file_type: str | None = None
    report_file_size: int | None = None
    report_text: str | None = None
    checksum: str | None = None
    generated_by: str | None = None
    model_name: str | None = None
    model_version: str | None = None
