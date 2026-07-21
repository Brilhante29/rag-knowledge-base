# Spec: rag-knowledge-base

## Number

#3

## Claim

Local-first RAG knowledge base with deterministic vector retrieval, FastAPI serving, and reproducible Recall@k benchmark.

## Portfolio Fit

Program: AI Evaluation and Retrieval Systems.

This repository is the retrieval substrate for the program. It supplies a local retrieval service and an explicit evidence contract that sibling evaluation projects can consume later; it does not yet claim a cross-repository platform integration.

## Scope

In:

- JSONL document ingestion and deterministic local embedding.
- Vector search over chunked documents.
- Replaceable embedding and vector-store adapters through domain ports.
- CLI and FastAPI interfaces.
- API filesystem confinement under configured data/result roots.
- Recall@k, latency, and zero-cost benchmark with repeated measurements.
- Docker path with no paid secret.

Out:

- LLM text generation or agent orchestration.
- Claims about production retrieval quality from the small fixture.
- Managed vector databases or embedding APIs.
- Async ingestion, authorization, and multi-tenancy.

## Observable Contract

- Recall per question is `recovered relevant documents / total relevant documents`.
- The primary metric is the macro mean across questions and repetitions.
- Default benchmark: 5 repetitions, 7 questions, 35 timed samples, plus 7 excluded warm-ups.
- API paths are relative to `RAG_DATA_ROOT` or `RAG_RESULT_ROOT`.
- CLI: `python -m rag_knowledge_base evaluate --repetitions 5 --output benchmarks/results/retrieval-baseline.json`.
- API: `/health`, `/ingest`, `/query`, `/evaluate`.
- Docker: `docker run --rm -p 8000:8000 rag-knowledge-base`.

## Dataset

- Source: repository fixture under `data/fixtures/`.
- Corpus size: 8 documents.
- Evaluation size: 7 questions, including one with two relevant documents.
- Determinism: hashing provider and persisted JSON index; no random seed is used.

## Definition Of Done

- [x] Domain ports own embedding and store contracts.
- [x] Application receives adapters by dependency injection.
- [x] API path traversal and absolute paths are rejected.
- [x] Repeated benchmark records clear sample semantics.
- [x] Tests cover retrieval, fractional recall, DI, API security, and benchmark shape.
- [x] Docker build and benchmark run locally without paid credentials.
- [x] README and committed JSON report the same result.
- [ ] Remote CI and publication are verified.
