from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from ..core.config import settings
print(">>> SETTINGS IMPORTED FROM:", settings.__class__.__module__)
print(">>> SETTINGS FIELDS:", list(settings.model_fields.keys()))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure_export_dir() -> None:
    os.makedirs(settings.EXPORT_DIR, exist_ok=True)


def project_json_path(project_id: int) -> Path:
    """One JSON file per project."""
    ensure_export_dir()
    return Path(settings.EXPORT_DIR) / f"project_{project_id}.json"


@dataclass
class JsonResultRecord:
    project_id: int
    image_id: int
    run_id: int
    filename: str
    sha256: str
    storage_path: str
    prompt: str
    model: str
    params: dict[str, Any]
    output_text: str
    tokens_in: int | None
    tokens_out: int | None
    created_at: str


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"project_id": None, "updated_at": None, "records": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def append_record(project_id: int, record: JsonResultRecord) -> Path:
    """
    Append a single result record into the project's JSON file.

    Ordering: records are kept sorted by filename, then run_id.
    """
    path = project_json_path(project_id)
    data = _read_json(path)

    data["project_id"] = project_id
    data["updated_at"] = _utc_now_iso()
    data.setdefault("records", [])
    data["records"].append(asdict(record))

    # "geordnet"
    data["records"] = sorted(
        data["records"],
        key=lambda r: ((r.get("filename") or ""), int(r.get("run_id") or 0)),
    )

    _atomic_write_json(path, data)
    return path