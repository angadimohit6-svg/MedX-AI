import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "medx-research-prototype")
    MODEL_PATH = os.getenv("MODEL_PATH", "models/best.pt")
    DEVICE = os.getenv("DEVICE", "auto")
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "20"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    UPLOAD_DIR = ROOT / "uploads"
    RESULT_DIR = ROOT / "results"


settings = Settings()
settings.UPLOAD_DIR.mkdir(exist_ok=True)
settings.RESULT_DIR.mkdir(exist_ok=True)
