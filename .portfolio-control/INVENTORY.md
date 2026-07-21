# Portfolio Control: #3 rag-knowledge-base

## Identity

- **Program:** AI Evaluation and Retrieval Systems
- **Status:** benchmarked
- **Proves:** local retrieval pipeline, correct Recall@k semantics, replaceable adapters, and safe FastAPI file boundaries
- **Primary benchmark:** `recall_at_3 = 1.00`

## Evidence Map

| Evidence | Location | State |
|---|---|---|
| Specification | `sdd/spec.md` | complete |
| Architecture/technical decisions | `sdd/architecture-decision.md`, `sdd/technical-decision.md` | complete |
| Benchmark method | `sdd/benchmark-plan.md` | complete |
| Docker benchmark result | `benchmarks/results/retrieval-baseline.json` | versioned |
| Behavioral/security tests | `tests/test_retrieval.py`, `tests/test_api.py` | 6 passing |
| OpenSpec verification | `openspec/artifacts/verification.md` | local evidence complete |
| Reuse review | `sdd/reuse-improvement-review.md` | complete |
| Remote publication | GitHub branch and Actions | pending verification |

Update this inventory when the benchmark, adapter contract, or publication evidence changes.
