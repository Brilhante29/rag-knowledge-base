# Technical Decision: rag-knowledge-base

## Stack

- Python package under `src/`.
- FastAPI for typed HTTP API and OpenAPI docs.
- Uvicorn for ASGI serving.
- Standard-library hashing embeddings for default local retrieval.
- JSON vector store for transparent deterministic persistence.
- Docker for the runnable path.

## API Style

REST/HTTP plus CLI.

REST is enough because the workload is command-oriented: ingest, query, evaluate. GraphQL is rejected because flexible nested reads are not the problem and would add resolver/security complexity without improving Recall@k.

## Messaging

No broker.

The baseline has synchronous ingestion and evaluation. RabbitMQ, Kafka, Redis Streams, and NATS are rejected until async jobs, replay, routing, DLQ, or streaming are part of the benchmark.

## Cloud

No cloud in the default path.

Kumo remains the preferred local-first layer if AWS-like services are added later. Real cloud providers must be adapters behind ports and cannot enter domain/use-case code.

## Embeddings And Vector Store

The default provider is `HashingEmbeddingProvider`, a deterministic local vectorizer. This keeps the benchmark reproducible, offline, and free.

Qdrant and sentence-transformers are useful next adapters, but they are not mandatory for the first proof because they introduce a service or model download before the baseline needs it.

## SOLID And Coupling

- SRP: chunking, embedding, vector storage, evaluation, CLI, and API have separate modules.
- OCP: new embedding/vector adapters can be added without changing use-case contracts.
- LSP: future providers must return vectors/search results with the same semantics.
- ISP: ports are narrow: embed, upsert, search, save/load.
- DIP: application depends on behavior, not framework or external services.

## KISS/YAGNI

No auth, broker, external vector DB, model download, or LLM generation until a benchmark requires it.
