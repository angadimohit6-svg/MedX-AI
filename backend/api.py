from pathlib import Path
from flask import Blueprint, jsonify, request
from sqlalchemy import inspect, text
from werkzeug.utils import secure_filename
from database import get_engine
from .config import settings
from .gpu import system_snapshot
from .model_manager import model_manager
from .storage import list_results, save_result

api = Blueprint("api", __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "tif", "tiff"}


def response(data, status=200):
    return jsonify(data), status


def unavailable(name):
    return {"name": name, "status": "NOT CONFIGURED", "available": False, "result": None}


@api.get("/health")
def health():
    return response({"status": "online", "service": "MedX AI", "prototype": True})


@api.get("/system")
def system():
    return response(system_snapshot())


@api.get("/database")
def database_status():
    engine = get_engine()
    db_url = str(engine.url)
    provider = "sqlite" if db_url.startswith("sqlite") else "postgresql" if db_url.startswith("postgresql") else "unknown"
    try:
        with engine.connect() as conn:
            tables = inspect(conn).get_table_names()
            conn.execute(text("SELECT 1"))
        payload = {
            "provider": provider,
            "database_url": db_url,
            "status": "ONLINE",
            "initialized": True,
            "tables": tables,
            "notes": "Local research database for MedX AI."
        }
    except Exception as exc:  # pragma: no cover - defensive backend status
        payload = {
            "provider": provider,
            "database_url": db_url,
            "status": "ERROR",
            "initialized": False,
            "tables": [],
            "notes": str(exc)
        }
    return response(payload)


@api.get("/model")
def model():
    return response(model_manager.status())


@api.post("/model/connect")
def connect_model():
    payload = request.get_json(silent=True) or {}
    return response(model_manager.connect(metadata=payload), 200)


@api.post("/model/reload")
def reload_model():
    return response(model_manager.reload())


@api.post("/upload")
def upload():
    image = request.files.get("file")
    if not image or not image.filename:
        return response({"error": "An image file is required."}, 400)
    suffix = Path(image.filename).suffix.lower().lstrip(".")
    if suffix not in ALLOWED_EXTENSIONS:
        return response({"error": "Unsupported image type."}, 415)
    if request.content_length and request.content_length > settings.MAX_UPLOAD_MB * 1024 * 1024:
        return response({"error": "Upload exceeds configured size limit."}, 413)
    filename = secure_filename(image.filename)
    destination = settings.UPLOAD_DIR / filename
    image.save(destination)
    return response({"filename": filename, "path": str(destination.relative_to(settings.UPLOAD_DIR)), "status": "UPLOADED"}, 201)


@api.post("/analyze")
def analyze():
    if not model_manager.status()["connected"]:
        return response({"error": "Model is not connected.", "status": "NOT CONFIGURED"}, 409)
    return response({"status": "NOT CONFIGURED", "result": None}, 501)


@api.post("/<stage>")
def stage(stage):
    supported = {"calibrate", "uncertainty", "xai", "quantification", "severity", "degrade"}
    if stage not in supported:
        return response({"error": "Unknown research stage."}, 404)
    return response(unavailable(stage), 501)


@api.get("/results")
def results():
    return response({"results": list_results()})


@api.get("/experiments")
def experiments():
    return response({"experiments": []})


@api.post("/experiments")
def create_experiment():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return response({"error": "Expected a JSON object."}, 400)
    return response(save_result({"type": "experiment", "status": "DRAFT", **payload}), 201)
