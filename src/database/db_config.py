from __future__ import annotations

from pathlib import Path


DB_FILENAME = "resume_screening.db"


def get_db_path() -> Path:
    """Return the absolute path to the SQLite DB file in project root."""
    return Path(__file__).resolve().parents[2] / DB_FILENAME
