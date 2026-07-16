# Benchmark Proof: rag-knowledge-base

## Primary Metric

- Metric: `recall_at_3`
- Unit: `ratio`
- Result: Recall@3 = 1.00
- Result path: `benchmarks/results/retrieval-baseline.json`

## Command

    python -m rag_knowledge_base evaluate --output benchmarks/results/retrieval-baseline.json

## Evidence

Average latency: 18.9 ms. P95 latency: 30.76 ms.

The README/post number must come from the committed benchmark JSON, not from manual text.
