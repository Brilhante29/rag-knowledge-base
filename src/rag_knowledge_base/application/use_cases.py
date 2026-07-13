from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rag_knowledge_base.application.chunking import chunk_documents
from rag_knowledge_base.domain.models import Document, SearchResult
from rag_knowledge_base.infrastructure.embeddings.hashing import HashingEmbeddingProvider
from rag_knowledge_base.infrastructure.stores.json_vector_store import JsonVectorStore

DEFAULT_CORPUS = Path("data/fixtures/corpus.jsonl")
DEFAULT_QUESTIONS = Path("data/fixtures/questions.jsonl")
DEFAULT_INDEX = Path("data/runtime/index.json")
DEFAULT_RESULT = Path("benchmarks/results/retrieval-baseline.json")


def load_documents(path: Path = DEFAULT_CORPUS) -> list[Document]:
    return [Document(**item) for item in _read_jsonl(path)]


def build_index(
    corpus_path: Path = DEFAULT_CORPUS,
    index_path: Path = DEFAULT_INDEX,
    *,
    dimension: int = 384,
) -> dict[str, int]:
    embedder = HashingEmbeddingProvider(dimension=dimension)
    documents = load_documents(corpus_path)
    chunks = chunk_documents(documents)
    store = JsonVectorStore(dimension=embedder.dimension)
    for chunk in chunks:
        store.upsert(chunk, embedder.embed(f"{chunk.title}\n{chunk.text}"))
    store.save(str(index_path))
    return {"documents": len(documents), "chunks": len(chunks), "dimension": embedder.dimension}


def retrieve(
    question: str,
    *,
    index_path: Path = DEFAULT_INDEX,
    top_k: int = 3,
    dimension: int = 384,
) -> list[SearchResult]:
    if not index_path.exists():
        build_index(DEFAULT_CORPUS, index_path, dimension=dimension)
    embedder = HashingEmbeddingProvider(dimension=dimension)
    store = JsonVectorStore.load(str(index_path))
    return store.search(embedder.embed(question), top_k=top_k)


def answer(question: str, *, index_path: Path = DEFAULT_INDEX, top_k: int = 3) -> dict[str, Any]:
    results = retrieve(question, index_path=index_path, top_k=top_k)
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
    corpus_path: Path = DEFAULT_CORPUS,
    questions_path: Path = DEFAULT_QUESTIONS,
    index_path: Path = DEFAULT_INDEX,
    output_path: Path = DEFAULT_RESULT,
    *,
    top_k: int = 3,
    dimension: int = 384,
) -> dict[str, Any]:
    index_stats = build_index(corpus_path, index_path, dimension=dimension)
    questions = _read_jsonl(questions_path)
    hits: list[float] = []
    latencies: list[float] = []

    for question in questions:
        started = time.perf_counter()
        results = retrieve(question["question"], index_path=index_path, top_k=top_k, dimension=dimension)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        expected = set(question["relevant_document_ids"])
        found = {result.chunk.document_id for result in results}
        hits.append(1.0 if expected.intersection(found) else 0.0)
        latencies.append(elapsed_ms)

    recall = sum(hits) / len(hits) if hits else 0.0
    avg_latency = statistics.fmean(latencies) if latencies else 0.0
    result = {
        "project": "rag-knowledge-base",
        "metric": f"recall_at_{top_k}",
        "value": recall,
        "unit": "ratio",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": (
            "python -m rag_knowledge_base evaluate "
            f"--corpus {corpus_path.as_posix()} --questions {questions_path.as_posix()} "
            f"--index {index_path.as_posix()} --top-k {top_k} --output {output_path.as_posix()}"
        ),
        "repeat": len(questions),
        "samples": hits,
        "summary": {
            "recall_at_k": recall,
            "avg_latency_ms": avg_latency,
            "p95_latency_ms": _percentile(latencies, 95),
            "cost_per_query_usd": 0.0,
            "queries": float(len(questions)),
            "top_k": float(top_k),
            "indexed_documents": float(index_stats["documents"]),
            "indexed_chunks": float(index_stats["chunks"]),
            "embedding_dimension": float(index_stats["dimension"]),
        },
        "environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "embedding_provider": "local-hashing",
            "vector_store": "json-vector-store",
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


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
