# Benchmark Plan: rag-knowledge-base

## Hypothesis

A deterministic local vector retriever can provide a reproducible RAG baseline with Recall@3 >= 0.85, low single-query latency, and zero paid API cost on the included fixture.

## Command

```powershell
$env:PYTHONPATH = "src"
python -m rag_knowledge_base evaluate --output benchmarks/results/retrieval-baseline.json
```

## Environment

- OS: Linux container on Docker Desktop/WSL2 for the committed baseline.
- Python: 3.12.13 in the Docker baseline.
- GPU: not required.
- External services: none.
- Paid secrets: none.
- Date: 2026-07-16.

## Inputs

- Corpus: `data/fixtures/corpus.jsonl`
- Questions: `data/fixtures/questions.jsonl`
- Corpus size: 8 documents.
- Evaluation size: 7 questions.
- Top K: 3.
- Embedding provider: local hashing, 384 dimensions.

## Metrics

| Metric | Unit | Source | Why it matters |
|---|---:|---|---|
| recall_at_3 | ratio | evaluation script | proves relevant context appears in the retrieval set |
| avg_latency_ms | ms | evaluation script | proves local query speed |
| p95_latency_ms | ms | evaluation script | shows tail behavior on the fixture |
| cost_per_query_usd | USD | static local provider cost | proves no paid API is required |

## Baseline Result

| Metric | Value | Unit |
|---|---:|---|
| recall_at_3 | 1.00 | ratio |
| avg_latency_ms | 18.90 | ms |
| p95_latency_ms | 30.76 | ms |
| cost_per_query_usd | 0.000000 | USD |

Result file: `benchmarks/results/retrieval-baseline.json`.
