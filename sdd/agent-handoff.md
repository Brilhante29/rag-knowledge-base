# Agent Handoff

Project: `3 - rag-knowledge-base`
Status: `published`

## Current State

- Recall@3: 1.00 on the 8-document/7-question fixture.
- Method: 5 repetitions, 35 timed queries, 7 excluded warm-ups.
- V2 Docker result: average 0.3175 ms, p95 0.4523 ms, zero paid cost.
- Application depends on embedding/vector-store ports through `RetrievalService`.
- HTTP filesystem access is confined by `ApiPathPolicy`.
- Local test suite: 7 tests covering behavior, DI, metric semantics, artifact export, and path security.
- `export-eval-artifact` produces the contract consumed by `llm-eval-harness` without source imports between repositories.
- V2 artifact: `benchmarks/publication/retrieval-baseline-v2.json`, validated against the central contract.
- Exact-head GitHub Actions run `30578422267` passed for `eafd61108bb4536184c963cf45176242e3f15c57`.
- Publication evidence: `.portfolio-control/PUBLICATION_EVIDENCE.json`.

## Continue From Here

1. Pin the final #3 source commit in the #2 consumer-contract CI.
2. Record exact-head CI in the central reuse kit.
3. Keep model-backed generation outside this retrieval artifact; the exported prediction is explicitly the top retrieved context.

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
- The hashing baseline can retrieve the wrong top context on harder questions; fixture results are not production retrieval quality.
