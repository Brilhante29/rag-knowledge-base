from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag_knowledge_base.application.use_cases import DEFAULT_REPETITIONS, RetrievalService
from rag_knowledge_base.infrastructure.composition import create_local_retrieval_service


class IngestRequest(BaseModel):
    corpus_path: str = Field(default="fixtures/corpus.jsonl")
    index_path: str = Field(default="runtime/index.json")


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)
    index_path: str = Field(default="runtime/index.json")


class EvaluateRequest(BaseModel):
    corpus_path: str = Field(default="fixtures/corpus.jsonl")
    questions_path: str = Field(default="fixtures/questions.jsonl")
    index_path: str = Field(default="runtime/index.json")
    output_path: str = Field(default="retrieval-baseline.json")
    top_k: int = Field(default=3, ge=1, le=10)
    repetitions: int = Field(default=DEFAULT_REPETITIONS, ge=1, le=100)


class UnsafePathError(ValueError):
    pass


@dataclass(frozen=True)
class ApiPathPolicy:
    data_root: Path
    result_root: Path

    def __post_init__(self) -> None:
        object.__setattr__(self, "data_root", self.data_root.resolve())
        object.__setattr__(self, "result_root", self.result_root.resolve())

    @classmethod
    def from_environment(cls) -> "ApiPathPolicy":
        return cls(
            data_root=Path(os.environ.get("RAG_DATA_ROOT", "data")),
            result_root=Path(os.environ.get("RAG_RESULT_ROOT", "benchmarks/results")),
        )

    def data_path(self, relative_path: str) -> Path:
        return _resolve_below(self.data_root, relative_path)

    def result_path(self, relative_path: str) -> Path:
        return _resolve_below(self.result_root, relative_path)


def create_app(
    *,
    service: RetrievalService | None = None,
    path_policy: ApiPathPolicy | None = None,
) -> FastAPI:
    retrieval = service or create_local_retrieval_service()
    paths = path_policy or ApiPathPolicy.from_environment()
    app = FastAPI(title="rag-knowledge-base", version="0.2.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/ingest")
    def ingest(request: IngestRequest) -> dict[str, int]:
        try:
            return retrieval.build_index(
                paths.data_path(request.corpus_path),
                paths.data_path(request.index_path),
            )
        except UnsafePathError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail="Corpus not found") from error

    @app.post("/query")
    def query(request: QueryRequest) -> dict[str, object]:
        try:
            return retrieval.answer(
                request.question,
                index_path=paths.data_path(request.index_path),
                top_k=request.top_k,
            )
        except UnsafePathError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail="Index not found; ingest the corpus first") from error

    @app.post("/evaluate")
    def evaluate(request: EvaluateRequest) -> dict[str, object]:
        try:
            return retrieval.evaluate_retrieval(
                paths.data_path(request.corpus_path),
                paths.data_path(request.questions_path),
                paths.data_path(request.index_path),
                paths.result_path(request.output_path),
                top_k=request.top_k,
                repetitions=request.repetitions,
            )
        except UnsafePathError as error:
            raise HTTPException(status_code=400, detail=str(error)) from error
        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail="Corpus or questions fixture not found") from error

    return app


def _resolve_below(root: Path, relative_path: str) -> Path:
    raw = relative_path.strip().replace("\\", "/")
    if not raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        raise UnsafePathError("Path must be relative to its configured root")

    relative = PurePosixPath(raw)
    if any(part in {"", ".", ".."} for part in relative.parts):
        raise UnsafePathError("Path traversal is not allowed")

    candidate = (root / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise UnsafePathError("Path escapes its configured root") from error
    if candidate == root:
        raise UnsafePathError("Path must identify a file below its configured root")
    return candidate


app = create_app()
