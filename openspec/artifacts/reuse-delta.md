# Reuse Delta: rag-knowledge-base

## Reusable Discoveries

| Candidate | Decision | Reason | Follow-up |
|---|---|---|---|
| benchmark sample-definition contract | backlog | `repeat` is ambiguous without warm-up and sample semantics | extend the kit schema after sibling benchmark review |
| rooted FastAPI path policy tests | backlog | file-processing APIs share traversal risk | extract after a second project confirms the shape |
| deterministic retrieval harness | backlog | RAG and embedding comparisons may share inputs/results | compare with `embeddings-benchmark` first |
| fixture corpus/questions | reject | evidence is specific to this repository | keep local |

## Final Gate

- [x] Reuse improvement considered after independent audit.
- [x] Candidates recorded for the kit without modifying another repository.
- [x] Project-specific implementation remains local.
