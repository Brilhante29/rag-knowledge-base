from __future__ import annotations

from pathlib import Path
from typing import Protocol

from rag_knowledge_base.domain.models import Chunk, SearchResult


class EmbeddingProvider(Protocol):
    @property
    def dimension(self) -> int: ...

    def embed(self, text: str) -> list[float]: ...


class VectorStore(Protocol):
    @property
    def dimension(self) -> int: ...

    def upsert(self, chunk: Chunk, vector: list[float]) -> None: ...

    def search(self, query_vector: list[float], top_k: int) -> list[SearchResult]: ...

    def save(self, path: Path) -> None: ...


class VectorStoreFactory(Protocol):
    def create(self, dimension: int) -> VectorStore: ...

    def load(self, path: Path) -> VectorStore: ...
