# Spec: rag-knowledge-base

## Number

#3

## Claim

Local-first RAG knowledge base with deterministic vector retrieval, FastAPI serving, and reproducible Recall@k benchmark.

## Portfolio Fit

Program: AI Evaluation and Retrieval Systems.

This project is the retrieval substrate for the AI evaluation/RAG platform. It creates a reusable local knowledge-base pattern that later projects can evaluate, compare, serve, or optimize.

## Scope

In:

- JSONL document ingestion.
- Deterministic local embedding provider.
- Vector search over chunked documents.
- CLI and FastAPI interface.
- Reproducible retrieval benchmark with Recall@k, latency, and cost/query.
- Docker path with no paid secret.

Out:

- LLM text generation.
- Managed vector database requirement.
- Managed embedding API requirement.
- Async ingestion workers.
- Multi-tenant authorization.

## User-Visible Output

- CLI: `python -m rag_knowledge_base evaluate --output benchmarks/results/retrieval-baseline.json`
- API: `/health`, `/ingest`, `/query`, `/evaluate`
- Docker: `docker run --rm -p 8000:8000 rag-knowledge-base`
- Benchmark JSON: `benchmarks/results/retrieval-baseline.json`

## Dataset

- Source: project-specific fixture in `data/fixtures/`.
- Corpus size: 8 documents.
- Evaluation size: 7 questions.
- License: repository MIT fixture.
- Deterministic seed: not needed; hashing provider is deterministic.

## Definition Of Done

- [x] Docker command exists.
- [x] README starts with project number and benchmark result.
- [x] Benchmark command writes JSON result.
- [x] Tests cover retrieval behavior and evaluation threshold.
- [x] REFERENCES.md explains reuse.
- [x] No secret or paid credential required for default demo.
