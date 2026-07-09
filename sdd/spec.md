# Spec: rag-knowledge-base

## Number

#3

## Claim

Este projeto prova que: RAG do zero com busca vetorial.

## Stack

python, fastapi, qdrant, sentence-transformers, docker

## User-visible output

- Docker command: pending
- README opens with: # #3 rag-knowledge-base
- Benchmark table: recall_at_k, latency_ms, cost_per_query

## Scope

In:

- Implementar o menor produto funcional que prove o claim.
- Rodar por Docker.
- Gerar benchmark JSON reproduzivel.

Out:

- Publicar repo antes do primeiro resultado numerico.
- Depender de segredo pago para o caminho default.

## Architecture

`	xt
client -> app -> domain -> adapters -> benchmark output
`

## Benchmark

Primary metric:

- name: recall_at_k, latency_ms, cost_per_query
- target: first reproducible baseline
- command: pending
- result file: enchmarks/results/*.json

## Dataset or fixture

- source: pending
- size: pending
- license: pending
- deterministic seed: 42

## Definition of done

- [ ] Docker command works from clean clone.
- [ ] README starts with project number and benchmark result.
- [ ] Benchmark command writes JSON result.
- [ ] Tests cover core behavior.
- [ ] REFERENCES.md explains reuse.
- [ ] No secret or paid credential required for default demo.