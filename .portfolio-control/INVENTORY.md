# Portfolio Control: #3 rag-knowledge-base

## Identity

- **Program:** AI Evaluation and Retrieval Systems
- **Status:** published
- **Proves:** local retrieval, correct Recall@k semantics, replaceable adapters, safe FastAPI paths, and a real prediction-artifact producer
- **Primary benchmark:** `recall_at_3 = 1.00`

## Evidence Map

| Evidence | Location | State |
|---|---|---|
| Specification | `sdd/spec.md` | complete |
| Architecture/technical decisions | `sdd/architecture-decision.md`, `sdd/technical-decision.md` | complete |
| Benchmark method | `sdd/benchmark-plan.md` | complete |
| Docker benchmark result | `benchmarks/results/retrieval-baseline.json` | versioned |
| Behavioral/security tests | `tests/test_retrieval.py`, `tests/test_api.py` | 7 passing |
| Producer-consumer contract | `contracts/prediction-artifact.schema.json`, `data/fixtures/answer-eval.jsonl` | implemented |
| OpenSpec verification | `openspec/artifacts/verification.md` | complete |
| Reuse review | `sdd/reuse-improvement-review.md` | complete |
| Remote publication | `.portfolio-control/PUBLICATION_EVIDENCE.json` and central kit evidence | exact-head gate |

Update this inventory when the benchmark, adapter contract, or publication evidence changes.
