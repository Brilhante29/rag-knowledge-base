# Change Design: auditable retrieval baseline

## Decision

- Architecture: Clean Architecture with injected ports and an infrastructure composition root.
- Stack: Python, FastAPI, local hashing embeddings, JSON vector store.
- API style: REST/HTTP plus trusted local CLI.
- Messaging/cloud: none; default remains local-first.

## Boundaries

- Domain owns `EmbeddingProvider`, `VectorStore`, and `VectorStoreFactory`.
- Application owns retrieval, indexing, Recall@k, and measurement policy.
- Infrastructure owns adapter creation/loading and local composition.
- FastAPI owns untrusted path validation under configured roots.
- CLI may accept explicit paths because it runs as a trusted local process.

## Benchmark Design

Warm up each question once, then run five complete repetitions. Compute each question's recovered/total Recall@3, macro-average by repetition, and retain every numerator, denominator, recall, and latency.

## Engineering Rules

- Enforce DIP with constructor injection.
- Preserve LSP by checking embedding/store dimensions.
- Keep ports narrow and lifecycle creation in a factory.
- Reject absolute/traversal paths before filesystem access.
- Do not describe questions as repetitions.
- State that the fixture proves execution, not production quality.

## Rejected Alternatives

- Concrete adapter construction in use cases: violates DIP.
- Path allowlists of exact filenames: too rigid for local datasets; rooted relative paths provide the needed boundary.
- Adding Qdrant or model downloads: unrelated to correcting the audited proof.
