# Reuse Improvement Review

Project: `3 - rag-knowledge-base`

## Review Points

- [x] after scaffold
- [x] after architecture decision
- [x] after first working slice
- [x] after independent audit
- [x] after benchmark correction
- [x] before local commit

## Findings

| Finding | Classification | Kit Area | Action | Status |
|---|---|---|---|---|
| Projects need an explicit reuse-improvement loop. | `patch_now` | decision brain, skills, SDD | Added to the kit before this repository was implemented. | done |
| Benchmark contracts must define what `repeat` and each sample mean. | `backlog` | benchmark schema/harness | Require repetition count, warm-up policy, timed sample count, and sample definition in the shared contract. | recorded |
| HTTP file-processing projects need reusable rooted-path policy tests. | `backlog` | FastAPI profile/security skill | Extract only after a second project confirms the same boundary. | recorded |
| A deterministic retrieval harness may be reusable across RAG/embedding projects. | `backlog` | harness/templates | Compare with `embeddings-benchmark` before extracting shared code. | recorded |
| This corpus/questions fixture should move into the kit. | `reject` | templates | It is project-specific evidence and remains here. | done |

## Final Gate

- [x] Reusable improvements were patched or recorded.
- [x] Project-specific implementation was not moved into the kit.
- [x] Validation reflects benchmark semantics, dependency direction, API security, and publication evidence.
