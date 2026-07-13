# Architecture Decision: rag-knowledge-base

## Decision

Use Clean Architecture with explicit domain/application/infrastructure/interfaces boundaries.

## Problem Forces

- Retrieval and evaluation logic must run without HTTP.
- Embedding provider and vector store should be swappable later.
- The first benchmark must be local-first and deterministic.
- The project must show architecture discipline without distributed-system ceremony.

## Chosen Layout

```txt
src/rag_knowledge_base/domain          -> entities and ports
src/rag_knowledge_base/application     -> chunking, indexing, retrieval, evaluation
src/rag_knowledge_base/infrastructure  -> embeddings and vector store adapters
src/rag_knowledge_base/interfaces      -> CLI and FastAPI
```

## Dependency Rule

Domain and application code do not import FastAPI, Uvicorn, cloud SDKs, broker SDKs, or vector database SDKs. Interfaces and infrastructure depend inward.

## Rejected Alternatives

| Alternative | Reason |
|---|---|
| MVC | Would mix API handlers with retrieval/evaluation behavior. |
| Pipeline only | Useful for offline processing, but the repo also serves an API. |
| Microservices | Adds operational cost without improving the RAG proof. |
| Event-driven | Baseline ingestion and query are synchronous. |
