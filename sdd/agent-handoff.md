# Agent Handoff

Project: `3 - rag-knowledge-base`
Status: `publication-v2`

## Current State

- Recall@3: 1.00 on the 8-document/7-question fixture.
- Method: 5 repetitions, 35 timed queries, 7 excluded warm-ups.
- Docker result: average 1.65 ms, p95 1.97 ms, zero paid cost.
- Application depends on embedding/vector-store ports through `RetrievalService`.
- HTTP filesystem access is confined by `ApiPathPolicy`.
- Local test suite: 6 tests covering behavior, DI, metric semantics, and path security.
- Exact-head GitHub Actions run `30329376065` passed for `e8d00dff29be52340f5c5913b60aa15aa129222f`.

## Continue From Here

1. Run `python tools/benchmark_v2.py` from a clean tree.
2. Validate the V2 artifact and add `.portfolio-control/PUBLICATION_EVIDENCE.json`.
3. Change status to `published`, commit, push, and verify the exact head.

## Decisions

- Clean Architecture; composition stays outside application.
- REST plus CLI; no broker or cloud dependency.
- Local hashing/JSON adapters are defaults, not hard-coded use-case dependencies.
- API accepts safe relative paths; CLI remains a trusted local interface.
- Recall is macro-averaged from per-question recovered/total ratios.
- V1 execution evidence and V2 publication provenance remain separate contracts.

## Open Risks

- The fixture is intentionally easy and small.
- No model-backed embedding or production vector-store adapter exists yet.
- No cross-repository integration test exists for the wider AI Evaluation and Retrieval program.
