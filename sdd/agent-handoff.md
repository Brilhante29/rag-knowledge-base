# Agent Handoff

Project: `3 - rag-knowledge-base`

## Principal Agent Summary

- Objective: Build the first concrete AI Evaluation and RAG Platform project after the reuse kit hardening.
- Portfolio program: AI Evaluation and Retrieval Systems.
- Public proof claim: local-first RAG retrieval with reproducible Recall@k benchmark.
- Primary benchmark: Recall@3.
- Default runnable path: Python CLI and Docker FastAPI service.

## Subagent Decisions

| Role | Decision | Evidence Path | Status |
|---|---|---|---|
| `program-planner` | Place under AI Evaluation and Retrieval Systems. | `project.yaml`, `sdd/spec.md` | done |
| `architecture-selector` | Clean Architecture. | `sdd/architecture-decision.md` | done |
| `engineering-principles-reviewer` | Domain/use cases isolated from API/infrastructure. | `project.yaml`, `sdd/technical-decision.md` | done |
| `stack-decision-agent` | FastAPI backend with local hashing embeddings. | `project.yaml`, code layout | done |
| `api-style-agent` | REST/HTTP plus CLI. | `src/rag_knowledge_base/interfaces/` | done |
| `cloud-local-first-agent` | No cloud default; Kumo reserved for future AWS-like behavior. | `project.yaml` | done |
| `messaging-agent` | No broker. | `sdd/technical-decision.md` | done |
| `language-profile-agent` | Python src-layout FastAPI service. | `pyproject.toml`, `src/`, `tests/` | done |
| `benchmark-harness-agent` | Recall@3/latency/cost benchmark. | `benchmarks/results/retrieval-baseline.json` | done |
| `design-system-agent` | README opens with number, claim, result, architecture, run path. | `README.md` | done |
| `security-reuse-reviewer` | No secrets; references documented. | `REFERENCES.md` | done |
| `reuse-improvement-reviewer` | Reuse loop added to kit before project implementation. | `sdd/reuse-improvement-review.md` | done |
| `release-ci-publisher` | Pending final Docker/push validation. | validation output | pending |

## Local-First Runtime

- Docker command: `docker build -t rag-knowledge-base .`
- Local services: none.
- Kumo services: none in baseline.
- Real cloud adapter target: none.
- Config switch: `PROVIDER=local` future extension.
- Default path requires paid secret: no.

## Benchmark Handoff

- Metric: Recall@3.
- Unit: ratio.
- Higher or lower is better: higher.
- Command: `python -m rag_knowledge_base evaluate --output benchmarks/results/retrieval-baseline.json`
- Result path: `benchmarks/results/retrieval-baseline.json`
- Dataset or fixture: `data/fixtures/`.

## Open Risks

- Fixture is intentionally small; future work should add a harder dataset and optional sentence-transformers/Qdrant adapters.

## Publication Gates

- [x] Docker path exists
- [x] benchmark result exists
- [x] README starts with number, claim, and benchmark
- [x] references are documented
- [x] no secret in files or git remote
- [x] validation passes after Docker build through `tools/validate-project.ps1`
