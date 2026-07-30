# Agent Handoff

Project: `3 - rag-knowledge-base`
Status: `published`

## Current State

- Recall@3: 1.00 on the 8-document/7-question fixture.
- Method: 5 repetitions, 35 timed queries, 7 excluded warm-ups.
- V2 Docker result: average 0.3175 ms, p95 0.4523 ms, zero paid cost.
- Application depends on embedding/vector-store ports through `RetrievalService`.
- HTTP filesystem access is confined by `ApiPathPolicy`.
- Local test suite: 6 tests covering behavior, DI, metric semantics, and path security.
- V2 artifact: `benchmarks/publication/retrieval-baseline-v2.json`, validated against the central contract.
- Exact-head GitHub Actions run `30578422267` passed for `eafd61108bb4536184c963cf45176242e3f15c57`.
- Publication evidence: `.portfolio-control/PUBLICATION_EVIDENCE.json`.

## Continue From Here

1. Treat #3 as complete in the central portfolio queue.
2. Reuse its V2 benchmark producer, publication evidence contract, rooted API path policy, and lockfile pattern in the next project.
3. Start project #11 only after the kit's central validator confirms the updated publication candidate.

## Decisions

- Clean Architecture; composition stays outside application.
- REST plus CLI; no broker or cloud dependency.
- Local hashing/JSON adapters are defaults, not hard-coded use-case dependencies.
- API accepts safe relative paths; CLI remains a trusted local interface.
- Recall is macro-averaged from per-question recovered/total ratios.
- V1 execution evidence and V2 publication provenance remain separate contracts.
- Published status requires exact-head CI evidence and a versioned V2 artifact.

## Open Risks

- The fixture is intentionally easy and small.
- No model-backed embedding or production vector-store adapter exists yet.
- No cross-repository integration test exists for the wider AI Evaluation and Retrieval program.