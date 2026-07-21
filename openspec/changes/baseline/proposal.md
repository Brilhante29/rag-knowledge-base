# Change Proposal: auditable retrieval baseline

Project: `rag-knowledge-base` (#3)

## Intent

Correct the retrieval proof so Recall@k, dependency direction, HTTP filesystem boundaries, and benchmark repetitions are explicit and testable.

## Why This Change Exists

The previous implementation treated any relevant hit as full recall, constructed concrete adapters inside application code, accepted arbitrary API file paths, and labeled seven questions as seven repetitions. Those behaviors contradicted the public metric and Clean Architecture claims.

## Scope

- In scope: per-question Recall@k, injected provider/store ports, rooted API paths, repeated measurements, tests, Docker evidence, and synchronized documentation.
- Out of scope: LLM generation, production datasets, managed providers, authentication, and cross-repository orchestration.

## Portfolio Impact

This change makes the repository a credible retrieval component for `ai-evaluation-retrieval`. Reusable candidates are recorded for the kit, but project-specific fixtures and implementation remain local.

## Acceptance Signal

- Recall uses every relevance label.
- Application imports no infrastructure module.
- HTTP clients cannot escape configured roots.
- The JSON records five repetitions and 35 timed samples.
- Tests, Docker benchmark, and project validation pass.
