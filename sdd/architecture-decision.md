# Architecture Decision: rag-knowledge-base

## Decision

Use Clean Architecture with explicit domain, application, infrastructure, and interface boundaries.

## Problem Forces

- Retrieval and evaluation must run without HTTP.
- Embedding and vector-store implementations must be replaceable.
- The default proof must be deterministic, local-first, and free.
- HTTP callers must not control arbitrary host filesystem paths.
- The project must remain smaller than a distributed RAG platform.

## Chosen Layout

```txt
src/rag_knowledge_base/domain          -> models and provider/store ports
src/rag_knowledge_base/application     -> chunking and injected RetrievalService
src/rag_knowledge_base/infrastructure  -> local adapters and composition root
src/rag_knowledge_base/interfaces      -> CLI, FastAPI, and API path policy
```

## Dependency Rule

Application imports domain ports and models only. Infrastructure implements those ports. CLI and FastAPI are composition boundaries that select adapters. Tests enforce that `application/use_cases.py` does not import infrastructure.

The API path policy belongs to the HTTP boundary because filesystem trust differs by caller: untrusted HTTP inputs are rooted and validated, while the trusted local CLI can use explicit paths.

## Rejected Alternatives

| Alternative | Reason |
|---|---|
| Application constructs local adapters | Violates DIP and prevents substitution tests. |
| Unrestricted API paths | Exposes arbitrary container/host reads and writes. |
| MVC | Would mix HTTP path policy with retrieval/evaluation policy. |
| Mandatory Qdrant/model download | Adds services and network variance before the baseline needs them. |
| Microservices/event-driven | Adds operational cost without improving Recall@k evidence. |
