# Verification: rag-knowledge-base

## Inputs

- Manifest: `project.yaml`
- Code: domain ports, injected application service, local adapters, CLI/FastAPI.
- Tests: `tests/test_retrieval.py`, `tests/test_api.py`.
- Benchmark: `benchmarks/results/retrieval-baseline.json`.
- Decisions: `sdd/` and this OpenSpec change.

## Verified Locally

- Baseline before edits: 2 tests passed with `PYTHONPATH=src`.
- Corrected suites: 6 unittest tests and 6 pytest tests passed.
- Docker image built successfully.
- Docker benchmark produced Recall@3 1.00 with 5 repetitions and 35 timed samples.
- README and benchmark artifact report the same metrics.
- `openspec validate --all --strict` passes: 1 change, 0 failures.
- Application source contains no infrastructure import.
- API tests reject Windows/POSIX absolute paths and traversal.

## Publication State

Status remains `benchmarked`. GitHub push and remote CI success are not inferred from local validation and remain required before `published`.
