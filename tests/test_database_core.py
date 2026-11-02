import pytest

from database import init_db
from database.repositories.patient_repository import PatientRepository
from database.repositories.examination_repository import ExaminationRepository
from database.repositories.prediction_repository import PredictionRepository
from database.repositories.report_repository import ReportRepository


@pytest.fixture
def db_path(tmp_path):
    db_url = f"sqlite:///{tmp_path / 'medx_test.db'}"
    init_db(db_url)
    return db_url


def test_patient_lifecycle_and_duplicate_rejection(db_path):
    repo = PatientRepository()

    patient = repo.create_patient(
        patient_code="P-001",
        age=45,
        sex="F",
        research_notes="demo patient",
    )

    assert patient.patient_id.startswith("MEDX-PAT-")
    assert repo.get_by_id(patient.id).patient_id == patient.patient_id

    with pytest.raises(ValueError):
        repo.create_patient(
            patient_code="P-001",
            age=30,
            sex="M",
            research_notes="duplicate code",
        )


def test_examination_and_prediction_validation(db_path):
    patient_repo = PatientRepository()
    exam_repo = ExaminationRepository()
    pred_repo = PredictionRepository()

    patient = patient_repo.create_patient(patient_code="P-002", age=60, sex="M")
    exam = exam_repo.create_examination(patient.id, examination_code="EX-01", modality="XRAY")

    prediction = pred_repo.create_prediction(
        patient_id=patient.id,
        examination_id=exam.id,
        image_id=None,
        class_id=1,
        class_name="abnormality",
        confidence=0.88,
        x1=10,
        y1=20,
        x2=100,
        y2=150,
        model_name="demo-model",
        model_version="1.0.0",
    )

    assert 0 <= prediction.confidence <= 1
    assert prediction.x2 > prediction.x1
    assert prediction.y2 > prediction.y1

    with pytest.raises(ValueError):
        pred_repo.create_prediction(
            patient_id=patient.id,
            examination_id=exam.id,
            image_id=None,
            class_id=2,
            class_name="bad",
            confidence=1.5,
            x1=50,
            y1=60,
            x2=40,
            y2=90,
            model_name="demo-model",
            model_version="1.0.0",
        )


def test_report_versioning_and_history(db_path):
    patient_repo = PatientRepository()
    exam_repo = ExaminationRepository()
    report_repo = ReportRepository()

    patient = patient_repo.create_patient(patient_code="P-003", age=32, sex="F")
    exam = exam_repo.create_examination(patient.id, examination_code="EX-02", modality="CT")

    v1 = report_repo.create_report(
        patient_id=patient.id,
        examination_id=exam.id,
        report_type="AI_ANALYSIS_REPORT",
        report_title="Initial Summary",
        report_text="first version",
        model_name="demo-model",
        model_version="1.0.0",
    )

    v2 = report_repo.create_report(
        patient_id=patient.id,
        examination_id=exam.id,
        report_type="AI_ANALYSIS_REPORT",
        report_title="Updated Summary",
        report_text="second version",
        model_name="demo-model",
        model_version="1.0.0",
    )

    assert v1.report_version == 1
    assert v2.report_version == 2
    history = report_repo.get_report_history(patient_id=patient.id, report_type="AI_ANALYSIS_REPORT")
    assert len(history) >= 2
    latest = report_repo.get_latest_report(patient_id=patient.id, report_type="AI_ANALYSIS_REPORT")
    assert latest.id == v2.id
