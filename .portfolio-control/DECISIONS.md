# Decision Register: #3 rag-knowledge-base

| Decision | Selected option | Evidence or reason | Revisit trigger |
|---|---|---|---|
| Architecture | Clean Architecture with injected ports | retrieval policy must run without HTTP/storage implementation | adapters require incompatible semantics |
| API style | REST/HTTP plus CLI | synchronous ingest/query/evaluate commands | clients require streaming or typed RPC |
| Messaging | none | no async delivery, replay, routing, or fan-out requirement | measured async workload appears |
| Storage | local JSON vector store | transparent, deterministic fixture-scale persistence | dataset size makes linear search a bottleneck |
| Local-first/cloud | Docker, no cloud service | benchmark requires no paid credentials | cloud behavior becomes part of the proof |
| Libraries | FastAPI, Pydantic, Uvicorn; stdlib retrieval core | typed API with deterministic offline benchmark | profiling or maintenance evidence changes fit |
| HTTP filesystem | rooted relative paths | API caller is untrusted; CLI operator is trusted | storage moves behind a non-filesystem port |
| Benchmark | 5 repeated macro Recall@3 runs | separates questions, repetitions, warm-up, and latency samples | harder dataset changes evaluation design |

## Design Principles

- **SRP:** retrieval policy, adapters, composition, path policy, and interfaces have separate reasons to change.
- **OCP/DIP:** application receives provider/store ports; infrastructure selects implementations.
- **LSP:** vector dimensions and search/persistence semantics must remain compatible.
- **ISP:** ports expose only embedding and vector-store lifecycle behavior.
- **DRY:** sample semantics are recorded once in code/JSON and mirrored in documentation.
- **KISS/YAGNI:** no broker, cloud, external vector DB, model download, auth, or generation layer yet.
- **Law of Demeter:** interfaces call the service; the service calls direct ports.
