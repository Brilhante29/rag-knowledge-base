# Decision Context: #3 rag-knowledge-base

This context records reviewable rationale and evidence, not private
chain-of-thought. Volatile state remains in `.portfolio-control/CURRENT_HANDOFF.md`.

## Objective

- Program: `ai-evaluation-retrieval`
- Claim: local-first RAG retrieval with deterministic embeddings and reproducible Recall@k.
- Primary benchmark: `recall_at_3` plus latency and cost.
- Definition of done: local V1 evidence, contract-valid publication V2 evidence, exact-head CI, and truthful release metadata.

## Decisions

| Decision | Selected option | Evidence | Revisit trigger |
|---|---|---|---|
| Architecture | Clean Architecture with ports and adapters | `sdd/architecture-decision.md`, dependency tests | retrieval or deployment boundary changes |
| Stack | Python + FastAPI + Uvicorn + standard-library retrieval core | `project.yaml`, `sdd/technical-decision.md` | benchmark requires model-backed or distributed retrieval |
| API | REST/HTTP plus CLI | command-oriented retrieval contract | flexible graph reads become a real need |
| Messaging | none | synchronous ingestion/query/evaluation | async volume or durable job semantics |
| Cloud | none in baseline | local Docker path; Kumo only if AWS-like behavior is added | cloud behavior becomes part of the proof |
| Publication evidence | V1 execution result and separate V2 provenance result | `benchmark.publication_result_path` | central contract changes |

## Boundary Checks

- [x] Domain/application code does not import FastAPI, Uvicorn, or provider SDKs.
- [x] Ports are implemented by local adapters through the composition root.
- [x] API paths are confined to configured roots.
- [x] Deterministic fixtures keep the default path offline and free.

## Next Action

Run `python tools/benchmark_v2.py`, validate the V2 artifact, then update the
release checklist and push the resulting commit.
