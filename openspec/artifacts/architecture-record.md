# Architecture Record: rag-knowledge-base

## Decision

- Architecture: `clean-architecture`
- Stack profile: `fastapi-backend`
- API style: `rest-http`
- Messaging: `none`
- Storage/runtime: `json-vector-store` / `python-cli-and-fastapi-uvicorn`

## Dependency Direction

`RetrievalService` depends on domain ports. `HashingEmbeddingProvider` and `JsonVectorStoreFactory` implement those contracts and are selected by `infrastructure/composition.py`. Interfaces call the composed service; application code never constructs adapters.

## Security Boundary

FastAPI treats path input as untrusted and resolves safe relative paths below `RAG_DATA_ROOT` or `RAG_RESULT_ROOT`. CLI paths remain explicit because the local operator is trusted.

## Principle Check

- SRP: retrieval, path policy, adapters, composition, and transport are separate.
- OCP/DIP: providers are replaceable through injected ports.
- LSP: dimension compatibility is checked before search.
- ISP: ports expose only embedding and vector-store lifecycle behavior.
- KISS/YAGNI: no managed services, broker, generation, or auth in this proof.
