# Architecture Record: rag-knowledge-base

## Decision

- Architecture: `clean-architecture`
- Stack profile: `fastapi-backend`
- API style: `rest-http`
- Messaging: `none`
- Database/runtime: `json-vector-store` / `python-cli-and-fastapi-uvicorn`

## Reason

Retrieval use cases, embedding provider, vector store, CLI, and HTTP API need clear dependency direction while remaining simple enough for a focused portfolio proof.

## Dependency Direction

Domain and application define behavior; infrastructure and interfaces depend inward.

## Boundaries

- domain models and ports
- application chunking/retrieval/evaluation use cases
- infrastructure embedding and vector store adapters
- interfaces CLI and FastAPI

## Library Policy

Use FastAPI and Pydantic for the API; use standard-library retrieval core for reproducible local benchmarking.

## Principle Check

- SRP: keep benchmark, API, use cases, and adapters separate.
- OCP: new providers must be adapters, not domain rewrites.
- LSP: replacement providers must preserve observable behavior.
- ISP: ports stay narrow.
- DIP: application depends on behavior, not infrastructure.
- KISS/YAGNI: leave out anything that does not improve the benchmark.
