# Verification: rag-knowledge-base

## Inputs

- Manifest: `project.yaml`
- Code: domain ports, injected application service, local adapters, CLI/FastAPI.
- Tests: `tests/test_retrieval.py`, `tests/test_api.py`.
- Benchmark: `benchmarks/results/retrieval-baseline.json`.
- Decisions: `sdd/` and this OpenSpec change.

## Verified Locally

- Baseline before edits: 2 tests passed with `PYTHONPATH=src`.
- Corrected suite: 7 unittest tests passed.
- Docker image built successfully.
- Docker benchmark produced Recall@3 1.00 with 5 repetitions and 35 timed samples.
- README and benchmark artifact report the same metrics.
- `openspec validate --all --strict` passes: 1 change, 0 failures.
- Application source contains no infrastructure import.
- API tests reject Windows/POSIX absolute paths and traversal.
- `export-eval-artifact` executes retrieval and emits four contract-valid predictions with producer commit, context IDs, and observed latency.

## Publication State

The baseline is published. Any integration release still requires exact-head GitHub Actions evidence recorded by the central reuse kit.
