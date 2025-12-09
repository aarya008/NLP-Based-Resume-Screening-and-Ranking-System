from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from utils.logger import get_logger

from .db_config import get_db_path


logger = get_logger(__name__)


def get_connection() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn


def initialize_schema(schema_path: Path | str | None = None) -> None:
    if schema_path is None:
        schema_path = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"
    schema_path = Path(schema_path)

    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    sql = schema_path.read_text(encoding="utf-8")
    conn = get_connection()
    try:
        conn.executescript(sql)
        conn.commit()
        logger.info("Database schema initialized at %s", get_db_path())
    finally:
        conn.close()


def insert_job_description(title: str, required_skills: str) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO job_description (title, required_skills) VALUES (?, ?)",
            (title, required_skills),
        )
        conn.commit()
        jd_id = int(cur.lastrowid)
        logger.info("Inserted job description id=%s", jd_id)
        return jd_id
    finally:
        conn.close()


def insert_candidate(
    name: str,
    email: Optional[str],
    phone: Optional[str],
    skills: str,
    experience: int,
    score: float,
    resume_path: str,
) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO candidates (name, email, phone, skills, experience, score, resume_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, email, phone, skills, experience, score, resume_path),
        )
        conn.commit()
        candidate_id = int(cur.lastrowid)
        logger.info("Inserted candidate id=%s name=%s", candidate_id, name)
        return candidate_id
    finally:
        conn.close()


def fetch_all_candidates() -> List[Tuple]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, email, phone, skills, experience, score, resume_path FROM candidates"
        )
        rows = cur.fetchall()
        return rows
    finally:
        conn.close()
