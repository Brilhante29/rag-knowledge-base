from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from rag_knowledge_base.domain.models import Chunk, SearchResult


class JsonVectorStore:
    def __init__(self, dimension: int, records: list[tuple[Chunk, list[float]]] | None = None) -> None:
        self.dimension = dimension
        self._records = records or []

    @property
    def size(self) -> int:
        return len(self._records)

    def upsert(self, chunk: Chunk, vector: list[float]) -> None:
        if len(vector) != self.dimension:
            raise ValueError(f"Expected vector dimension {self.dimension}, got {len(vector)}")
        self._records = [(item, values) for item, values in self._records if item.id != chunk.id]
        self._records.append((chunk, vector))

    def search(self, query_vector: list[float], top_k: int) -> list[SearchResult]:
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        scored = [SearchResult(chunk=chunk, score=_dot(query_vector, vector)) for chunk, vector in self._records]
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def save(self, path: str) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "dimension": self.dimension,
            "records": [
                {"chunk": asdict(chunk), "vector": vector}
                for chunk, vector in self._records
            ],
        }
        target.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str) -> "JsonVectorStore":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        records = []
        for record in payload["records"]:
            chunk_payload = record["chunk"]
            records.append((Chunk(**chunk_payload), [float(value) for value in record["vector"]]))
        return cls(dimension=int(payload["dimension"]), records=records)


def _dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
