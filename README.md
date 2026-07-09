# #3 rag-knowledge-base

**Status:** scaffold

**Proves:** RAG do zero com busca vetorial.

**Benchmark target:** recall_at_k, latency_ms, cost_per_query.

**Stack:** python, fastapi, qdrant, sentence-transformers, docker.

## Next milestone

Implement the smallest Docker-runnable version and produce the first JSON benchmark under enchmarks/results/.

## Run

`ash
docker build -t rag-knowledge-base .
docker run --rm rag-knowledge-base
`

## Benchmark

`ash
docker run --rm rag-knowledge-base benchmark
`

| Metric | Value | Unit |
|---|---:|---|
| recall_at_k, latency_ms, cost_per_query | pending | pending |

## Architecture

Defined in sdd/spec.md before implementation.

## References

See REFERENCES.md.