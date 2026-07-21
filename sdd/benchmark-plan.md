# Benchmark Plan: rag-knowledge-base

## Hypothesis

The deterministic local retriever reaches Recall@3 >= 0.85 at zero paid API cost on the included fixture.

## Command

```powershell
$resultDir = (Resolve-Path benchmarks/results).Path
docker run --rm -v "${resultDir}:/results" rag-knowledge-base evaluate --repetitions 5 --output /results/retrieval-baseline.json
```

## Environment

- Runtime: Linux Docker image on Docker Desktop/WSL2.
- Python: 3.12.13.
- GPU/external services/paid secrets: none.
- Recorded: 2026-07-21.

## Inputs

- 8 corpus documents.
- 7 questions; 8 total relevance labels because q2 has two relevant documents.
- Top K: 3.
- Local hashing embeddings: 384 dimensions.
- JSON vector store loaded once before timing.

## Measurement

Each question's Recall@k is `|relevant retrieved| / |relevant|`. One warm-up pass is excluded. Five measured repetitions produce five macro Recall@3 samples and 35 query-latency samples. The JSON retains every per-question numerator, denominator, recall, repetition, and latency.

## Baseline Result

| Metric | Value | Unit |
|---|---:|---|
| recall_at_3 | 1.00 | ratio |
| avg_latency_ms | 1.65 | ms |
| p95_latency_ms | 1.97 | ms |
| cost_per_query_usd | 0.000000 | USD |
| repetitions | 5 | runs |
| timed_query_samples | 35 | queries |

This small fixture validates the pipeline and metric implementation, not production retrieval quality. Result: `benchmarks/results/retrieval-baseline.json`.
