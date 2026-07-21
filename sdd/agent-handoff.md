# Agent Handoff

Project: `3 - rag-knowledge-base`
Status: `benchmarked`

## Current State

- Recall@3: 1.00 on the 8-document/7-question fixture.
- Method: 5 repetitions, 35 timed queries, 7 excluded warm-ups.
- Docker result: average 1.65 ms, p95 1.97 ms, zero paid cost.
- Application depends on embedding/vector-store ports through `RetrievalService`.
- HTTP filesystem access is confined by `ApiPathPolicy`.
- Local test suite: 6 tests covering behavior, DI, metric semantics, and path security.

## Continue From Here

1. Run `powershell -ExecutionPolicy Bypass -File tools/validate-project.ps1`.
2. Review `git diff --check` and the benchmark JSON.
3. Commit locally.
4. Push the branch and verify GitHub Actions before changing status to `published`.
5. Add publication evidence instead of inferring remote success from local files.

## Decisions

- Clean Architecture; composition stays outside application.
- REST plus CLI; no broker or cloud dependency.
- Local hashing/JSON adapters are defaults, not hard-coded use-case dependencies.
- API accepts safe relative paths; CLI remains a trusted local interface.
- Recall is macro-averaged from per-question recovered/total ratios.

## Open Risks

- The fixture is intentionally easy and small.
- Dependencies and GitHub Actions are range/tag pinned, not immutable digest/SHA pinned.
- No model-backed embedding or production vector-store adapter exists yet.
- No cross-repository integration test exists for the wider AI Evaluation and Retrieval program.
