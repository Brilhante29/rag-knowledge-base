# Intent: rag-knowledge-base

## Measurable Claim

Local-first RAG knowledge base with deterministic vector retrieval, FastAPI serving, and reproducible Recall@k benchmark.

## Problem

Builds the reusable retrieval layer for the AI evaluation and RAG platform program, proving grounded context retrieval before LLM generation.

## In Scope

- Use the selected component pack: `ai-evaluation-retrieval`.
- Keep the project under the AI Evaluation and Retrieval Systems program.
- Preserve the benchmark contract: `recall_at_3` in `benchmarks/results/retrieval-baseline.json`.
- Keep the default path local-first and reproducible.

## Out Of Scope

- Paid credentials for the default demo.
- External infrastructure that is not required by the benchmark.
- Replacing local portfolio skills with external components silently.

## Default Demo Path

- Status: benchmarked
- Runtime: python-cli-and-fastapi-uvicorn
- Benchmark command: `python -m rag_knowledge_base evaluate --output benchmarks/results/retrieval-baseline.json`

## Public Proof

- Benchmark: Recall@3 = 1.00
- Result path: `benchmarks/results/retrieval-baseline.json`
