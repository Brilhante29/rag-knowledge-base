# #3 rag-knowledge-base: Recall@3 = 1.00

Local-first RAG knowledge base with deterministic vector retrieval, FastAPI serving, and reproducible Recall@k benchmark.

This repository belongs to the AI Evaluation and Retrieval Systems program. Its job is narrow: prove the measurable claim through the selected component pack before adding unrelated infrastructure or features.

The benchmark is the proof. Recall@3 = 1.00. Average latency: 18.9 ms. P95 latency: 30.76 ms. The result is stored in `benchmarks/results/retrieval-baseline.json` and can be reproduced from the Docker/local path.

The important architecture decision is clean-architecture. Retrieval use cases, embedding provider, vector store, CLI, and HTTP API need clear dependency direction while remaining simple enough for a focused portfolio proof.

The default path stays local-first. The project uses fastapi-backend, exposes rest-http, uses messaging mode `none`, and stores data with `json-vector-store`. The dependency rule is explicit: Domain and application define behavior; infrastructure and interfaces depend inward.

The rejected work matters as much as the implemented work. Anything that does not improve the benchmark stays out of the first version.

Post angle: start with the number, show the architecture boundary, then explain which future adapter can be added without changing the core use cases.
