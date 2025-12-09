import re
from typing import Iterable


# A compact English stopword set to avoid heavy NLTK setup.
BASIC_STOPWORDS: set[str] = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "in",
    "on",
    "at",
    "for",
    "to",
    "of",
    "with",
    "is",
    "are",
    "was",
    "were",
    "be",
    "this",
    "that",
    "these",
    "those",
    "as",
    "by",
    "from",
    "it",
    "its",
    "you",
    "your",
    "we",
    "our",
}


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_text(text: str, *, lowercase: bool = True, remove_stopwords: bool = True) -> str:
    """Basic text normalization: lowercasing, punctuation and stopword removal."""

    if lowercase:
        text = text.lower()

    # Replace non-alphanumeric characters with spaces.
    text = re.sub(r"[^a-z0-9+.]", " ", text)

    tokens = text.split()
    if remove_stopwords:
        tokens = [t for t in tokens if t not in BASIC_STOPWORDS]

    return normalize_whitespace(" ".join(tokens))


def tokenize(text: str) -> list[str]:
    """Simple whitespace tokenization after cleaning punctuation."""
    text = re.sub(r"[^a-zA-Z0-9+.]", " ", text)
    return [t for t in text.split() if t]


def join_tokens(tokens: Iterable[str]) -> str:
    return " ".join(tokens)
