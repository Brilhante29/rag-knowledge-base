# Benchmark Proof: rag-knowledge-base

## Primary Metric

- Metric: `recall_at_3`
- Unit: `ratio`
- Result: Recall@3 = 1.00
- Result path: `benchmarks/results/retrieval-baseline.json`

## Command

`powershell
python -m rag_knowledge_base evaluate --output benchmarks/results/retrieval-baseline.json
`

## Evidence

Average latency: 1.16 ms. P95 latency: 1.22 ms.

The README/post number must come from the committed benchmark JSON, not from manual text.
