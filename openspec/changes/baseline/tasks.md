# Change Tasks: auditable retrieval baseline

## Planning

- [x] Read project, agent, SDD, OpenSpec, and reuse contracts.
- [x] Reproduce the original two-test baseline.
- [x] Confirm audited metric, coupling, path, and repetition defects.
- [x] Preserve the local-first scope and rejected alternatives.

## Implementation

- [x] Compute Recall@k as recovered relevant divided by total relevant.
- [x] Inject embedding and vector-store ports into `RetrievalService`.
- [x] Move local adapter selection to the infrastructure composition root.
- [x] Confine FastAPI paths to configured roots.
- [x] Record warm-up policy, repetitions, and per-query measurements.
- [x] Add behavioral, DI, benchmark-shape, and API security tests.
- [x] Update the committed benchmark and documentation.

## Verification

- [x] Run unit tests and pytest.
- [x] Build Docker image and generate the benchmark in Docker.
- [x] Run `openspec validate --all --strict` with 1 change passed and 0 failed.
- [x] Review reusable improvements and record kit backlog.
- [ ] Verify remote CI before publication.
