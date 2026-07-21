from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from rag_knowledge_base.application.chunking import chunk_documents
from rag_knowledge_base.domain.models import Document, SearchResult
from rag_knowledge_base.domain.ports import EmbeddingProvider, VectorStore, VectorStoreFactory

DEFAULT_CORPUS = Path("data/fixtures/corpus.jsonl")
DEFAULT_QUESTIONS = Path("data/fixtures/questions.jsonl")
DEFAULT_INDEX = Path("data/runtime/index.json")
DEFAULT_RESULT = Path("benchmarks/results/retrieval-baseline.json")
DEFAULT_REPETITIONS = 5


@dataclass(frozen=True)
class RetrievalService:
    embedding_provider: EmbeddingProvider
    vector_stores: VectorStoreFactory

    def load_documents(self, path: Path = DEFAULT_CORPUS) -> list[Document]:
        return [Document(**item) for item in _read_jsonl(path)]

    def build_index(
        self,
        corpus_path: Path = DEFAULT_CORPUS,
        index_path: Path = DEFAULT_INDEX,
    ) -> dict[str, int]:
        documents = self.load_documents(corpus_path)
        chunks = chunk_documents(documents)
        store = self.vector_stores.create(self.embedding_provider.dimension)
        for chunk in chunks:
            store.upsert(
                chunk,
                self.embedding_provider.embed(f"{chunk.title}\n{chunk.text}"),
            )
        store.save(index_path)
        return {
            "documents": len(documents),
            "chunks": len(chunks),
            "dimension": self.embedding_provider.dimension,
        }

    def retrieve(
        self,
        question: str,
        *,
        index_path: Path = DEFAULT_INDEX,
        top_k: int = 3,
    ) -> list[SearchResult]:
        store = self.vector_stores.load(index_path)
        return self._retrieve_from_store(question, store=store, top_k=top_k)

    def answer(
        self,
        question: str,
        *,
        index_path: Path = DEFAULT_INDEX,
        top_k: int = 3,
    ) -> dict[str, Any]:
        results = self.retrieve(question, index_path=index_path, top_k=top_k)
        contexts = [
            {
                "document_id": result.chunk.document_id,
                "chunk_id": result.chunk.id,
                "title": result.chunk.title,
                "score": round(result.score, 6),
                "text": result.chunk.text,
            }
            for result in results
        ]
        return {
            "question": question,
            "answer": "\n\n".join(item["text"] for item in contexts),
            "contexts": contexts,
        }

    def evaluate_retrieval(
        self,
        corpus_path: Path = DEFAULT_CORPUS,
        questions_path: Path = DEFAULT_QUESTIONS,
        index_path: Path = DEFAULT_INDEX,
        output_path: Path = DEFAULT_RESULT,
        *,
        top_k: int = 3,
        repetitions: int = DEFAULT_REPETITIONS,
    ) -> dict[str, Any]:
        if repetitions <= 0:
            raise ValueError("repetitions must be positive")

        index_stats = self.build_index(corpus_path, index_path)
        store = self.vector_stores.load(index_path)
        questions = _read_jsonl(questions_path)
        if not questions:
            raise ValueError("questions fixture must not be empty")

        # Warm-up is intentionally excluded from measured samples.
        for question in questions:
            self._retrieve_from_store(question["question"], store=store, top_k=top_k)

        repetition_recalls: list[float] = []
        latency_samples_ms: list[float] = []
        measurements: list[dict[str, Any]] = []

        for repetition in range(1, repetitions + 1):
            question_recalls: list[float] = []
            for question in questions:
                started = time.perf_counter()
                results = self._retrieve_from_store(
                    question["question"],
                    store=store,
                    top_k=top_k,
                )
                elapsed_ms = (time.perf_counter() - started) * 1000.0
                expected = set(question["relevant_document_ids"])
                found = {result.chunk.document_id for result in results}
                recall = recall_at_k(expected, found)
                recovered = len(expected.intersection(found))

                question_recalls.append(recall)
                latency_samples_ms.append(elapsed_ms)
                measurements.append(
                    {
                        "repetition": repetition,
                        "question_id": question["id"],
                        "relevant_documents": len(expected),
                        "recovered_relevant_documents": recovered,
                        "recall_at_k": recall,
                        "latency_ms": elapsed_ms,
                    }
                )
            repetition_recalls.append(statistics.fmean(question_recalls))

        recall = statistics.fmean(repetition_recalls)
        result = {
            "project": "rag-knowledge-base",
            "metric": f"recall_at_{top_k}",
            "value": recall,
            "unit": "ratio",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "command": (
                "python -m rag_knowledge_base evaluate "
                f"--corpus {corpus_path.as_posix()} --questions {questions_path.as_posix()} "
                f"--index {index_path.as_posix()} --top-k {top_k} "
                f"--repetitions {repetitions} --output {output_path.as_posix()}"
            ),
            "repeat": repetitions,
            "samples": repetition_recalls,
            "sample_definition": (
                "Each sample is the macro mean of per-question Recall@k for one full "
                "evaluation repetition; warm-up queries are excluded."
            ),
            "latency_samples_ms": latency_samples_ms,
            "measurements": measurements,
            "summary": {
                "recall_at_k": recall,
                "avg_latency_ms": statistics.fmean(latency_samples_ms),
                "p95_latency_ms": _percentile(latency_samples_ms, 95),
                "cost_per_query_usd": 0.0,
                "queries": float(len(questions)),
                "repetitions": float(repetitions),
                "timed_query_samples": float(len(latency_samples_ms)),
                "warmup_queries": float(len(questions)),
                "top_k": float(top_k),
                "indexed_documents": float(index_stats["documents"]),
                "indexed_chunks": float(index_stats["chunks"]),
                "embedding_dimension": float(index_stats["dimension"]),
            },
            "environment": {
                "python": sys.version.split()[0],
                "platform": platform.platform(),
                "embedding_provider": type(self.embedding_provider).__name__,
                "vector_store_factory": type(self.vector_stores).__name__,
            },
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result

    def _retrieve_from_store(
        self,
        question: str,
        *,
        store: VectorStore,
        top_k: int,
    ) -> list[SearchResult]:
        if store.dimension != self.embedding_provider.dimension:
            raise ValueError(
                "Embedding dimension does not match the persisted vector store: "
                f"{self.embedding_provider.dimension} != {store.dimension}"
            )
        return store.search(self.embedding_provider.embed(question), top_k=top_k)


def recall_at_k(expected_document_ids: Iterable[str], found_document_ids: Iterable[str]) -> float:
    expected = set(expected_document_ids)
    if not expected:
        raise ValueError("Recall@k requires at least one relevant document")
    return len(expected.intersection(found_document_ids)) / len(expected)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, round((percentile / 100) * (len(ordered) - 1))))
    return ordered[index]
