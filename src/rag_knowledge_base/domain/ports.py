from __future__ import annotations

from typing import Protocol

from rag_knowledge_base.domain.models import Chunk, SearchResult


class EmbeddingProvider(Protocol):
    @property
    def dimension(self) -> int: ...

    def embed(self, text: str) -> list[float]: ...


class VectorStore(Protocol):
    def upsert(self, chunk: Chunk, vector: list[float]) -> None: ...

    def search(self, query_vector: list[float], top_k: int) -> list[SearchResult]: ...

    def save(self, path: str) -> None: ...

    @classmethod
    def load(cls, path: str) -> "VectorStore": ...
