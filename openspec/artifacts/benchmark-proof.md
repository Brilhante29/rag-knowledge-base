# Benchmark Proof: rag-knowledge-base

## Primary Metric

- Metric: `recall_at_3`
- Unit: `ratio`
- Result: Recall@3 = 1.00
- Result path: `benchmarks/results/retrieval-baseline.json`

## Docker Command

```powershell
$resultDir = (Resolve-Path benchmarks/results).Path
docker run --rm -v "${resultDir}:/results" rag-knowledge-base evaluate --repetitions 5 --output /results/retrieval-baseline.json
```

## Method And Evidence

- 5 complete repetitions.
- 7 questions per repetition; 35 timed query samples.
- 7 warm-up queries excluded.
- Per-question recall = recovered relevant / total relevant.
- Macro Recall@3 = 1.00.
- Average latency = 1.65 ms.
- P95 latency = 1.97 ms.
- Cost/query = $0.000000.
- Environment: Python 3.12.13, Linux Docker image on Docker Desktop/WSL2.

The fixture is small and intentionally easy. This proves the metric and local pipeline contract, not production retrieval quality.
