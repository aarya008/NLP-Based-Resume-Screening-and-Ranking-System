from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class TfidfVectorizerWrapper:
    """Simple wrapper to vectorize documents and compute cosine similarity."""

    vectorizer: TfidfVectorizer

    @classmethod
    def create_default(cls) -> "TfidfVectorizerWrapper":
        vec = TfidfVectorizer(
            max_features=5000,  
            ngram_range=(1, 2),
        )
        return cls(vectorizer=vec)

    def fit_transform(self, documents: Iterable[str]) -> np.ndarray:
        return self.vectorizer.fit_transform(list(documents)).toarray()

    def transform(self, documents: Iterable[str]) -> np.ndarray:
        return self.vectorizer.transform(list(documents)).toarray()


def cosine_similarity_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Compute cosine similarity between two matrices of vectors."""

    if a.size == 0 or b.size == 0:
        return np.zeros((a.shape[0], b.shape[0]))

    # normalize rows
    a_norm = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-8)
    b_norm = b / (np.linalg.norm(b, axis=1, keepdims=True) + 1e-8)
    return np.dot(a_norm, b_norm.T)


def pairwise_cosine_similarity(vectors: np.ndarray, single: np.ndarray) -> np.ndarray:
    """Cosine similarity between each row in `vectors` and a single vector."""

    if vectors.ndim != 2 or single.ndim != 1:
        raise ValueError("vectors must be 2D and single must be 1D")

    num = vectors @ single
    denom = (np.linalg.norm(vectors, axis=1) * (np.linalg.norm(single) + 1e-8)) + 1e-8
    return num / denom
