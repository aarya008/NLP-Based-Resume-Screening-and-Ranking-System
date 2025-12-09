from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np

from utils.logger import get_logger

from src.nlp.vectorizer import TfidfVectorizerWrapper, pairwise_cosine_similarity


logger = get_logger(__name__)


@dataclass
class CandidateDocument:
    name: str
    email: str | None
    phone: str | None
    raw_text: str
    cleaned_text: str
    skills: list[str]
    experience_years: int
    resume_path: str


class SimilarityScoringEngine:
    def __init__(self) -> None:
        self.vectorizer_wrapper = TfidfVectorizerWrapper.create_default()

    def score_candidates(self, jd_text: str, candidate_docs: List[CandidateDocument]) -> list[float]:
        """Return similarity scores for each candidate vs the JD text."""

        corpus = [jd_text] + [c.cleaned_text for c in candidate_docs]
        matrix = self.vectorizer_wrapper.fit_transform(corpus)

        jd_vec = matrix[0]
        cand_vecs = matrix[1:]

        scores = pairwise_cosine_similarity(cand_vecs, jd_vec)

        logger.info("Computed similarity scores for %d candidates", len(candidate_docs))

        return scores.tolist()
