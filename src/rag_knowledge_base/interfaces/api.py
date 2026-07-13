from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from rag_knowledge_base.application.use_cases import (
    DEFAULT_CORPUS,
    DEFAULT_INDEX,
    DEFAULT_QUESTIONS,
    answer,
    build_index,
    evaluate_retrieval,
)


class IngestRequest(BaseModel):
    corpus_path: str = Field(default=str(DEFAULT_CORPUS))
    index_path: str = Field(default=str(DEFAULT_INDEX))


class QueryRequest(BaseModel):
    question: str
    top_k: int = Field(default=3, ge=1, le=10)
    index_path: str = Field(default=str(DEFAULT_INDEX))


class EvaluateRequest(BaseModel):
    corpus_path: str = Field(default=str(DEFAULT_CORPUS))
    questions_path: str = Field(default=str(DEFAULT_QUESTIONS))
    index_path: str = Field(default=str(DEFAULT_INDEX))
    output_path: str = Field(default="benchmarks/results/retrieval-baseline.json")
    top_k: int = Field(default=3, ge=1, le=10)


def create_app() -> FastAPI:
    app = FastAPI(title="rag-knowledge-base", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/ingest")
    def ingest(request: IngestRequest) -> dict[str, int]:
        return build_index(Path(request.corpus_path), Path(request.index_path))

    @app.post("/query")
    def query(request: QueryRequest) -> dict[str, object]:
        return answer(request.question, index_path=Path(request.index_path), top_k=request.top_k)

    @app.post("/evaluate")
    def evaluate(request: EvaluateRequest) -> dict[str, object]:
        return evaluate_retrieval(
            Path(request.corpus_path),
            Path(request.questions_path),
            Path(request.index_path),
            Path(request.output_path),
            top_k=request.top_k,
        )

    return app


app = create_app()
