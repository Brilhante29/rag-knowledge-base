# Technical Decision: rag-knowledge-base

## Stack

- Python package under `src/`.
- FastAPI/Pydantic for typed HTTP and OpenAPI.
- Uvicorn for ASGI serving.
- Deterministic hashing embeddings and JSON vector persistence.
- Docker for the no-secret runnable path.

## Ports And Composition

`RetrievalService` depends on `EmbeddingProvider` and `VectorStoreFactory`. `JsonVectorStoreFactory` and `HashingEmbeddingProvider` are selected only in `infrastructure/composition.py`. This preserves DIP and lets tests inject collaborators without framework or storage setup.

The vector-store port exposes dimension, upsert, search, and save. The factory owns create/load lifecycle because loading is adapter behavior, not application policy.

## API Security

`ApiPathPolicy` resolves normalized relative paths below configured roots. It rejects absolute Windows/POSIX paths, dot segments, traversal, and resolved paths outside the root. Data/index operations use `RAG_DATA_ROOT`; benchmark output uses `RAG_RESULT_ROOT`.

## Benchmark Method

- Warm the store with each of seven questions once; exclude warm-up from timing.
- Execute five complete repetitions.
- Compute per-question Recall@3 as recovered relevant divided by total relevant.
- Macro-average question recall within each repetition and across repetitions.
- Record five recall samples, 35 latency samples, and per-question measurements.
- Load the index once before timed retrieval so latency measures embedding plus search, not file loading.

## API Style And Messaging

REST plus CLI remains sufficient for synchronous ingest/query/evaluate commands. GraphQL, gRPC, brokers, and cloud services do not improve the current claim.

## Principles

- SRP: path policy, retrieval policy, composition, adapters, and transport are separate.
- OCP/DIP: new providers enter through ports and composition.
- LSP: stores preserve dimension, persistence, and search semantics.
- ISP: ports expose only retrieval lifecycle behavior.
- KISS/YAGNI: no auth, broker, external database, model download, or generation layer yet.
