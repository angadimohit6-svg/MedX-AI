from pathlib import Path
from .config import settings


class ModelManager:
    def __init__(self):
        self.model = None
        self.metadata = None

    def status(self):
        path = Path(settings.MODEL_PATH)
        return {
            "connected": self.model is not None,
            "status": "CONNECTED" if self.model is not None else "NOT CONNECTED",
            "path": str(path),
            "version": self.metadata.get("version") if self.metadata else None,
            "device": self.metadata.get("device") if self.metadata else None,
            "inference": "READY" if self.model is not None else "UNAVAILABLE",
        }

    def connect(self, model=None, metadata=None):
        self.model = model
        self.metadata = metadata or {}
        return self.status()

    def disconnect(self):
        self.model = None
        self.metadata = None
        return self.status()

    def reload(self):
        return self.status()


model_manager = ModelManager()
