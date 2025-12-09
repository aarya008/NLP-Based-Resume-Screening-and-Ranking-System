from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from utils.logger import get_logger

from src.parser.pdf_reader import extract_text_from_pdf
from src.parser.text_cleaner import clean_text
from src.nlp.jd_processor import JobDescription, load_job_description_from_dir
from src.nlp.skill_extractor import extract_skills, estimate_experience_years
from src.engine.scorer import CandidateDocument, SimilarityScoringEngine
from src.database.db_operations import (
    initialize_schema,
    insert_candidate,
    insert_job_description,
)
from src.automation.ranker import export_ranked_candidates_csv


logger = get_logger(__name__)


@dataclass
class CandidateSummary:
    name: str
    email: Optional[str]
    phone: Optional[str]
    skills: list[str]
    experience_years: int
    score: float
    resume_path: str


NAME_REGEX = re.compile(r"(?i)name\s*[:\-]\s*(.+)")
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(?:(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4})")


def extract_basic_contact_info(text: str) -> tuple[str, Optional[str], Optional[str]]:
    """Heuristic extraction of name, email, and phone from raw resume text."""

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Name: first "Name: X" style line, or top line as fallback
    name = "Unknown"
    for line in lines[:10]:  # only scan top lines for name
        m = NAME_REGEX.search(line)
        if m:
            name = m.group(1).strip()
            break
    else:
        if lines:
            name = lines[0]

    # Email and phone from full text
    email_match = EMAIL_REGEX.search(text)
    phone_match = PHONE_REGEX.search(text)

    email = email_match.group(0) if email_match else None
    phone = phone_match.group(0) if phone_match else None

    return name, email, phone


def process_resumes(resume_dir: str | Path, job_description: JobDescription) -> List[CandidateSummary]:
    """Main in-memory pipeline from resumes to candidate summaries with scores."""

    resume_dir = Path(resume_dir)
    if not resume_dir.is_dir():
        raise FileNotFoundError(f"Resume directory not found: {resume_dir}")

    pdf_files = sorted(resume_dir.glob("*.pdf"))
    if not pdf_files:
        logger.warning("No PDF resumes found in %s", resume_dir)
        return []

    engine = SimilarityScoringEngine()

    candidate_docs: list[CandidateDocument] = []

    for pdf_path in pdf_files:
        logger.info("Processing resume: %s", pdf_path)

        raw_text = extract_text_from_pdf(pdf_path)
        if not raw_text.strip():
            logger.warning("Skipping resume with no text: %s", pdf_path)
            continue

        cleaned = clean_text(raw_text)
        skills = extract_skills(cleaned)
        experience_years = estimate_experience_years(raw_text)

        name, email, phone = extract_basic_contact_info(raw_text)

        candidate_docs.append(
            CandidateDocument(
                name=name,
                email=email,
                phone=phone,
                raw_text=raw_text,
                cleaned_text=cleaned,
                skills=skills,
                experience_years=experience_years,
                resume_path=str(pdf_path),
            )
        )

    if not candidate_docs:
        logger.warning("No valid candidate documents were created.")
        return []

    scores = engine.score_candidates(job_description.text, candidate_docs)

    summaries: list[CandidateSummary] = []
    for cand, score in zip(candidate_docs, scores, strict=True):
        summaries.append(
            CandidateSummary(
                name=cand.name,
                email=cand.email,
                phone=cand.phone,
                skills=cand.skills,
                experience_years=cand.experience_years,
                score=float(score),
                resume_path=cand.resume_path,
            )
        )

    return summaries


def run_pipeline() -> None:
    project_root = Path(__file__).resolve().parents[1]

    # 1. Initialize DB schema
    initialize_schema()

    # 2. Load job description
    jd_dir = project_root / "data" / "jd"
    job_description = load_job_description_from_dir(jd_dir)

    # 3. Insert JD into DB
    jd_id = insert_job_description(
        title=job_description.title,
        required_skills=", ".join(job_description.required_skills),
    )
    job_description.id = jd_id

    # 4. Process resumes and score
    resume_dir = project_root / "data" / "resumes"
    candidate_summaries = process_resumes(resume_dir, job_description)

    if not candidate_summaries:
        logger.warning("No candidates processed; aborting before ranking.")
        return

    # 5. Store candidates in DB
    for cand in candidate_summaries:
        insert_candidate(
            name=cand.name,
            email=cand.email,
            phone=cand.phone,
            skills=", ".join(cand.skills),
            experience=cand.experience_years,
            score=cand.score,
            resume_path=cand.resume_path,
        )

    # 6. Ranking and CSV export
    csv_path = export_ranked_candidates_csv(output_dir=project_root / "output")
    logger.info("Pipeline completed. Ranked candidates CSV: %s", csv_path)


if __name__ == "__main__":
    run_pipeline()
