from __future__ import annotations

from database.db import init_db, get_session
from database.models import Patient, Examination, MedicalImage, Prediction, AnalysisResult, Report, Experiment, ExperimentMetric, ModelRegistry
from database.repositories import (
    AnalysisRepository,
    ExperimentRepository,
    ExaminationRepository,
    HistoryRepository,
    ImageRepository,
    ModelRepository,
    PatientRepository,
    PredictionRepository,
    ReportRepository,
)


def seed_demo_data():
    init_db()
    session = get_session()

    patient_repo = PatientRepository(session=session)
    history_repo = HistoryRepository(session=session)
    examination_repo = ExaminationRepository(session=session)
    image_repo = ImageRepository(session=session)
    prediction_repo = PredictionRepository(session=session)
    analysis_repo = AnalysisRepository(session=session)
    report_repo = ReportRepository(session=session)
    experiment_repo = ExperimentRepository(session=session)
    model_repo = ModelRepository(session=session)

    existing = session.query(Patient).first()
    if existing:
        return {"status": "demo data already exists"}

    patient = patient_repo.create_patient(
        patient_code="DEMO-PAT-001",
        age=42,
        sex="F",
        research_notes="DEMO DATA ONLY",
    )
    history_repo.create_history(
        patient_id=patient.patient_id,
        record_date="2024-01-15",
        history_type="RESEARCH",
        description="DEMO DATA",
        notes="Seed record for development only",
    )
    examination = examination_repo.create_examination(
        patient.id,
        examination_code="DEMO-EXAM-001",
        examination_date="2024-02-01",
        modality="XRAY",
        body_region="CHEST",
        clinical_context="DEMO DATA",
    )
    image = image_repo.register_image(
        patient_id=patient.patient_id,
        examination_id=examination.id,
        file_reference="/demo/upload/demo-image.png",
        original_filename="demo-image.png",
        stored_filename="demo-image.png",
        file_type="image/png",
        file_size=120000,
        image_width=1024,
        image_height=768,
        checksum="DEMO_CHECKSUM",
    )
    prediction = prediction_repo.create_prediction(
        patient_id=patient.patient_id,
        examination_id=examination.id,
        image_id=image.id,
        class_id=1,
        class_name="abnormality",
        confidence=0.91,
        x1=50,
        y1=60,
        x2=180,
        y2=220,
        model_name="DEMO-MODEL",
        model_version="1.0.0",
    )
    analysis_repo.store_result(
        patient_id=patient.patient_id,
        examination_id=examination.id,
        prediction_id=prediction.id,
        result_type="CALIBRATION",
        result_version="1.0.0",
        result_data={"status": "DEMO DATA", "calibrated_confidence": 0.9},
    )
    report_repo.create_report(
        patient_id=patient.patient_id,
        examination_id=examination.id,
        report_type="AI_ANALYSIS_REPORT",
        report_title="Demo Report",
        report_text="DEMO DATA ONLY",
        model_name="DEMO-MODEL",
        model_version="1.0.0",
    )
    experiment = experiment_repo.create_experiment(
        experiment_name="DEMO-EXPERIMENT",
        dataset_name="DEMO-DATASET",
        model_name="DEMO-MODEL",
        model_version="1.0.0",
        configuration={"notes": "DEMO DATA"},
        notes="DEMO DATA ONLY",
        status="COMPLETED",
    )
    experiment_repo.add_metric(experiment.id, "F1", 0.89, "score")
    model_repo.register_model(
        model_name="DEMO-MODEL",
        version="1.0.0",
        file_reference="/demo/models/demo-model.pt",
        framework="PyTorch",
        device="CPU",
        description="DEMO DATA",
    )
    session.close()
    return {"status": "demo data loaded"}
