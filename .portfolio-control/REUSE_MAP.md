# Reuse Map: #3 rag-knowledge-base

## Kit Inputs

| Concern | Source of truth | Project use |
|---|---|---|
| Agent skills | `.codex/skills/`, `.claude/skills/` | execution and handoff rules |
| Architecture/principles | `.portfolio/decision-brain/` | Clean Architecture, DIP, KISS/YAGNI decisions |
| API style | `.portfolio/decision-brain/api-style-matrix.yaml` | REST plus CLI selection |
| Benchmark contract | `.portfolio/contracts/benchmark-result.schema.json` | machine-readable primary result |
| Local-first | `.portfolio/decision-brain/cloud-matrix.yaml` | Docker/no-secret default; no unnecessary cloud |
| SDD/OpenSpec | `.portfolio/sdd/`, local `sdd/`, `openspec/` | traceable requirements and evidence |

## Project Delta

| Delta | Scope | Action |
|---|---|---|
| per-question recovered/total Recall@k implementation | retrieval-specific implementation | keep local |
| injected `RetrievalService` and local composition root | reusable architecture pattern, project-specific code | document; do not extract yet |
| rooted FastAPI path policy | likely reusable security pattern | kit backlog after second adopter |
| explicit benchmark sample/warm-up semantics | cross-portfolio contract improvement | kit schema/harness backlog |
| corpus and questions | project-specific evidence | reject extraction |

## Coupling Rule

Domain/application code does not depend on infrastructure, FastAPI, model vendors, brokers, or cloud SDKs. Reuse is accepted only when another project confirms the same stable contract.
