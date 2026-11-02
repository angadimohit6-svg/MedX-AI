import json
from pathlib import Path
from datetime import datetime, timezone
from .config import settings


def save_result(payload):
    result_id = payload.get("id") or f"result-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
    record = {**payload, "id": result_id, "created_at": datetime.now(timezone.utc).isoformat()}
    (settings.RESULT_DIR / f"{result_id}.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    return record


def list_results():
    records = []
    for path in sorted(settings.RESULT_DIR.glob("*.json"), reverse=True):
        try:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return records
