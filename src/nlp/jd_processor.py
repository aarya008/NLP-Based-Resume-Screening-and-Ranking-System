from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.logger import get_logger

from .skill_extractor import extract_skills


logger = get_logger(__name__)


@dataclass
class JobDescription:
    id: Optional[int]
    title: str
    text: str
    required_skills: list[str]


def load_job_description_from_dir(jd_dir: str | Path) -> JobDescription:
    """Load the first .txt file from `jd_dir` as the job description."""
    path = Path(jd_dir)
    if not path.is_dir():
        raise FileNotFoundError(f"Job description directory not found: {path}")

    candidates = sorted(path.glob("*.txt"))
    if not candidates:
        raise FileNotFoundError(f"No .txt job description files found in {path}")

    jd_path = candidates[0]
    text = jd_path.read_text(encoding="utf-8")

    # naive title: first non-empty line
    title = next((line.strip() for line in text.splitlines() if line.strip()), "Job Description")

    required_skills = extract_skills(text)

    logger.info("Loaded job description '%s' from %s", title, jd_path)

    return JobDescription(id=None, title=title, text=text, required_skills=required_skills)
