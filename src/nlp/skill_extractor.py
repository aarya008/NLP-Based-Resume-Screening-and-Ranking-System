from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Sequence

from utils.logger import get_logger


logger = get_logger(__name__)


# A small default skills list. You can extend this or load from data/samples.
DEFAULT_SKILLS: set[str] = {
    "python",
    "java",
    "c++",
    "sql",
    "javascript",
    "html",
    "css",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "machine learning",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "django",
    "flask",
    "react",
}


def load_additional_skills_from_file(path: Path | str) -> set[str]:
    """Load one skill per line from a text file, if it exists."""
    skills_file = Path(path)
    if not skills_file.is_file():
        return set()

    skills: set[str] = set()
    for line in skills_file.read_text(encoding="utf-8").splitlines():
        skill = line.strip().lower()
        if skill:
            skills.add(skill)
    return skills


def build_skill_vocabulary(*sources: Iterable[str]) -> set[str]:
    """Merge default skills with skills from provided sources (e.g. JD)."""
    vocab = set(DEFAULT_SKILLS)

    for source in sources:
        for text in source:
            text_lower = text.lower()
            # crude heuristic: treat up to 3-word phrases as potential skills
            tokens = re.findall(r"[a-zA-Z0-9+#.]+", text_lower)
            for token in tokens:
                if len(token) > 2:
                    vocab.add(token)

    return vocab


def extract_skills(text: str, skills_vocab: Sequence[str] | set[str] | None = None) -> list[str]:
    """Extract skills present in text by exact or phrase matching.

    - If `skills_vocab` is None, `DEFAULT_SKILLS` is used.
    - Matching is case-insensitive.
    """

    if skills_vocab is None:
        skills_vocab = DEFAULT_SKILLS

    normalized_text = " " + text.lower() + " "

    found: set[str] = set()
    for skill in skills_vocab:
        s = skill.lower().strip()
        if not s:
            continue
        # word-boundary style match (handles single words and simple phrases)
        pattern = r"(?<![a-z0-9+.#])" + re.escape(s) + r"(?![a-z0-9+.#])"
        if re.search(pattern, normalized_text):
            found.add(skill)

    return sorted(found)


def estimate_experience_years(text: str) -> int:
    """Very rough heuristic to extract years of experience from resume text.

    Looks for patterns like "5 years", "3+ years" and returns the max found.
    """

    matches = re.findall(r"(\d+)(?:\+)?\s+years", text.lower())
    years = [int(m) for m in matches]
    return max(years) if years else 0
