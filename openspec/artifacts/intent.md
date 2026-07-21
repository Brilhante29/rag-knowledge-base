# Intent: rag-knowledge-base

## Measurable Claim

Local-first RAG knowledge base with deterministic vector retrieval, FastAPI serving, and reproducible Recall@k benchmark.

## Problem

Provide the retrieval component for AI Evaluation and Retrieval Systems with an auditable metric and replaceable adapters.

## In Scope

- Preserve `recall_at_3` in `benchmarks/results/retrieval-baseline.json`.
- Compute recovered/total recall for every question.
- Keep local provider/store selection behind ports.
- Confine HTTP paths to configured roots.
- Record repetitions and timed samples explicitly.

## Out Of Scope

- Production-quality claims from the fixture.
- Paid credentials, managed infrastructure, LLM generation, and silent external components.

## Default Demo Path

- Status: benchmarked.
- Runtime: Python CLI and FastAPI/Uvicorn in Docker.
- Benchmark: 5 repetitions, 35 timed queries, Recall@3 1.00.

## Publication Rule

Do not change status to `published` until the branch is pushed and remote CI success is verified.
