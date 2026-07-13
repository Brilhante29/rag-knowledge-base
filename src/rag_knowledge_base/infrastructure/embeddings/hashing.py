from __future__ import annotations

import hashlib
import math
import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9]+")


class HashingEmbeddingProvider:
    """Deterministic local vectorizer used as the no-secret default embedding provider."""

    def __init__(self, dimension: int = 384) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        self._dimension = dimension

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self._dimension
        tokens = _tokens(text)
        weighted_terms = Counter(tokens)
        weighted_terms.update({f"{left}_{right}": 2 for left, right in zip(tokens, tokens[1:])})

        for term, weight in weighted_terms.items():
            digest = hashlib.sha256(term.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], byteorder="big") % self._dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign * float(weight)

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0.0:
            return vector
        return [value / norm for value in vector]


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())
